# Demo

Running `py main.py ./data/situation1-2.pl` from the project root should result in the following three PDF files being generated and displayed:
1. [./situation1-2-combined.pdf](./situation1-2-combined.pdf)
2. [./situation1-2-has-changed.pdf](./situation1-2-has-changed.pdf)
2. [./situation1-2-has-not-changed.pdf](./situation1-2-has-not-changed.pdf)

The first file contains all objects, with those that have moved/were destroyed between situation1-2 and situation1-3 highlighted in yellow/red.

The second file contains only objects that have changed, while the third file contains all unchanged objects.