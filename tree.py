import dataclasses as dc
from lexer import Token
# a node class
class Node:
    
    def __str__(self):
        return "<%s>" % (self.__class__.__name__)

class Context:

    def __init__(self, **kwargs) -> None:
        self.data = kwargs
    
    def fetch(self, key):
        return self.data.get(key, None)
    
    def setattr(self, key, value):
        self.data[key] = value
    
    def print(self, node):
        print(node)
@dc.dataclass
class IfThenElse(Node):

    condition: Node
    then_branch: Node
    else_branch: Node

    def eval(self):
        if self.condition.eval():
            return self.then_branch.eval()
        else:
            return self.else_branch.eval()
@dc.dataclass
class IfThen(Node):
    condition: Node
    then_branch: Node

    def eval(self):
        if self.condition.eval():
            return self.then_branch.eval()
        else:
            return None 
@dc.dataclass
class While(Node):
    condition: Node
    body: Node

    def eval(self):
        while self.condition.eval():
            self.body.eval()
        return None
@dc.dataclass
class For(Node):
    init: Node
    condition: Node
    update: Node
    body: Node

    def eval(self):
        self.init.eval()
        while self.condition.eval():
            self.body.eval()
            self.update.eval()
        return None

@dc.dataclass
class Function(Node):
    name: str
    args: list[Token]
    body: Node
    context: Context

    def eval(self):
        def f(*args):
            context = self.context.copy()
            for i in range(len(args)):
                context.set(self.args[i].value, args[i])
            return self.body.eval(context)
        setattr(self.context, self.name, f)
@dc.dataclass
class Call(Node):
    name: str
    args: list[Node]
    context: Context
    
    def eval(self):
        if hasattr(self.context, self.name):

            return getattr(self.context, self.name)(self.args.eval())
        else:
            raise Exception("Unknown function %s" % self.name)
@dc.dataclass
class Return(Node):
    value: Node

    def eval(self):
        return self.value.eval()
@dc.dataclass
class Var(Node):
    name: Token
    context: Context

    def eval(self):
        return self.context.fetch(self.name.value)
@dc.dataclass
class BinOp(Node):
    left: Node
    op: Token
    right: Node

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if self.op.value == "+":
            return left + right
        elif self.op.value == "-":
            return left - right
        elif self.op.value == "*":
            return left * right
        elif self.op.value == "/":
            return left / right
        elif self.op.value == "^":
            return left ** right
        else:
            raise Exception("Unknown operator %s" % self.op.value)
@dc.dataclass
class List(Node):
    elements: list[Node]

    def eval(self):
        return [e.eval() for e in self.elements]
@dc.dataclass
class Parentheses(Node):
    expr: Node

    def eval(self):
        return self.expr.eval()
@dc.dataclass
class Commant(Node):
    comment: str

    def eval(self):
        return None
@dc.dataclass
class Number(Node):
    value: str

    def eval(self):
        return int(self.value)
@dc.dataclass
class Float(Node):
    value: str

    def eval(self):
        return float(self.value)


@dc.dataclass
class String(Node):
    value: str

    def eval(self):
        return self.value
@dc.dataclass
class AssignVar(Node):
    name: Token
    value: Node
    context: Context
    
    def eval(self):
        self.context.setattr(self.name.value, self.value.eval())
        return self.context




    






