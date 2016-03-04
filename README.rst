==========
RstTable
==========

format data to reStructedText Table

.. note::

    all inputed data must be unicode string.

Usage
=====
::

    data = [['a', 'b', 'c'], ['e', 'f', 'g']]
    t = RstTable(data)
    print(t.table)
