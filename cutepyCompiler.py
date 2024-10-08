# Zisis Psalidas, 3369, cse63369
# Panagiotis Varelis, 3388, cse63388
from sys import argv
from string import ascii_letters, digits

keywords = ["main", "def", "#def", "input", "print", "return", "if", "elif", "else", "while",
"int", "#int", "global", "not", "or", "and"]
alphanumerics = ascii_letters + digits
operators = ["+", "-", "*", "//", "%"]
comparison = ["<", "<=", "==", ">=", ">", "!="]
delimiters = [":", ","]
grouping = ["(", ")", "#{", "#}"]
white_space = ["\t", " ", "\n"]
symbols = operators + comparison + delimiters + grouping
quadnum = 1
level = 0
symb = open("symb.sym", "w")
fin = open("fin.asm", "w")

def main():
    try:
        file = open(argv[1], "r")
    except Exception:
        print("Could not open file.")
        exit()
    lex = Lex(1, file, None)
    quadList = QuadList()
    table = []
    assembler = Assembler()
    parser = Parser(lex, lex.next_Token(), quadList, table, assembler)
    parser.program()
    print("Lexical and Syntax analysis complete")

    inter = open("inter.int", "w")
    inter.write(str(quadList))

    symb.write(str(table))

#------------------------------------------------------------------------------
class Token:
    def __init__(self, family, unit, line):
        self.family = family
        self.unit = unit
        self.line = line
    
    def __str__(self):
        return ("Family: " + self.family + ", recognized_string: " + self.unit + ", line: " + str(self.line) + "\n")

class Lex:
    def __init__(self, curr_line, file, token):
        self.curr_line = curr_line
        self.file = file
        self.token = None
    
    def error(self, type, unit=""):
        match type:
            case "large string":
                print("Line " + str(self.curr_line) + ": Identifier " + unit + " has more than 30 characters.\n")
                exit()
            case "large number":
                print("Line " + str(self.curr_line) + ": Number " + unit + " out of range.\n")
                exit()
            case "single /":
                print("Line " + str(self.curr_line) + ": Expected //, found /.\n")
                exit()
            case "#":
                print("Line " + str(self.curr_line) + ": Expected #int or #def.\n")
            case "!":
                print("Line " + str(self.curr_line) + ": Expected !=. found !.\n")
            case "invalid":
                print("Line " + str(self.curr_line) + ": Invalid character detected, " + unit + ".\n")
                exit()

    def next_Token(self):
        word = ""
        byte = self.file.read(1)
        if not byte:
            self.token = Token("eof", "eof", self.curr_line)
            return self.token
        while byte:
        # Whitespaces
            if byte in [" ", "\t"]:
                byte = self.file.read(1)
                continue
            elif byte == "\n":
                byte = self.file.read(1)
                self.curr_line += 1
                continue
        # Keywords and identifiers
            if byte in ascii_letters:
                while byte in alphanumerics:
                    word += byte
                    byte = self.file.read(1)
                pointer = self.file.tell()
                self.file.seek(pointer - 1, 0)
                if word in keywords:
                    self.token = Token("keyword", word, self.curr_line)
                    return self.token
                elif len(word) <= 30:
                    self.token = Token("identifier", word, self.curr_line)
                    return self.token
                else:
                    ## Error message for alphanumeric larger than 30 characters
                    self.error("large string", word)
        # Digits
            elif byte in digits:
                while byte in digits:
                    word += byte
                    byte = self.file.read(1)
                pointer = self.file.tell()
                self.file.seek(pointer - 1, 0)
                temp = int(word)
                if (temp > 32767):
                    self.error("large number", word)
                self.token = Token("digit", word, self.curr_line)
                return self.token
        # Operators
            elif byte in ["+", "-"]:
                self.token = Token("add operator", byte, self.curr_line)
                return (self.token)
            elif byte in ["*", "/", "%"]:
                word = byte
                if byte == "/":
                    byte = self.file.read(1)
                    if byte == "/":
                        word += byte
                    else:
                        pointer = self.file.tell()
                        self.file.seek(pointer - 1, 0)
                        self.error("single /")
                self.token = Token("mult operator", word, self.curr_line)
                return(self.token)
        # Delimeters
            elif byte in delimiters:
                word = byte
                self.token = Token("delimeter", word, self.curr_line)
                return (self.token)
        # Grouping
            elif byte in grouping:
                word = byte
                self.token = Token("grouping", word, self.curr_line)
                return (self.token)
        # Comparisons
            elif byte == "<" or byte == ">":
                word += byte
                byte = self.file.read(1)
                if byte == "=":
                    word += byte
                else:
                    pointer = self.file.tell()
                    self.file.seek(pointer - 1, 0)
                self.token = Token("comparison", word, self.curr_line)
                return (self.token)
            elif byte == "=":
                word += byte
                byte = self.file.read(1)
                if byte == "=":
                    word += byte
                else:
                    pointer = self.file.tell()
                    self.file.seek(pointer - 1, 0)
                    self.token = Token("assignment", word, self.curr_line)
                    return (self.token)
                self.token = Token("comparison", word, self.curr_line)
                return (self.token)
            elif byte == "!":
                word += byte
                byte = self.file.read(1)
                if byte == "=":
                    word += byte
                    self.token = Token("comparison", word, self.curr_line)
                    return (self.token)
                else:
                    self.error("!")
        # Comments and #{ #}
            elif byte == "#":
                word += byte
                byte = self.file.read(1)
                if byte == "#":
                    while byte:
                        byte = self.file.read(1)
                        if byte == "#":
                            byte = self.file.read(1)
                            if byte == "#":
                                break
                            else:
                                pointer = self.file.tell()
                                self.file.seek(pointer - 1, 0)
                    word = ""
                    byte = self.file.read(1)
                elif byte == "{" or byte == "}":
                    word += byte
                    self.token = Token("grouping", word, self.curr_line)
                    return (self.token)
                else:
                    word += byte
                    byte = self.file.read(1)
                    word += byte
                    byte = self.file.read(1)
                    word += byte
                    if word in keywords:
                        self.token = Token("keyword", word, self.curr_line)
                        return (self.token)
                    else:
                        self.error("#")

            else:
                self.error("invalid", byte)
