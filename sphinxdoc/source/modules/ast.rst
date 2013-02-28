:mod:`tayra.ast` -- Abstract syntax tree
=========================================

.. automodule:: tayra.ast

Module contents
---------------

.. autoclass:: Node
    :members: parent, parser, children, validate, headpass1, headpass2,
        generate, tailpass, lstrip, rstrip, dump, show, getroot, bubbleup,
        bubbleupaccum
    :show-inheritance:

.. autoclass:: Terminal
    :members: terminal, lineno, lstrip, rstrip, generate, dump, show
    :show-inheritance:

.. autoclass:: NonTerminal
    :members: _terms, _nonterms, lstrip, rstrip, gencontrolblock, genfunction,
        flatten
    :show-inheritance:
