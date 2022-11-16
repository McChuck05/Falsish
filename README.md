# Falsish
A FALSE variant inspired by fish >&lt;>

Copyright (C) 2022 McChuck.  Released under GNU General Public License.  See LICENSE for more details.

Use: python falsish.py filename.fls [-d/-diag]  {allows diagnostic display of state when program ends}

Falsish is a superset of FALSE.  The following is a partial list of changes.  Read "Falsish commands.txt" to see the full command list.  Note that, with the exception of the ` (68k assembly) command, existing FALSE programs will run in Falsish.

* Input and output flushing is automatic.
* Assembly functionality is omitted.
* The '`' (back quote) character indicates an alternate action for the following character.  ` followed by whitespace is a break. `` is a halt.
* ',' in addition to printing a number as a character, will also print a variable name or lambda function.
* Lowercase letters are local variables, specific to a data stack.
* Uppercase letters are global variables.
* You add a stack by using 'N(', where N is the number of items from the current stack to populate onto the new stack.  This will also copy each of the new stack elements into a new set of local variables, starting with a, which gets the lowest element' value.
* You close a stack by using ')', which moves the remaining items onto the lower stack and deletes its associated local variables.
* '¶' breaks from most recent while loop (but not the current lambda function).
* Useful (sort of) error messages are introduced.
* You can create your own variables with: value <"name"     *MUST* end in whitespace!  MUST begin with a letter!
>     If the first letter is uppercase, the variable is global.  If lowercase, local.
>     To use: <name :   or:    <Name ;    like any single letter variable.
>     If the name ends in '!', it will execute instead of having its name pushed to the stack.
* And several more.

The addition of stack reversal, creation, and deletion, each stack having its own local variables, and string manipulation greatly enhances the expressive power of the base FALSE language.

For more information of Falsish, see:
* https://esolangs.org/wiki/Falsish

For more information on False, see:
* https://esolangs.org/wiki/FALSE
* https://strlen.com/false-language/
