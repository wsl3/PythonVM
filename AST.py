"""
    测试文件, 使用访问者模式实现生成ast, 生成字节码

    expr := term + term + term ... + term
    term := factor * factor * factor ... * factor
    factor := num | -num | (expr) | -(expr)
    

"""
import tokenize


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
            value = value + rightValue
        elif tokenValue == "-":
            value = value - rightValue

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
            value = value * rightValue
        elif tokenValue == "/":
            try:
                value = value / rightValue
            except ZeroDivisionError as e:
                print("Error: ", e)
                exit(0)
        tokenType = currentToken.type
        tokenValue = currentToken.string
    return value


def factor(t):
    tokenType = currentToken.type
    tokenValue = currentToken.string

    value = 0
    # number==>2
    if tokenType == 2:
        value = int(tokenValue)
        print(f"当前token:\t{value}")
    elif tokenValue == "-":

        print(f"当前token:\t{tokenValue}")
        nextToken(t)
        if currentToken.type == 2:
            print(f"当前token:\t{currentToken.string}")
            value = - int(currentToken.string)
        elif currentToken.string == "(":
            print(f"当前token:\t(")
            nextToken(t)
            value = - expr(t)
            print(f"当前token:\t)")
       
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


if __name__ == "__main__":

    f = open("./source.txt")

    t = tokenize.generate_tokens(f.readline)

    # 把currentToken初始化为第一个Token
    nextToken(t)

    res = expr(t)
    print(res)