#------------------------------------------------------------------------------
class Parser:
    def __init__(self, lex, token, quadList, table, assembler):
        self.lex = lex
        self.token = token
        self.funcs = {"functions": {}, "variables": [], "formal params": [], "parent functions": {}, "parent variables": []}
        self.quads = quadList
        self.table = table
        self.assembler = assembler
        
    def get_Token(self):
        self.token = self.lex.next_Token()
        return self.token

    def error(self, type):
        match type:
            case "main":    
                print("Line " + str(self.token.line) + ": Main function definition not found but got " + str(self.token.unit) + ".\n")
                exit()
            case "variable defined":
                print("Line " + str(self.token.line) + ": Variable " + str(self.token.unit) + " already defined.\n")
                exit()
            case "identifier expected":
                print("Line " + str(self.token.line) + ": Expected identifier but got " + str(self.token.unit) + ".\n")
                exit()
            case "main expected":
                print("Line " + str(self.token.line) + ": Expected main after #def but got " + str(self.token.unit) + ".\n")
                exit()
            case "function defined":
                print("Line " + str(self.token.line) + ": Function " + str(self.token.unit) + " already defined.\n")
                exit()
            case "#{ expected":
                print("Line " + str(self.token.line) + ": Expected #{ after function declaration but got " + str(self.token.unit) + ".\n")
                exit()
            case "#} expected":
                print("Line " + str(self.token.line) + ": Expected #} after code block but got " + str(self.token.unit) + ".\n")
                exit()
            case "( expected":
                print("Line " + str(self.token.line) + ": Expected ( after function identifier or function call but got " + str(self.token.unit) + ".\n")
                exit()
            case ") expected":
                print("Line " + str(self.token.line) + ": Expected ) after function identifier or function call.\n but got " + str(self.token.unit) + ".\n")
                exit()
            case ": expected":
                print("Line " + str(self.token.line) + ": Expected : after function declaration or condition in flow control statement but got " + str(self.token.unit) + ".\n")
                exit()
            case "= expected":
                print("Line " + str(self.token.line) + ": Expected = for assignment to variable but got " + str(self.token.unit) + ".\n")
                exit()
            case "input expected":
                print("Line " + str(self.token.line) + ": Expected input after ( but got " + str(self.token.unit) + ".\n")
                exit()
            case "statement expected":
                print("Line " + str(self.token.line) + ": Expected at least one statement in code block but got " + str(self.token.unit) + ".\n")
                exit()
            case "illegal expression":
                print("Line " + str(self.token.line) + ": Illegal expression " + str(self.token.unit) + ".\n")
                exit()
            case ", expected":
                print("Line " + str(self.token.line) + ": Expected , in formal parameters list but got " + str(self.token.unit) + ".\n")
                exit()
            case "arguements expected":
                print("Line " + str(self.token.line) + ": Expected required number of arguements but got " + str(self.token.unit) + ".\n")
                exit()
            case "invalid global":
                print("Line " + str(self.token.line) + ": Identifier " + str(self.token.unit) + " is not a global parameter.\n")
                exit()
            case "illegal argument":
                print("Line " + str(self.token.line) + ": Illegal argument " + str(self.token.unit) + ".\n")
                exit()
            
    def program(self):
        global level

        ##Add global scope to table
        scope = Scope("global", level)
        self.table.append(scope)
        level += 1

        self.quads.genQuad("begin_block", "program", "_", "_")
        if self.token.unit == "eof":
            self.quads.genQuad("end_block", "program", "_", "_")
            return
        while self.token.unit == "#int":
            self.get_Token()
            self.declarations(self.funcs["variables"], glob = True)
        fin.write("\t.data\nstr_nl: .asciz \"\\n\"\n\t.text \n")
        fin.write("j main\n")

        while self.token.unit == "def":
            self.get_Token()
            self.func(self.funcs)
        if self.token.unit == "#def":
            self.get_Token()
            self.maindef()
        else:
            ## Expected main definition
            self.error("main")
        
        self.quads.genQuad("end_block", "program", "_", "_")
    

    def declarations(self, var_list, arg="Variable", glob=False):
        if self.token.family != "identifier":
            self.error("identifier expected")
        if self.token.unit in var_list or self.token.unit in self.funcs["variables"]:
            ## Variable already defined
            self.error("variable defined")
        var_list.append(self.token.unit) ##save global variable
        
        ##Add Entity to scope's entity list
        if arg == "Variable" and (self.token.unit not in self.funcs["variables"] or glob == True):
            entity = Variable(self.token.unit, self.table[-1].offset)    
        else:
            entity = Argument(self.token.unit, self.table[-1].offset, "cv")
        self.table[-1].offset += 4
        self.table[-1].entitylist[self.token.unit] = entity

        self.get_Token()
        if self.token.unit == ",":
            self.get_Token()
            self.declarations(var_list, arg)
            
    def globals_decleration(self, globals):
        if self.token.family != "identifier":
            self.error("identifier expected")
        if self.token.unit not in self.funcs["variables"]:
            self.error("invalid global")
        globals.append(self.token.unit)

        ##Add Entity to scope's entity list
        if self.token.unit not in self.funcs["variables"]:
            entity = Variable(self.token.unit, self.table[-1].offset)
            self.table[-1].offset += 4
            self.table[-1].entitylist[self.token.unit] = entity

        self.get_Token()
        if self.token.unit == ",":
                self.get_Token()
                self.globals_decleration(globals)

    def maindef(self):
        global level

        if self.token.unit != "main":
            ## Expected main
            self.error("main expected")
        self.get_Token()
        
        self.quads.genQuad("begin_block", "main", "_", "_")

        ##Add Entity to scope's entity list
        entity = Function("main", self.quads.nextQuad(), 0)
        self.table[-1].entitylist["main"] = entity

        ##Add Scope to table
        scope = Scope("main", level)
        self.table.append(scope)
        level += 1

        while self.token.unit == "#int":
            self.get_Token()
            self.declarations(self.funcs["variables"], glob = True)
        self.block(self.funcs)
        self.quads.genQuad("end_block", "main", "_", "_")

        ##Write to final code
        self.assembler.assemble(self.quads, self.table, 1, True)

        ##Remove Scope from table
        level -= 1
        symb.write(str(self.table.pop()))
        

    def func(self, parent_func):
        global level
        global symb 

        if self.token.family == "identifier":
            if self.token.unit in parent_func["functions"] or self.token.unit in parent_func["variables"]:
                ## func already defined
                self.error("function defined")
            current_function = self.token.unit
            parent_func[current_function] = {"formal params": [], "globals": [], "variables": [], "parent variables": [], "functions": {}, "parent_functions": {}}
            parent_func["functions"][current_function] = parent_func[current_function]
            parent_func[current_function]["parent_functions"] = parent_func["functions"]
            parent_func[current_function]["parent variables"] = parent_func["variables"]
            
            self.quads.genQuad("begin_block", self.token.unit, "_", "_")

            ##Add Entity to scope's entity list
            entity = Function(current_function, self.quads.nextQuad(), 0)
            self.table[-1].entitylist[current_function] = entity

            ##Add Scope to table
            scope = Scope(current_function, level)
            self.table.append(scope)
            level += 1

            self.get_Token()
            self.func_declaration(parent_func[current_function]["formal params"])
        else:
            ## Expected identifier
            self.error("identifier expected")
        self.get_Token()
        if self.token.unit != "#{":
            ## Expected #{ after function declaration
            self.error("#{ expected")
        self.get_Token()
        while self.token.unit == "#int":
            self.get_Token()
            self.declarations(parent_func[current_function]["variables"])
        while self.token.unit == "def":
            self.get_Token()
            self.func(parent_func[current_function])
        while self.token.unit == "global":
            self.get_Token()
            self.globals_decleration(parent_func[current_function]["globals"])
        
        #Add starting quad to entity
        self.table[-2].entitylist[current_function].startQuad = self.quads.nextQuad()
        
        self.block(parent_func[current_function])
        self.quads.genQuad("end_block", current_function, "_", "_")
        if self.token.unit != "#}":
            ## Expected #} after code block
            self.error("#} expected")
        self.get_Token()

        ##Fill out frame len in function entity
        self.table[-2].entitylist[current_function].framelen = self.table[-2].offset

        #Produce final code for function
        self.assembler.assemble(self.quads, self.table, 2)

        ##Remove Scope from table
        level -= 1

        ##Write to symb.sym      
        symb.write(str(self.table.pop()))

    def func_declaration(self, formal_params):
        if self.token.unit != "(":
             ## Expected (
            self.error("( expected")
        self.get_Token()
        self.declarations(formal_params, "Arguement")
        if self.token.unit != ")":
            ## Expected ) after formal parameters
            self.error(") expected")
        self.get_Token()
        if self.token.unit != ":":
            ## Expected : after function declaration
            self.error(": expected")
    
    def single_block(self, function):
        if self.token.unit == "if":
            self.get_Token()
            self.if_call(function)
        elif self.token.unit == "while":
            self.get_Token()
            self.while_call(function)
        elif self.token.unit == "return":
            self.get_Token()
            self.return_call(function)
        elif self.token.unit == "print":
            self.get_Token()
            self.print_call(function)
        elif self.token.family == "identifier" and (self.token.unit in function["variables"] or self.token.unit in self.funcs["variables"]):
            id = self.token.unit
            self.get_Token()
            self.assignment(function, id)
        else:
            return 0
        return 1
        
    def block(self, function):
        statements = 0
        while self.token.unit != "#}":
            if self.token.unit == "if":
                statements += 1
                self.get_Token()
                self.if_call(function)
            elif self.token.unit == "while":
                statements += 1
                self.get_Token()
                self.while_call(function)
            elif self.token.unit == "return":
                statements += 1
                self.get_Token()
                self.return_call(function)
                return statements
            elif self.token.unit == "print":
                statements += 1
                self.get_Token()
                self.print_call(function)
            elif self.token.family == "identifier" and (self.token.unit in function["variables"] or self.token.unit in self.funcs["variables"]):
                statements += 1
                idplace = self.token.unit
                self.get_Token()
                self.assignment(function, idplace)
            if self.token.unit == "eof":
                return statements
        return statements
    
    def assignment(self, function, idplace):
        eplace = [" "]
        if self.token.unit != "=":
            ## Expected = after variable
            self.error("= expected")
        self.get_Token()
        if self.token.unit == "int":
            self.get_Token()
            if self.token.unit != "(":
                ## Expected ( after int
                self.error("( expected")
            self.get_Token()
            if self.token.unit != "input":
                ## Expected input after (
                self.error("input expected")
            self.get_Token()
            if self.token.unit != "(":
                ## Expected ( after input
                self.error("( expected")    
            self.get_Token()
            if self.token.unit != ")":
                ## Expected ) after (
                self.error(") expected")
            self.get_Token()
            if self.token.unit != ")":
                ## Expected ) after input
                self.error(") expected")
            self.get_Token()
            w = self.quads.newTemp()
            self.quads.genQuad("in", w, "_", idplace)

            ##Add temp variable entity to scope's entity list
            entity = Temp(w, self.table[-1].offset)
            self.table[-1].offset += 4
            self.table[-1].entitylist[w] = entity

            return
        self.expression(function, eplace)
        self.quads.genQuad("=", eplace[0], "_", idplace)

    def while_call(self, function):
        rule = Rule()

        q = self.quads.nextQuad()
        self.condition(function, rule)
        if self.token.unit != ":":
            ## Expected : after condition
            self.error(": expected")
        self.get_Token()
        hash_flag = False
        statements = 0
        if self.token.unit == "#{":
            hash_flag = True
            self.get_Token()
            self.quads.backPatch(rule.true, self.quads.nextQuad())
            statements = self.block(function)
        else:
            self.quads.backPatch(rule.true, self.quads.nextQuad())
            statements = self.single_block(function)
        if hash_flag:
            if self.token.unit != "#}":
                ## Expected #} after code block
                self.error("#} expected")
            self.get_Token()
        if statements > 1 and not hash_flag:
            ## Expected #} after multiple statements code block
            self.error("#} expected")
        elif statements < 1:
            ## Expected at least one statement in code block
            self.error("statement expected")
        self.quads.genQuad("jump", "_", "_", q)
        self.quads.backPatch(rule.false, self.quads.nextQuad())
                
    def if_call(self, function, else_flag=False):
        global quadnum

        rule = Rule()

        self.condition(function, rule)
        
        if self.token.unit != ":":
            ## Expected : after condition
            self.error(": expected")
        self.get_Token()
        
        self.quads.backPatch(rule.true, self.quads.nextQuad())
        hash_flag = False
        statements = 0
        if self.token.unit == "#{":
            hash_flag = True
            self.get_Token()
            statements = self.block(function)
        else:
            statements = self.single_block(function)
        
        L1 = self.quads.nextQuad()
        self.quads.genQuad("jump", "_", "_", "_")
        self.quads.backPatch(rule.false, self.quads.nextQuad())
       
        if hash_flag:
            if self.token.unit != "#}":
                ## Expected #} after code block
                self.error("#} expected")
            self.get_Token()
        if statements > 1 and not hash_flag:
            ## Expected #} after multiple statements code block
            self.error("#} expected")
        elif statements < 1:
            ## Expected at least one statement in code block
            self.error("statement expected")
        
        if (else_flag):
            return
        while self.token.unit == "elif":
            self.get_Token()
            self.if_call(function, True)
        if self.token.unit == "else":
            self.get_Token()
            if self.token.unit != ":":
                self.error(": expected")
            self.get_Token()      
            hash_flag = False
            statements = 0
            if self.token.unit == "#{":
                hash_flag = True
                self.get_Token()
                statements = self.block(function)
            else:
                statements = self.single_block(function)
            if hash_flag:
                if self.token.unit != "#}":
                    ## Expected #} after code block
                    self.error("#} expected")
            if statements > 1 and not hash_flag:
                ## Expected #} after multiple statements code block
                self.error("#} expected")
            elif statements < 1:
                ## Expected at least one statement in code block
                self.error("statement expected")
            self.quads.backPatch(L1, self.quads.nextQuad())
        else:
            del self.quads.quads[L1]
            quadnum -= 1
    
    def condition(self, function, rule):
        bt1 = Rule()
        bt2 = Rule()

        self.bool_term(function, bt1)
        rule.true = bt1.true
        rule.false = bt1.false
        if self.token.unit == "or":
            self.get_Token()
            self.quads.backPatch(rule.false, self.quads.nextQuad())
            self.bool_term(function, bt2)
            rule.false = bt2.false
            #rule.true = self.quads.merge(rule.true, bt2.true)

    def bool_term(self, function, bt):
        bf1 = Rule()
        bf2 = Rule()

        self.bool_factor(function, bf1)
        bt.true = bf1.true
        bt.false = bf1.false
        if self.token.unit == "and":
            self.get_Token()
            self.quads.backPatch(bt.true, self.quads.nextQuad())
            self.bool_factor(function, bf2)
            bt.true = bf1.true
            #bt.false = self.quads.merge(bt.false, bf2.false)

    def bool_factor(self, function, bf):
        e1place = [" "]
        e2place = [" "]
        op = ""
        rule = Rule()

        if self.token.unit == "not":
            self.get_Token()
            self.condition(function, rule)
            bf.true = rule.false
            bf.false = rule.true
        # elif self.token.family in ["digit", "identifier"]:
        #     self.get_Token()
        #     self.condition(function)
        else:
            self.expression(function, e1place)
            if self.token.family == "comparison":
                op = self.token.unit
                self.get_Token()
                self.expression(function, e2place)
                bf.true = self.quads.nextQuad()
                ##FIX THIS L8R
                self.quads.genQuad(op, e1place[0], e2place[0], "_")
                bf.false = self.quads.nextQuad()
                self.quads.genQuad("jump", "_", "_", "_")
            else:
                ## Illegal expression
                print("bad boy")
                self.error("illegal expression")

    def expression(self, function, eplace):
        t1place = [" "]
        t2place = [" "]
        op = ""

        temp = self.optional_sign()
        self.term(function, t1place)
        while True:
            if self.token.unit in ["+", "-"]:
                op = self.token.unit
                self.get_Token()
                self.term(function, t2place)
                w = self.quads.newTemp()
                self.quads.genQuad(op, t1place[0], t2place[0], w)
                t1place[0] = w

                ##Add temp variable entity to scope's entity list
                entity = Temp(w, self.table[-1].offset)
                self.table[-1].offset += 4
                self.table[-1].entitylist[w] = entity
            else:
                break
        if temp:
            pass ##TEMP FIX
        eplace[0] = t1place[0]

    def optional_sign(self):
        if self.token.unit == "-":
            self.get_Token()
            return True
        elif self.token.unit == "+":
            self.get_Token()
            return False
        else:
            return False

    def term(self, function, tplace):
        f1place = [" "]
        f2place = [" "]
        op = ""

        self.factor(function, f1place)
        while True:
            self.get_Token()
            if self.token.unit in ["*", "//", "%"]:
                op = self.token.unit
                self.get_Token()
                self.factor(function, f2place)
                w = self.quads.newTemp()
                self.quads.genQuad(op, f1place[0], f2place[0], w)
                f1place[0] = w

                ##Add temp variable entity to scope's entity list
                entity = Temp(w, self.table[-1].offset)
                self.table[-1].offset += 4
                self.table[-1].entitylist[w] = entity
            else:
                break
        tplace[0] = f1place[0]

    def factor(self, function, fplace):
        eplace = [" "]

        current_token = self.token.unit
        if self.token.family == "digit":
            fplace[0] = current_token
            return
        elif self.token.family == "identifier" and (self.token.unit in function["variables"] or self.token.unit in self.funcs["variables"] or self.token.unit in function["formal params"] or self.token.unit in function["parent variables"]):
            fplace[0] = current_token
            return
        elif self.token.family == "identifier" and self.token.unit in function["functions"]:
            fplace[0] = current_token
            self.quads.genQuad("call", self.token.unit, "_", "_")
            self.get_Token()
            self.func_call(function["functions"][current_token])
        elif self.token.family == "identifier" and self.token.unit in function["parent_functions"]:
            fplace[0] = current_token
            self.quads.genQuad("call", self.token.unit, "_", "_")
            self.get_Token()
            self.func_call(function["parent_functions"][current_token])
        elif self.token.unit == "(":
            self.get_Token()
            self.expression(function, eplace)
            fplace[0] = eplace[0]
            if self.token.unit != ")":
                ## Expected ) after expression
                self.error(") expected")
        else:
            ## Expression syntax error
            self.error("illegal expression")

    def func_call(self, function):
        formal_params = function["formal params"]
        if self.token.unit != "(":
            ## Expected (
            self.error("( expected")
        arguments = len(formal_params)
        self.get_Token()
        for i in range(0, arguments):
            eplace = [" "]
            self.expression(function, eplace)
            self.quads.genQuad("par", eplace[0], "cv", "_")
            if self.token.unit != "," and i < arguments - 1:
                self.error(", expected")
            elif self.token.unit == ",":
                self.get_Token()
            elif self.token.unit == ")" and i < arguments - 1:
                self.error("arguements expected")
            elif self.token.unit == ")":
                break
            else:
                self.error("illegal argument")
            
    def return_call(self, function):
       eplace = [" "]
       self.expression(function, eplace)
       self.quads.genQuad("ret", eplace[0], "_", "_")

    def print_call(self, function):
        eplace = [" "]
        if self.token.unit != "(":
            ## Expected (
            self.error("( expected")
        self.get_Token()
        self.expression(function, eplace)
        self.quads.genQuad("out", eplace[0], "_", "_")
        if self.token.unit != ")":
            ## Expected ) after expression
            self.error(") expected")
        self.get_Token()
