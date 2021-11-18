Introduction
============

**miditapyr - MIDI TAbulation in PYthon and for R**

This python package can be used to read in midi files (via
`mido <https://github.com/mido/mido>`_) in dataframes of different formats.  And to write these back to
midi files with mido.

Motivation
**********

These dataframes can then
also be read in in R via the package
`pyramidi <https://github.com/urswilke/pyramidi>`_.

Then they can be modified (using pandas / R dataframe methods) and visualized (using for instance altair / ggplot2).

Limitations
***********

Midi files come in various formats. Miditapyr does not work for all files yet.
