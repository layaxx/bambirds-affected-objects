# Determine which objects have moved between two situations

Tested with Python 3.8.18

Install requirements as documented in requirements.txt.

Run main.py with one ore two arguments:

- arg0: path to first situation file (before shot);                     *required*
- -s, --situation-after: path to second situation file (after shot):    *defaults to consecutive situation file*
- -b, --bambirds: path of bambirds folder, relative to this folder:     *defaults to ../bambirds*
- -d, --debug: (boolean) display output of pdf generation in stout, otherwise might silently fail:     *defaults to False*

IDs of Objects that have moved/disappeared from situation1 to situation2 are displayed in the console. Additionally, two PDFs are generated, one including only objects that have moved and one only including objects that haven't. This relies on the presence of the prolog files from the bambirds project. 


Sample usage:

```bash
py main.py ./data/situation1-1.pl -s ./data/situation1-2.pl

OR

py main.py ./data/situation1-1.pl
```

## Manually draw PDF Output
```bash
swipl -s [PATH/TO/BAMBIRDS]/planner/main.pl draw.pl -- [PATH/TO/SITUATION/FILE]
```

## Highlighting of moved objects
The thirds PDF contains all objects, with objects that have moved highlighted in yellow and objects that were destroyed highlighted in red. This does not apply to birds, which keep their color regardless of status.

## Demo
For a demo, see the [Demo Folder](./demo).

## About differentiating between moved/destroyed objects
This is currently somewhat unstable. 
In particular, it cannot be safely determined which object has moved and which was destroyed if several similar blocks (same material, same shape and similar size) changed. 
Additionally, this currently assumes objects that change their shape to have been removed, even if this might not be correct. 
For example, from situation1-1 to situation1-2, one of the ice blocks is hit and changes shape. 
It is therefore considered destroyed, even if it remains on stage.
