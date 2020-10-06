<!-- from here: https://dbader.org/blog/write-a-great-readme-for-your-github-project -->

# Miditapyr
> MIDI TAbulation in PYthon (and for R)

**Work in progress!**

This python package can be used to read in midi files (via [mido](https://github.com/mido/mido)) in dataframes. These dataframes
can then also be read in in R via the package pyramidi. The dataframes then can be easily modified and visualized. Finally they can be written back to midi files via mido.

![](header.png)

## Installation

```sh
pip install miditapyr
```

## Usage example

A usage example is shown in a [jupyter notebook in this repo](https://nbviewer.jupyter.org/github/urswilke/miditapyr/blob/master/notebooks/pyramidi_integration.ipynb)
<!-- A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._ -->

<!-- ## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
``` -->

## Release History

<!-- * 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()` -->
* 0.0.1
    * Work in progress

## Meta

[Urs Wilke](https://twitter.com/UrsWilke)

Distributed under the MIT license. See [``LICENSE``](https://github.com/urswilke/miditapyr/blob/master/LICENSE) for more information.

## Contributing

1. Fork it (<https://github.com/UrsWilke/miditapyr/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'commit message text for fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
<!-- [npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki -->