#------------------------------------------------------------------------------
class Quad:
    def __init__(self, label, op, arg1, arg2, result):
        self.label = label
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
        self.next = None

    def __str__(self):
        return (str(self.label) + ": " + str(self.op) + ", " + str(self.arg1) + ", " + str(self.arg2) + ", " + str(self.result) + "\n")

class QuadList:
    def __init__(self):
        self.quads = {}
        self.temp = 0

    def nextQuad(self):
        return quadnum

    def genQuad(self, op, arg1, arg2, result):
        global quadnum

        if len(self.quads) > 0:    
            self.quads[quadnum - 1].next = quadnum  
        
        self.quads[quadnum] = Quad(quadnum, op, arg1, arg2, result)
        quadnum += 1

        return self.quads[quadnum - 1]

    def newTemp(self):
        self.temp += 1
        return "T_" + str(self.temp)

    def backPatch(self, quads, result):
        tmp = quads
        while(self.quads[tmp].next != None):
            if self.quads[tmp].result == "_" and (self.quads[tmp].op == "jump" or self.quads[tmp].op in ["<", "<=", "==", ">=", ">", "!="]):
                self.quads[tmp].result = result
            tmp = self.quads[tmp].next

    # def makeList(self, label):
    #     new_list = QuadList()
    #     new_list.quads[label] = None
    #     return new_list

    # def mergeList(self, L1, L2):        
    #     L1.quads.update(L2.quads)

    def __str__(self):
        return '\n'.join([str(self.quads[quad]) for quad in self.quads])
    
