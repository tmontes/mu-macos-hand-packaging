#!/usr/bin/env python3

FILENAME = './bin/mu-editor'

FIRST_TWO_LINES = """
#!/bin/sh                                                                                 
"exec" "`dirname $0`/python3.7" "$0" "$@"
""".lstrip()

with open(FILENAME, 'rt') as f:
    REMAINING_LINES = ''.join(
        f.readlines()[2:]
    )

with open(FILENAME, 'wt') as f:
    f.write(FIRST_TWO_LINES)
    f.write(REMAINING_LINES)
