"""
    测试文件, 使用访问者模式实现生成ast, 生成字节码

    expr := term + term + term ... + term
    term := factor * factor * factor ... * factor
    factor := num | (expr) | -factor
    
"""
import tokenize


class AddNode(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def visit(self):
        leftValue = self.left.visit()
        rightValue = self.right.visit()
        print("BINARY_ADD")
        return leftValue + rightValue
    def __str__(self):
        return f"<+, {self.left.visit()}, {self.right.visit()}>"
    __repr__ = __str__

class SubNode(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def visit(self):
        leftValue = self.left.visit()
        rightValue = self.right.visit()
        print("BINARY_SUB")
        return leftValue - rightValue
    def __str__(self):
        return f"<-, {self.left.visit()}, {self.right.visit()}>"
    __repr__ = __str__


class MulNode(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def visit(self):
        leftValue = self.left.visit()
        rightValue = self.right.visit()
        print("BINARY_MUL")
        return leftValue * rightValue
    def __str__(self):
        return f"<*, {self.left.visit()}, {self.right.visit()}>"
    __repr__ = __str__

class DivNode(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def visit(self):
        leftValue = self.left.visit()
        rightValue = self.right.visit()
        print("BINARY_DIV")
        return leftValue / rightValue
    def __str__(self):
        return f"</-, {self.left.visit()}, {self.right.visit()}>"
    __repr__ = __str__

class NumNode(object):
    def __init__(self, value):
        self.value = value

    def visit(self):
        print(f"LOAD_CONST\t{self.value}")
        return self.value
    def __str__(self):
        return f"<num, {self.visit()}>"
    __repr__ = __str__

global currentToken


def currentToken():
    global currentToken
    return currentToken


def nextToken(t):
    global currentToken
    currentToken = next(t)
    return currentToken


def expr(t):
    # 获取第一个term的value, 之后current token 移动到下一个 token
    leftValue = term(t)
    tokenType = currentToken.type
    tokenValue = currentToken.string
    expression = currentToken.line

    value = leftValue

    while tokenValue == "+" or tokenValue == "-":
        print(f"当前的token:\t{tokenValue}")
        nextToken(t)
        rightValue = term(t)

        if tokenValue == "+":
            value = AddNode(value, rightValue)
        elif tokenValue == "-":
            value = SubNode(value, rightValue)

        tokenType = currentToken.type
        tokenValue = currentToken.string

    # print(f"{expression}求值结果: {value}")
    return value


def term(t):
    # factor()之后 current token 移动到下一个
    leftValue = factor(t)
    tokenType = currentToken.type
    tokenValue = currentToken.string

    value = leftValue
    while tokenValue == "*" or tokenValue == "/":
        print(f"当前的token:\t{tokenValue}")

        # 获取下一个factor的value
        nextToken(t)
        rightValue = factor(t)
        if tokenValue == "*":
            value = MulNode(value, rightValue)
        elif tokenValue == "/":
            value = DivNode(value, rightValue)

        tokenType = currentToken.type
        tokenValue = currentToken.string
    return value


def factor(t):
    tokenType = currentToken.type
    tokenValue = currentToken.string

    value = 0
    # number==>2
    if tokenType == 2:
        value = NumNode(int(tokenValue))
        print(f"当前token:\t{value}")
        nextToken(t)
    elif tokenValue == "-":

        print(f"当前token:\t{tokenValue}")
        nextToken(t)
        value = NumNode(-factor(t).visit())

    elif tokenValue == "(":
        print(f"当前token:\t(")
        # current token 移动到下一个
        nextToken(t)
        # 求 expr 的值
        value = expr(t)
        print(f"当前token:\t)")
        # current token后移
        nextToken(t)
    return value



def build():
    a = NumNode(2)
    b = NumNode(3)
    c = NumNode(6)
    
    leftValue = MulNode(a, b)
    res = AddNode(leftValue, c)

    print(res.visit())


if __name__ == "__main__":

    # f = open("./source.txt")

    # t = tokenize.generate_tokens(f.readline)

    # # 把currentToken初始化为第一个Token
    # nextToken(t)

    # res = expr(t)
    # print(res)
    # print(res.visit())

    build()
