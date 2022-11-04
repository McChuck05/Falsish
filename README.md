# Falsish
A False variant inspired by fish >&lt;>

Copyright (C) 2022 McChuck

Released under GNU General Public License

See LICENSE for more details.

This is a False-like language, with an interpreter written in Python.

* The pick character has been replaced with '>', which was unused.
* Keyboard and display flushing is done automatically.
* Assembly programming is omitted.
* ',' will print a number as a character.  It will also print variable names and lambda functions.
* '`' is used as a break.  It will halt the current lambda function level.
* Lowercase letters (a..z) are local variables.
* Uppercase letters (A..Z) are global variables.
* '(' and ')' create and drop a new data stack and local variable array.  Inspired by the fish ><> esolang.
*   N '(' moves the top N elements of the stack to the new stack being created.  It also creates a new local (lowercase) variable array.
*   ')' closes the higher level stack and moves and stack elements back onto the next lower level.  It also removes the higher local (lowercase) variable array.
*   '®' reverses the elements of the top data stack.  Find it online and copy it.  U+00AE

For more information of Falsish, see:
* https://esolangs.org/wiki/Falsish

For more information on False, see:
* https://esolangs.org/wiki/FALSE
* https://strlen.com/false-language/
