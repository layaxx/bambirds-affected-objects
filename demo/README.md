# Demo

Running `py main.py ./data/situation15-1.pl` from the project root should result in the following three PDF files being generated and displayed:
1. [./situation15-1.pdf](./situation15-1.pdf)
2. [./situation15-1-has-changed.pdf](./situation15-1-has-changed.pdf)
2. [./situation15-1-has-not-changed.pdf](./situation15-1-has-not-changed.pdf)

The first file contains all objects, with those that have moved/were destroyed between situation15-1 and situation15-2 highlighted in yellow/red.

The second file contains only objects that have changed, while the third file contains all unchanged objects.
