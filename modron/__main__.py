"""
A UNIX command-line interface to the modron data cleaning utility.
"""

import sys

import modron


def main(argv=None):
    """
    The main entry point.
    """
    argv = argv or sys.argv[1:]
    if len(argv) == 0:
        print('Usage: modron [http uris]')
        print('The executable will dump schema info to stdout.')
        return 1
    schematizer = modron.Schematizer()
    print(repr(schematizer.schematize_csvs(argv)))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