class Rule:
    def __init__(self, true=None, false=None):
        self.true = true
        self.false = false
#------------------------------------------------------------------------------
class Entity:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return (str(self.name) + "\n")

class Variable(Entity):
    def __init__(self, name, offset):
        super().__init__(name)
        self.offset = offset
    
    def __str__(self):
        return (str(self.name) + "/" + str(self.offset) + "\n")

class Function(Entity):
    def __init__(self, name, startQuad, framelen):
        super().__init__(name)
        self.startQuad = startQuad
        self.args = []
        self.framelen= framelen
    
    def __str__(self):
        return (str(self.name) + "/" + str(self.startQuad) + "/" + str(self.framelen) + "\n")

class Argument(Entity):
    def __init__(self, name, offset, mode):
        super().__init__(name)
        self.offset = offset
        self.mode = mode

    def __str__(self):
        return (str(self.name) + "/" + str(self.offset) + "/" + str(self.mode) + "\n")

class Temp(Variable):
    def __init__(self, name, offset):
        super().__init__(name, offset)

    def __str__(self):
        return (str(self.name) + "/" + str(self.offset) + "\n")

class Scope:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.entitylist = {}
        self.next = None
        self.offset = 12

    def __str__(self):
        entitylist_str = "\n".join([str(key) + ", " + str(entity) for key, entity in self.entitylist.items()])
        return f"Name: {self.name}, Level: {self.level}, Offset: {self.offset}\nEntities:\n{entitylist_str}\n"
    
    __repr__ = __str__
