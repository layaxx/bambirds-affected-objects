# Determine which objects have moved between two situations

Tested with Python 3.8.18

Install requirements as documented in requirements.txt.

Run main.py with one ore two arguments:

- arg0: path to first situation file (before shot);     required
- arg1: path to second situation file (after shot):     optional
  - if not provided, program looks for the consecutive situation file

IDs of Objects that have moved/disappeared from situation1 to situation2 are displayed in teh console. Additionally, two PDFs are generated, one including only objects that have moved and one only including objects that haven't. This relies on the presence of the prolog files from the bambirds project. The code currently assumes that this folder and the bambirds folder share the same parent folder.


Sample usage:

```bash
py main.py ./data/situation1-1.pl -s ./data/situation1-2.pl

OR

py main.py ./data/situation1-1.pl
```

## Draw PDF Output
```bash
swipl -s [PATH/TO/BAMBIRDS]/planner/main.pl draw.pl -- [PATH/TO/SITUATION/FILE]
```