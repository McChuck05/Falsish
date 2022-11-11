# Falsish
A FALSE variant inspired by fish >&lt;>

Copyright (C) 2022 McChuck.  Released under GNU General Public License.  See LICENSE for more details.

Falsish is a superset of FALSE with the following changes:

* Input and output flushing is automatic.
* Assembly functionality is omitted.
* The '`' (back quote) character executes a break, exiting out of a lambda function or the program.
* ',' in addition to printing a number as a character, will also print a variable name or lambda function.
* Lowercase letters are local variables, specific to a data stack.
* Uppercase letters are global variables.
* You add a stack by using 'N(', where N is the number of items from the current stack to populate onto the new stack.  This will also copy each of the new stack elements into the local variables, starting with a.
* You close a stack by using ')', which moves the remaining items onto the lower stack.
* '®' reverses the current stack, effectively making it a deque.
* '©' pushes the top element of the stack N elements in. Sort of the opposite of 'Ø'. Example: 1 2 3 4 5 a 2 < --> 1 2 3 a 4 5
* '™' pops an element N deep in the stack, like a destructive 'ø'. Example: 1 2 3 4 5 3 --> 1 3 4 5 2
* '£' copies the second element to the top of the stack.  Exampke: 1 2 3 --> 1 2 3 2
* '‡' clears the current stack.
* '¿' if else
* Useful (sort of) error messages are introduced.
* Note that, with the exception of the ` assembly command, existing FALSE programs will run in Falsish.

Falsish, although completely functional, is still a work in progress.  With the addition of the stack reversal function, Falsish is a Turing complete language.  A reversible stack is a deque, or conceptually two separate stacks with shared elements.

For more information of Falsish, see:
* https://esolangs.org/wiki/Falsish

For more information on False, see:
* https://esolangs.org/wiki/FALSE
* https://strlen.com/false-language/