#------------------------------------------------------------------------------
class Assembler:
    def __init__(self):
        self.framecount = 1
        self.labelcount = 1
        self.mem = []

    def loadvr(self, value, reg, offset):
        if value[0] not in "0123456789":
            self.mem[-1] += "\tlw " + reg + ", " + str(offset) + "(" + value + ")\n"
        else:
            self.mem[-1] += "\tli " + reg + ", " + value + "\n"

    def storerv(self, value, reg, offset):
        if value[0] not in "0123456789":
            self.mem[-1] += "\tsw " + value + str(offset) + "(" + reg + ")\n"

    def gnvlcode(self, var, sym):
        scopelen = 0
        scopenum = 1
        for scope in reversed(sym):
            if var in scope.entitylist.keys() and isinstance(scope.entitylist[var], (Variable, Argument, Temp)):
                if scope.name == "global":
                    self.mem[-1] += "\tlw $t0, " + var + "\n"
                    self.mem[-1] += "\tsw $t0, -" + str(scopelen - scope.entitylist[var].offset + scope.offset) + "($gp)\n"
                    return 0
                scopelen += scope.entitylist[var].offset
                
                self.mem[-1] += "\t" + "lw $t0, -" + str(scopelen) + "($sp)\n"
                return scopelen
            if scopenum > 1:
                scopelen += scope.offset
            scopenum += 1
        return ""
           
    def assemble(self, inter, sym, level, func = False):
        next = self.framecount
        nextlabel = "L"
        labellist = []
        while next <= len(inter.quads):
            if next in labellist:
                self.mem[-1] += "L" + str(next) + ":\n"
                
            if inter.quads[next].op in operators:
                
                arg = self.gnvlcode(inter.quads[next].arg1, sym)
                if(arg != ""):
                    self.loadvr(inter.quads[next].arg1, "$t1", 0)
                elif inter.quads[next].arg1[0] in "0123456789" or inter.quads[next].arg1 == sym[-1].name or isinstance(sym[-1].entitylist[inter.quads[next].arg1], Function):
                    self.loadvr(inter.quads[next].arg1, "$t1", 0)
                else:
                    self.loadvr(inter.quads[next].arg1, "$t1", sym[-1].entitylist[inter.quads[next].arg1].offset)
                
                arg = self.gnvlcode(inter.quads[next].arg2, sym)
                if(arg != ""):
                    self.loadvr(inter.quads[next].arg2, "$t2", 0)
                elif inter.quads[next].arg2[0] in "0123456789" or inter.quads[next].arg2 == sym[-1].name or isinstance(sym[-1].entitylist[inter.quads[next].arg2], Function):
                    self.loadvr(inter.quads[next].arg2, "$t2", 0)
                else:
                    self.loadvr(inter.quads[next].arg2, "$t2", sym[-1].entitylist[inter.quads[next].arg2].offset)
                
                if inter.quads[next].op == "+":
                    self.mem[-1] += "\t" + "add $t3, $t1, $t2\n"
                if inter.quads[next].op == "-":
                    self.mem[-1] += "\t" + "sub $t3, $t1, $t2\n"
                if inter.quads[next].op == "*":
                    self.mem[-1] += "\t" + "mul $t3, $t1, $t2\n"
                if inter.quads[next].op == "//":
                    self.mem[-1] += "\t" + "div $t3, $t1, $t2\n"
                if inter.quads[next].op == "%":
                    ##FIX DIS
                    self.mem[-1] += "\t" + "rem $t3, $t1, $t2\n"

            if inter.quads[next].op in comparison:
                print(inter.quads[next])
                
                arg = self.gnvlcode(inter.quads[next].arg1, sym)
                if(arg != ""):
                    self.loadvr(inter.quads[next].arg1, "$t1", 0)
                elif inter.quads[next].arg1[0] in "0123456789" or inter.quads[next].arg1 == sym[-1].name or isinstance(sym[-1].entitylist[inter.quads[next].arg1], Function):
                    self.loadvr(inter.quads[next].arg1, "$t1", 0)
                else:
                    self.loadvr(inter.quads[next].arg1, "$t1", sym[-1].entitylist[inter.quads[next].arg1].offset)
                
                arg = self.gnvlcode(inter.quads[next].arg2, sym)
                if(arg != ""):
                    self.loadvr(inter.quads[next].arg2, "$t2", 0)
                elif inter.quads[next].arg2[0] in "0123456789" or inter.quads[next].arg2 == sym[-1].name or isinstance(sym[-1].entitylist[inter.quads[next].arg2], Function):
                    self.loadvr(inter.quads[next].arg2, "$t2", 0)
                else:
                    self.loadvr(inter.quads[next].arg2, "$t2", sym[-1].entitylist[inter.quads[next].arg2].offset)
                
                if inter.quads[next].op == "<":
                    self.mem[-1] += "\t" + "blt $t1, $t2, " + str(inter.quads[next].result) + "\n"
                if inter.quads[next].op == "<=":
                    self.mem[-1] += "\t" + "ble $t1, $t2, " + str(inter.quads[next].result) + "\n"
                if inter.quads[next].op == "==":
                    self.mem[-1] += "\t" + "beq $t1, $t2, " + str(inter.quads[next].result) + "\n"
                if inter.quads[next].op == ">=":
                    self.mem[-1] += "\t" + "bge $t1, $t2, " + str(inter.quads[next].result) + "\n"
                if inter.quads[next].op == ">":
                    self.mem[-1] += "\t" + "bgt $t1, $t2, " + str(inter.quads[next].result) + "\n"
                if inter.quads[next].op == "!=":
                    self.mem[-1] += "\t" + "bne $t1, $t2, " + str(inter.quads[next].result) + "\n"    

                nextlabel = "L" + str(inter.quads[next].result)

            if inter.quads[next].op == "=":
                arg = self.gnvlcode(inter.quads[next].result, sym)

                if(arg != ""):
                    self.loadvr(inter.quads[next].result, "$t1", 0)
                elif inter.quads[next].result[0] in "0123456789" or isinstance(sym[-1].entitylist[inter.quads[next].result], Function):
                    self.loadvr(inter.quads[next].result, "$t1", 0)
                    self.storerv(inter.quads[next].arg1, "$t1", 0)
                else:
                    self.loadvr(inter.quads[next].result, "$t1", sym[-1].entitylist[inter.quads[next].result].offset)
                
                if inter.quads[next].arg1[0] in "0123456789" or isinstance(sym[-1].entitylist[inter.quads[next].arg1], Function):
                    self.loadvr(inter.quads[next].arg1, "$t2", 0)
                else:
                    self.loadvr(inter.quads[next].arg1, "$t2", sym[-1].entitylist[inter.quads[next].arg1].offset)
                
                self.mem[-1] += "\t" + "sw $t1, 0($t0)\n"
                
            if inter.quads[next].op == "jump":

                self.mem[-1] += "\t" + "j " + str(inter.quads[next].result) + "\n"
                labellist.append(inter.quads[next].result)
                if nextlabel != "L" and int(nextlabel[1:]) not in labellist:
                    labellist.append(nextlabel[1:])
                    self.mem[-1] += nextlabel + ": \n"
                    nextlabel = "L"
                elif nextlabel in labellist:
                    nextlabel = "L"
                    


            if inter.quads[next].op == "begin_block":
                self.mem.append("")
                self.mem[-1] += str(inter.quads[next].arg1) + ": \n"
                self.mem[-1] += "\t" + "sw $ra, 0($sp)\n"
                self.labelcount += 1

            if inter.quads[next].op == "end_block":
                self.mem[-1] += "\t" + "lw $ra, 0($sp)\n"
                self.mem[-1] += "\t" + "jr $ra\n"

            if inter.quads[next].op == "in":
                self.mem[-1] += "\t" + "li $a7, 5\n"
                self.mem[-1] += "\t" + "ecall\n"
                ##to do more here
            if inter.quads[next].op == "out":
                self.mem[-1] += "\t" + "mv $a0," + "$t0\n"
                self.mem[-1] += "\t" + "li $a7, 1\n"
                self.mem[-1] += "\t" + "ecall\n"

            if inter.quads[next].op == "par":
                self.gnvlcode(inter.quads[next].arg1, sym)
                self.loadvr(inter.quads[next].arg1, "$t1", 0)
            
            if inter.quads[next].op == "call":
                if (inter.quads[next].arg1 == sym[-1].name):
                    self.mem[-1] += "\t" + "addi $s7, $sp, " + str(sym[-1].offset) + "\n"
                elif func == True:
                    self.mem[-1] += "\t" + "addi $sp, $sp, " + str(sym[-2].entitylist[inter.quads[next].arg1].framelen) + "\n"
                else:
                    self.mem[-1] += "\t" + "addi $sp, $sp, " + str(sym[-1].entitylist[inter.quads[next].arg1].framelen) + "\n"
                self.mem[-1] += "\t" + "jal " + str(inter.quads[next].arg1) + "\n"

            if inter.quads[next].op == "ret":
                pass

            self.framecount += 1 
            next += 1
        fin.write(str(self.mem.pop()))


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()