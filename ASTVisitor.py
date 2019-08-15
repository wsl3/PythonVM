"""
    使用访问者模式构建AST
"""

class BinaryOpNode(object):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def accept(self, visitor):
        return visitor.visitBinaryOp(self)

class ConstNode(object):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visitConst(self)
        

# visitor
class PrintVisitor(object):
    def visitConst(self, node):
        print(f"LOAD_CONST\t{node.value}")
    
    def visitBinaryOp(self, node):
        node.left.accept(self)
        node.right.accept(self)

        if node.op == "+":
            print("BINARY_ADD")
        elif node.op == "-":
            print("BINARY_SUB")
        elif node.op == "*":
            print("BINARY_MUL")
        elif node.op == "/":
            print("BINARY_DIV")

class ResVisitor(object):
    def visitConst(self, node):
        return node.value
    def visitBinaryOp(self, node):
        leftValue = node.left.accept(self)
        rightValue = node.right.accept(self)

        if node.op == "+":
            return leftValue + rightValue
        elif node.op == "-":
            return leftValue - rightValue
        elif node.op == "*":
            return leftValue * rightValue
        elif node.op == "/":
            return leftValue / rightValue



def main():
    a = ConstNode(2)
    b = ConstNode(3)
    c = ConstNode(6)
    d = ConstNode(3)
    
    leftValue = BinaryOpNode("*", a, b)
    rightValue = BinaryOpNode("/", c, d)
    res = BinaryOpNode("+", leftValue,rightValue)

    pv = PrintVisitor()
    pv.visitBinaryOp(res)

    rv = ResVisitor()
    result = rv.visitBinaryOp(res)
    print(result)


if __name__ == "__main__":
    main()


