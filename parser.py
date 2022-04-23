import tree
import lexer


def parse_expr(tokens, context, cg=False):
    if len(tokens) == 0:
        return
    token = tokens[0]
    if token.type() == "Float":
        return tree.Float(token.value)
    if token.type() == "Keyword":
        if token.value == "if":
            tokens.pop(0)
            condition = parse_expr(tokens, context, True)
            if len(tokens) == 0:
                raise Exception("Unexpected end of program")
            print(tokens[0].value)
            token = tokens[0]
            if token.value == "then":

                list_value = list(map(lambda x: x.value, tokens))
                if "end" not in list_value:
                    raise Exception("Unexpected end of program: no end")
                else:

                    then_branch = parse_expr(
                        tokens[list_value.index("then")+1:list_value.index("end")],
                        context,
                        True)
                    return tree.IfThen(condition, then_branch)
            else:
                raise Exception("Unexpected token %s" % token)

        elif token.value == "while":
            tokens.pop(0)
            condition = parse_expr(tokens, context, True)
            if len(tokens) == 0:
                raise Exception("Unexpected end of program")
            token = tokens[0]
            if token.value == "do":
                tokens.pop(0)
                body = parse_expr(tokens, context, True)
                return tree.While(condition, body)
            else:
                raise Exception("Unexpected token %s" % token)

    if token.type() == "Atom":
        if hasattr(context, token.value):
            tokens.pop(0)
            return tree.Call(token.value, parse_expr(tokens, context), context)
        return tree.Var(token, context)
    if token.type() == "Number":
        if cg:
            tokens.pop(0)

        return tree.Number(token.value)
    if token.type() == "String":
        if cg:
            tokens.pop(0)
        return tree.String(token.value)
    if token.type() == "Operator":
        if len(tokens) < 3:
            raise Exception("Unexpected end of program")
        if tokens[1].type() == "Operator":
            tokens.pop(0)
            left = parse_expr(tokens, context)
            right = parse_expr(tokens[3:], context)
        else:
            left = parse_expr(tokens[1:], context)
            right = parse_expr(tokens[2:], context)
        return tree.BinOp(left, token, right)
    if token.type() == "SpecialCharactor":
        if token.value == "\n":
            tokens.pop(0)
            return parse_expr(tokens, context)


def parse(tokens, context):
    print(tokens)
    if len(tokens) == 0:
        raise Exception("Empty program")
    return parse_expr(tokens, context)
    

print(parse(lexer.tokenize("""if 1 then 
print 2 
print 3
end"""), tree.Context()).eval())
