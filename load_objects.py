from object import object
from parser import parser

test = """shape(pig0,ball, 414,331.5,143,[6.75]).
shape(pig1,ball, 414.5,368.5,132,[65]).
shape(pig2,ball, 532.5,326.5,380,[11]).
shape(pig3,ball, 652.5,275,143,[675]).
protects(struct2,pig2)."""


test2 = """shape(pig1,ball, 414.5,368.5,132,[65]).
shape(pig2,ball, 532.5,326.5,380,[11]).
shape(pig3,ball, 652.5,275,143,[675]).
protects(struct2,pig2)."""

all_objects = (
    list(map(lambda shape: object(shape),
             filter(
        lambda f: f[0] == "shape", parser.parseString(test).get("fact")))),
    list(map(lambda shape: object(shape),
             filter(
        lambda f: f[0] == "shape", parser.parseString(test2).get("fact")))))

has_not_moved = []
has_moved = []


for o in all_objects[0]:
    if o in all_objects[1]:
        # if second set has an object that is similar enough,
        # we assume it was not affected
        has_not_moved.append(o)
    else:
        has_moved.append(o)


print("{} objects ha(s/ve) moved, {} ha(s/ve) not.".format(
    len(has_moved), len(has_not_moved)))

for o in has_moved:
    print(o.id)
