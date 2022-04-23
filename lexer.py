import abc
import dataclasses as dc


class Token:
    LIST_OBJ_CAN_USE_ARITHEMETIQUE = ("Int", "Float", "String", "Atom")
    KEYWORD = ("if", "else", "while",
               "for", "fun", "return",
               "true", "false", "null",
               "then", "do", "end")

    
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return self.__class__.__name__ + "(" + self.value + ")"

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.value + ")"
    
    

    @abc.abstractmethod
    def check(self) -> bool:
        raise NotImplementedError

    def type(self):
        return self.__class__.__name__
    
@dc.dataclass
class Operator(Token):
    value: str 
    def check(self) -> bool:
        return self.value in ("+", "-", "*", "/", "^", ":=")


@dc.dataclass
class Atom(Token):
    value: str
    def check(self) -> bool:
        if self.value in Token.KEYWORD:
            return False
        if len(self.value) > 0:
            return self.value[0].isalpha()
        return True

@dc.dataclass
class Number(Token):
    value: str
    def check(self) -> bool:
        if len(self.value) == 0:
            return False
        for i in self.value:
            if not i.isdigit():
                return False
        return True
@dc.dataclass
class Float(Token):
    value: str
    def check(self) -> bool:
        if self.value == "":
            return False
        for i in self.value:
            if not i.isdigit() and i != ".":
                return False
        return True
@dc.dataclass
class String(Token):
    value: str
    def check(self) -> bool:
        if len(self.value) < 2:
            return False 
        else:
            if self.value[0] == '"' and self.value[-1] == '"':
                return True
            elif self.value[0] == "'" and self.value[-1] == "'":
                return True
            else:
                return False 

@dc.dataclass
class Keyword(Token):
    value: str
    def check(self) -> bool:
        return self.value in self.KEYWORD


@dc.dataclass
class Seperator(Token):
        def check(self) -> bool:
            return self.value in ("(", ")", "[", "]", "{", "}", ",")
@dc.dataclass
class SpecialCharactor(Token):
    value: str
    def check(self) -> bool:
        return self.value in ("\n", "\t", "\r")


def args_to_token(tokens):
    lenght_tk = len(tokens)
    if len(filter(lambda x: x.type() == "Seperator", tokens)) != lenght_tk // 2 - 1 :
        return None
    return list(filter(lambda x: x.type() != "Seperator", tokens))

def check_function(tokens):
    len_tokens = len(tokens)
    if len_tokens < 3:
        return False
    
    if tokens[0].type() != "Atom":
        return False
    if tokens[1].type() != "Seperator":
        return False
    if tokens[-1].type() != "Seperator":
        return False
    return True
    
def tokenize(string):
    tokens = []
    is_string = False
    tkchar = ""
    strchar = ""
    for n in  range(len(string)): 
        if is_string:
            strchar += string[n]
        if string[n] == '"':
            if is_string:
                if string[n-1] != "\\":
                    is_string = False
                    tokens.append(String(strchar+ '"'))
                    strchar = ""
            else:
                is_string = True
                strchar = ""
        if string[n] == " " or string[n] == "\n" or string[n] == "\r":
            if string[n] == "\n" or string[n] == "\r":
                tokens.append(SpecialCharactor(string[n]))
            if not tkchar:
                pass
            elif Number(tkchar).check():
                tokens.append(Number(tkchar))
            elif Float(tkchar).check():
                tokens.append(Float(tkchar))
            elif Keyword(tkchar).check():
                tokens.append(Keyword(tkchar))
            elif Atom(tkchar).check():
                tokens.append(Atom(tkchar))
            elif Seperator(tkchar).check():
                tokens.append(Seperator(tkchar))
            elif Operator(tkchar).check():
                tokens.append(Operator(tkchar))
            tkchar = ""
        elif n == len(string) - 1:
            tkchar += string[n]
            if Number(tkchar).check():
                tokens.append(Number(tkchar))
            elif Float(tkchar).check():
                tokens.append(Float(tkchar))
            elif Keyword(tkchar).check():
                tokens.append(Keyword(tkchar))
            elif Atom(tkchar).check():
                tokens.append(Atom(tkchar))
            elif Seperator(tkchar).check():
                tokens.append(Seperator(tkchar))
            elif Operator(tkchar).check():
                tokens.append(Operator(tkchar))
            tkchar = ""
        else:
            tkchar += string[n]
    return tokens


