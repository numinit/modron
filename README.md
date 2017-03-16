# [modron](https://www.dandwiki.com/wiki/Modron_\(5e_Race\))

A Python being of routine and perfect order using Pandas to clean CSVs.

## Compatibility

`modron` works with Python 3.5+.

## Hacking

Clone the repository, and be sure that you have a python3 version of virtualenv
installed. Then, assuming you cloned to `modron`, run `virtualenv modron`. cd
to the directory, and `source bin/activate`.

To install dependencies, _with the virtualenv activated_, run
`python setup.py develop`. pandas and its dependencies take a while to
compile, grab a coffee.

## Contributing

Changes _must_ be unit tested, style checked, and linted.

* To unit test: `python setup.py test`
* To style check: `python setup.py style`
* To lint: `python setup.py lint`