==========
RstTable
==========

format data to reStructedText Table

Support
=======
+   support all Data type
+   fix width for MultiByte character, such as CJK
+   add "encoding" for Non-Unicode string

Usage
=====
::

    data = [['a', 'b', 'c'], ['e', 'f', 'g']]
    t = RstTable(data)
    print(t.table())

    data = [['a', 'b', 'c'], [1, 2, 3]]
    t = RstTable(data)
    print(t.table())

    +===+===+===+
    | a | b | c |
    +===+===+===+
    | 1 | 2 | 3 |
    +---+---+---+
