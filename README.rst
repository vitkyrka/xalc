.. -*- rst -*-

Xalc
====

Xalc is a hexadecimal calculator for embedded systems programmers, implemented
as a pre-processor for Python expressions, with a console interface based on
IPython.

Features:

- Mixed calculations with hex, decimal, binary and binary prefix literals
- Support for undecorated hex literals.  Ambiguous literals can be forced to hex by either prefixing or suffixing with 'x'.
- Display in hex, decimal, 32-bit binary (with bit position ruler) and binary prefixes (sizes)
- Simple bit mask construction
- Bit field extraction operator
- Highlighting of changed nibbles/bits
- From IPython: Support for arbitrary Python expressions (minus the ones that conflict with the pre-processed syntax), command history, access to previous results with _* variables, etc.

The following "screenshot" demonstrates some of the features of Xalc.  The real
program displays the different bases in different colors and highlights changed
bits and nibbles with underlines, if your console supports that::

 $ xalc
 In [1]: deadbeef
 0xdeadbeef
 Out[1]:
 3735928559    │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
 0xdeadbeef    │  1101 1110 1010 1101 1011 1110 1110 1111
 3 Gi + 490 Mi + 879 Ki + 751

 In [2]: deadbeef $ m5t13
 0xdeadbeef >> 5 & ((0x3fe0) >> 5)
 Out[2]:
  503           │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
  0x000001f7    │  0000 0000 0000 0000 0000 0001 1111 0111

 In [3]: _ ^ cafe
 _ ^ 0xcafe
 Out[3]:
  51977         │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
  0x0000cb09    │  0000 0000 0000 0000 1100 1011 0000 1001
  50 Ki + 777

 In [4]: 7f000000 - 35000000x
 0x7f000000 - 0x35000000
 Out[4]:
  1241513984    │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
  0x4a000000    │  0100 1010 0000 0000 0000 0000 0000 0000
  1 Gi + 160 Mi

 In [5]: m2@0_5_8t9_29_31t31
 (0x3|0x20|0x300|0x20000000|0x80000000)
 Out[5]:
  2684355363    │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
  0xa0000323    │  1010 0000 0000 0000 0000 0011 0010 0011
  2 Gi + 512 Mi + 803

 In [6]: 2g | m12
 0x80000000 | (0x1000)
 Out[6]:
  2147487744    │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
  0x80001000    │  1000 0000 0000 0000 0001 0000 0000 0000
  2 Gi + 4 Ki

 In [7]: -45
 -45
 Out[7]:
  -45           │  28─╮ 24─╮ 20─╮ 16─╮ 12─╮  8─╮  4─╮  0─╮
  0xffffffd3    │  1111 1111 1111 1111 1111 1111 1101 0011

Install with pip::

    pip install --upgrade xalc

Or by cloning the `git repo <https://github.com/rabinv/xalc>`_ and running::

    python setup.py install

Run ``xalc`` after installation.
