#!/usr/bin/python
# Falsish, a False-like interpreter inspired by fish ><>
# Copyright (C) 2022 McChuck
# Released under GNU General Public License
# See LICENSE for more details.
#
# Keyboard and display flushing is done automatically.
# Assembly programming is omitted.
# Lots of other changes implemented, but it will still run native FALSE programs as expected.
# use "python falsish.py filename.fls [-d/-diag]"
# -d/-diag flag will print the internal state at end of program.



import sys
import os

try:
    from getch import getch, getche         # Linux
except ImportError:
    from msvcrt import getch, getche        # Windows

data = [[]]
running = True
variables = [[]]
Variables = []
local_words = [{}]
global_words = {}


def push(item):
    global data
    data[0].insert(0, item)

def pop(deep):
    global data
    if len(data[0]) > 0:
        return data[0].pop(deep)
    else:
        print("\n\nCan't pop that deep (", deep, ") in stack", data[0], flush=True)
        raise IndexError


def parse(mem):
    try:
        global data, running, variables, Variables, local_words, global_words
        end_while = False
        mem = mem + ' '
        char = ''
        in_string = False
        in_lambda = False
        in_char = False
        in_num = False
        in_comment = False
        in_word = False

        for char_index, char in enumerate(mem):
            if in_comment:
                if char == '}':
                    in_comment = False
                continue

            elif in_string:
                if char == '"':
                    print(build_str, end="", flush=True)
                    build_str = ""
                    in_string = False
                else:
                    build_str += char
                continue

            elif in_char:
                push(ord(char))
                in_char = False
                continue

            elif in_lambda:
                build_lambda += char
                if char == ']':
                    lambda_level -= 1
                    if lambda_level == 0:
                        in_lambda = False
                        push(build_lambda)
                        build_lambda = ""
                if char == '[':
                    lambda_level += 1
                continue

            elif in_num:
                if char.isdigit() and ord(char) < 128:
                    build_num *= 10
                    build_num += int(char)
                    continue
                else:
                    in_num = False
                    push(build_num)
                    build_num=0

            elif in_word:
                if char.isspace():
                    in_word = False
                    if build_word[0] == '"' and build_word[-1] == '"':
                        build_word = build_word[1:-1]
                        temp1 = pop(0)
                        if build_word[0].islower():
                            local_words[0].update({build_word:temp1})
                        elif build_word[0].isupper():
                            global_words.update({build_word:temp1})
                        else:
                            print("\n\n>", build_word, "incorrect format.  First character must be a letter.", flush=True)
                            raise ValueError
                    else:
                        if build_word[-1] == '!':       # execute "name!" instead of pushing "name" onto stack
                            if build_word in local_words[0]:
                                action = local_words[0][build_word]
                            elif build_word in global_words:
                                action = global_words[build_word]
                            else:
                                print("\n\nError: defined word", build_word, "not found.", flush=True)
                                raise ValueError
                            if type(action) == str:
                                if action[0] == '[' and action[-1] == ']':
                                    action = action[1:-1]
                            else:
                                action = str(action)
                            end_while = parse(action)
                        else:
                            push(build_word)
                    build_word = ""
                else:
                    build_word += char
                    continue


            if char.isdigit() and ord(char) < 128:
                in_num = True
                build_num = int(char)

            elif char =='<':        # user defined word, create with value/[action] <"name" or <"Name"
                in_word = True
                build_word = ""

            elif char.isalpha() and ord(char) < 128:    #   variables   # Why is Ø a letter?
                push(char)

            elif char == "'":       # next character's ordinal value will be pushed
                in_char = True

            elif char == '?':                         #   IF
                to_exec_true = pop(0)
                condition = pop(0)
                if condition != 0:
                    if to_exec_true[0] == '[' and to_exec_true[-1] == ']':
                        to_exec_true = to_exec_true[1:-1]     # strip off brackets to avoid recursion error
                        end_while = parse(to_exec_true)
                    else:
                        print("\n\nError: ? expected [lambda]: ", to_exec)
                        raise ValueError

            elif char == '¿':                         #   IF ELSE
                to_exec_false = pop(0)
                to_exec_true = pop(0)
                condition = pop(0)
                if condition != 0:
                    if to_exec_true[0] == '[' and to_exec_true[-1] == ']':
                        to_exec_true = to_exec_true[1:-1]     # strip off brackets to avoid recursion error
                        end_while = parse(to_exec_true)
                    else:
                        print("\n\nError: ¿ True expected [lambda]: ", to_exec)
                        raise ValueError
                else:
                    if to_exec_false[0] == '[' and to_exec_false[-1] == ']':
                        to_exec_false = to_exec_false[1:-1]     # strip off brackets to avoid recursion error
                        end_while = parse(to_exec_false)
                    else:
                        print("\n\nError: ¿ False expected [lambda]: ", to_exec)
                        raise ValueError


            elif char == '#':                         #   WHILE
                to_exec = pop(0)
                to_eval = pop(0)
                if to_eval[0] == '[' and to_eval[-1] == ']':
                    to_eval = to_eval[1:-1]
                else:
                    print("\n\nError: # expected lambda: ", to_eval)
                    raise ValueError
                if to_exec[0] == '[' and to_exec[-1] == ']':
                    to_exec = to_exec[1:-1]
                else:
                    print("\n\nError: # expected lambda: ", to_exec)
                    raise ValueError
                end_while = parse(to_eval)
                condition = pop(0)
                while condition != 0:
                    end_while = parse(to_exec)
                    if end_while == True:
                        condition = 0
                        end_while = False
                    else:
                        end_while = parse(to_eval)
                        condition = pop(0)

            elif char == '¶':       #   break out of while loop, not the function
                end_while = True

            elif char == '!':       #   execute
                to_exec = pop(0)
                if to_exec[0] == '[' and to_exec[-1] == ']':
                    to_exec = to_exec[1:-1]
                    end_while = parse(to_exec)
                else:
                    print("\n\nError: ! expected lambda: ", to_exec)
                    raise ValueError

            elif char == ':':        #  store
                to_var = pop(0)
                value = pop(0)
                if len(to_var) == 1:
                    if to_var.islower():
                        index = ord(to_var) - ord('a')
                        variables[0][index] = value
                    elif to_var.isupper():
                        index = ord(to_var) - ord('A')
                        Variables[index] = value
                elif to_var in local_words[0]:
                    local_words[0][to_var] = value
                elif to_var in global_words:
                    global_words[to_var] = value
                else:
                    print("\n\nError: : expected variable: ", to_var)
                    raise ValueError

            elif char == ';':       #   fetch
                from_var = pop(0)
                if len(from_var) == 1:
                    if from_var.islower():
                        index = ord(from_var) - ord('a')
                        push(variables[0][index])
                    elif from_var.isupper():
                        index = ord(from_var) - ord('A')
                        push(Variables[index])
                elif from_var in local_words[0]:
                    push(local_words[0][from_var])
                elif from_var in global_words:
                    push(global_words[from_var])
                else:
                    print("\n\nError: ; expected variable: ", from_var)
                    raise ValueError

            elif char == '"':       #   begin quote to print
                in_string = True
                build_str = ""

            elif char == '[':       #   begin lambda function
                in_lambda = True
                build_lambda = char
                lambda_level = 1

            elif char == '$':       #   DUP     A -> AA
                temp = data[0][0]
                push(temp)

            elif char == '%':       #   DROP    A ->
                pop(0)

            elif char == '\\':       #   SWAP   AB -> BA
                temp = pop(1)
                push(temp)

            elif char == '@':       #   ROT     ABC -> BCA
                temp = pop(2)
                push(temp)

            elif char == 'ø':       # PICK      ABCD2 -> ABCDB      # 0 is top of stack
                deep = pop(0)
                if len(data[0]) > deep:
                    push(data[0][deep])
                else:
                    print("\n\nError: Attempt to pick:", deep, "deeper than stack height", flush=True)
                    raise IndexError

            elif char == '£':       # OVER      ABC -> ABCB
                if len(data[0]) > 1:
                    push(data[0][1])
                else:
                    print("\n\nError: Attempt to over with insufficient stack height", flush=True)
                    raise IndexError

            elif char == '©':       # PUT       ABCDE2 -> ABECD     # 0 is the top of stack after getting the depth and the item
                deep = pop(0)
                temp1 = pop(0)
                if len(data[0]) > deep:
                    data[0].insert(deep, temp1)
                else:
                    print("\n\nError: Attempt to push:", deep, "deeper than stack height", flush=True)
                    raise IndexError

            elif char == '™':       # ROLL       ABCD2 -> ABCDB      # 0 is the top of stack after getting the depth and the item
                deep = pop(0)
                if len(data[0]) > deep:
                    push(pop(deep))
                else:
                    print("\n\nError: Attempt to pop:", deep, " deeper than stack height", flush=True)
                    raise IndexError

            elif char == '‡':       #   clear the stack
                data[0] = []

            elif char == '®':       # reverse the top data stack
                data[0].reverse()

            elif char == '§':       # push the stack depth
                push(len(data[0]))

            elif char == '+':
                temp2 = pop(0)
                temp1 = pop(0)
                push(temp1 + temp2)

            elif char == '-':
                temp2 = pop(0)
                temp1 = pop(0)
                push(temp1 - temp2)

            elif char == '*':
                temp2 = pop(0)
                temp1 = pop(0)
                push(temp1 * temp2)

            elif char == '/':       #   integer division
                temp2 = pop(0)
                temp1 = pop(0)
                if temp2 != 0:
                    push(temp1 // temp2)
                else:
                    print("\n\nError:  Division by zero")
                    raise ValueError

            elif char == '_':       # negate
                temp1 = pop(0)
                push(-temp1)

            elif char == '~':       #   NOT
                temp1 = pop(0)
                push(~temp1)

            elif char == '&':       #   AND
                temp2 = pop(0)
                temp1 = pop(0)
                push(temp1 & temp2)

            elif char == '|':       #   OR
                temp2 = pop(0)
                temp1 = pop(0)
                push(temp1 | temp2)

            elif char == '>':       #   greater than (negate or switch signs for less than)
                temp2 = pop(0)
                temp1 = pop(0)
                if temp1 > temp2:
                   push(-1)         # True
                else:
                    push(0)         # False

            elif char == '=':
                temp2 = pop(0)
                temp1 = pop(0)
                if temp1 == temp2:
                    push(-1)
                else:
                    push(0)

            elif char == '^':       #   read char from keyboard
                temp1 = ord(getche())
                push(temp1)

            elif char == '.':       #   print number
                temp1 = pop(0)
                if isinstance(temp1, int):
                    print(temp1, end="", flush=True)
                else:
                    print("\n\nError: expected number to print:", temp1)
                    raise ValueError

            elif char == ',':       # print char
                temp1 = pop(0)
                if isinstance(temp1, int) and temp1 >= 0:
                    print(chr(temp1), end="", flush=True)
                elif isinstance(temp1, str):
                    print(temp1, end="", flush=True)        #   Prints variable names and lambda functions
                else:
                    print("\n\nError: expected character to print:", temp1)
                    raise ValueError

            elif char == '{':       # begin comment
                in_comment = True

            elif char == '`':       #   BREAK
                return end_while

            elif char == '(':       # create new data stack
                how_many = pop(0)    # move N elements to the new stack
                temp_data = []
                local_words.insert(0, [])
                variables.insert(0, [])
                for i in range(26):
                    variables[0].append(0)
                if how_many > 0:
                    for i in range(how_many):
                        temp1 = pop(0)
                        temp_data.append(temp1)
                        variables[0][how_many - i - 1] = temp1
                data.insert(0, temp_data)

            elif char == ')':       # pop higher data stack
                if len(data) > 1:
                    temp_data = data.pop(0)
                    for temp1 in temp_data:
                        push(temp1)  # save the elements in the lower stack
                else:
                    print("\n\nError:  Can't remove the bottom stack")
                    raise IndexError
                variables.pop(0)
                local_words.pop(0)

            elif char == 'ß':
                print("", end="", flush=True)

            else:
                pass                #   just in case
        # END for

        if in_string:
            print("\n\nError: Incomplete string")
            raise ValueError
        if in_lambda:
            print("\n\nError: Incomplete lambda")
            raise ValueError
        if in_char:
            print("\n\nError: Incomplete character")
            raise ValueError
        if in_num:
            print("\n\nError: Incomplete number")
            raise ValueError
        if in_comment:
            print("\n\nError: Incomplete comment")
            raise ValueError

        return end_while

    except(ValueError):
        excerpt = extract_excerpt(char_index, mem)
        print("\nValue error", char, "@", char_index, "\n", excerpt)
        print("Locals:", variables, "\n>>", local_words, "\nGlobals:", Variables, "\n>>", global_words, "\nStack:", data)
        exit()
    except(IndexError):
        excerpt = extract_excerpt(char_index, mem)
        print("\nIndex error", char, "@", char_index, "\n", excerpt)
        print("Locals:", variables, "\n>>", local_words, "\nGlobals:", Variables, "\n>>", global_words, "\nStack:", data)
        exit()

def extract_excerpt(index, code):
    low = index - 10
    high = index + 10
    if low < 0:
        low = 0
    if high > len(code):
        high = len(code)
    return code[low:high]

def main(args):
    global data, variables, Variables

    print()
    for i in range(26):
        variables[0].append(0)
        Variables.append(0)
    try:
        if len(args) ==1 or len(args) == 2:
            infile_name = args[0]
            mem = ''
            with open(infile_name, "r") as in_file:
                raw = in_file.read()
                in_file.close()
            parse(raw)
            print("\n\nProgram completed")
            if len(args) == 2 and (args[1] == "-d" or args[1] == "-diag"):
                print("Locals:", variables, "\n>>", local_words, "\nGlobals:", Variables, "\n>>", global_words, "\nStack:", data)
        else:
            print("usage: python false.py infile.f\n")
    except FileNotFoundError:
        print("< *Peter_Lorre* >\nYou eediot!  What were you theenking?\nTry it again, but thees time with a valid file name!\n</ *Peter_Lorre* >\n")
        print("usage: python false.py infile.f\n")
    except(ValueError, IndexError):
                print("I just don't know what went wrong!\n")
                in_file.close()


if __name__ == '__main__':
    main(sys.argv[1:])
