Introduction
============

This python package can be used to read in midi files (via
`mido <https://github.com/mido/mido>`_) in dataframes.  And to write these back to
midi files via mido.

Motivation
**********

These dataframes can then
also be read in in R via the package
`pyramidi <https://github.com/urswilke/pyramidi>`_.

Then they can be easily modified (using pandas / R dataframe methods) and visualized (using for instance altair / ggplot2).

Limitations
***********

Midi files come in various formats. Miditapyr does not work for all files.
