<!-- template from here: https://dbader.org/blog/write-a-great-readme-for-your-github-project -->

# Miditapyr <a href='https://miditapyr.readthedocs.io/'><img src='https://github.com/urswilke/miditapyr/raw/master/docs/source/hex-miditapyr.png' align="right" height="160" /></a>
> MIDI TAbulation in PYthon (and for R)


[![PyPI version](https://badge.fury.io/py/miditapyr.svg)](https://pypi.org/project/miditapyr/)
[![codecov](https://img.shields.io/codecov/c/github/urswilke/miditapyr/master.svg?style=flat-square&label=Codecov+Coverage)](https://codecov.io/gh/urswilke/miditapyr)
[![Documentation Status](https://readthedocs.org/projects/miditapyr/badge/?version=latest)](https://miditapyr.readthedocs.io/en/latest/?badge=latest)
![gh actions tests](https://github.com/urswilke/miditapyr/actions/workflows/ci.yml/badge.svg)
[![Lifecycle: experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)

**Work in progress!**

This python package can be used to read in midi files (via
[mido](https://github.com/mido/mido)) in dataframes. These dataframes can then
also be read in in R via the package
[pyramidi](https://github.com/urswilke/pyramidi). The dataframes then can be
easily modified and visualized. Finally they can be written back to midi files
via mido.

![](header.png)

## Installation

```sh
pip install miditapyr
```

If you are an R user check out the related R package [pyramidi](https://github.com/urswilke/pyramidi).


## Documentation

Documentation can be found [here](https://miditapyr.readthedocs.io/)

## Usage 

miditapyr provides a `MidiFrame` class. A [jupyter notebook how to use this class](https://miditapyr.readthedocs.io/en/latest/notebooks/midi_frame_usage.html) is shown in the documentation.

The low-level functions which this class uses are demonstrated in a notebook for [functions usage](https://miditapyr.readthedocs.io/en/latest/notebooks/functions_usage.html). 

These notebooks can also be downloaded [from the repo](https://github.com/urswilke/miditapyr/blob/master/docs/source/notebooks/).


## Release History

Please find the changelog here: [CHANGELOG.md](https://github.com/urswilke/miditapyr/blob/master/CHANGELOG.md)

## License

Distributed under the MIT license. See [``LICENSE``](https://github.com/urswilke/miditapyr/blob/master/LICENSE) for more information.

## Contributing

1. Fork it (<https://github.com/UrsWilke/miditapyr/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'commit message text for fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

