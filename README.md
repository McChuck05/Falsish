# Falsish
A False variant inspired by fish >&lt;>

Copyright (C) 2022 McChuck

Released under GNU General Public License

See LICENSE for more details.

Falsish is a superset of FALSE with the following changes:

* Input and output flushing is automatic.
* Assembly functionality is omitted.
* The '`' (back quote) character executes a break, exiting out of a lambda function or the program.
* ',' in addition to printing a number as a character, will also print a variable name or lambda function.
* Lowercase letters are local variables, specific to a data stack.
* Uppercase letters are global variables.
* You add a stack by using 'N(', where N is the number of items from the current stack to populate onto the new stack.
* You close a stack by using ')', which moves the remaining items onto the lower stack.
* '®' reverses the current stack, effectively making it a deque or two stacks.
* '©' pushes the top element of the stack N elements in. Sort of the opposite of 'ø'. Example: 1 2 3 4 5 a 2 < --> 1 2 3 a 4 5
* '™' pops an element N deep in the stack, like a destructive 'ø'. Example: 1 2 3 4 5 3 --> 1 3 4 5 2
* '‡' clears the current stack.
* Useful (sort of) error messages are introduced.
* Note that, with the exception of the ` assembly command, existing FALSE programs will run in Falsish.

Falsish, although completely functional, is still a work in progress.

For more information of Falsish, see:
* https://esolangs.org/wiki/Falsish

For more information on False, see:
* https://esolangs.org/wiki/FALSE
* https://strlen.com/false-language/
