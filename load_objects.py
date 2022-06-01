from object import object
from parser import parser


def load_objects_from_file(path):
    with open(path) as f:
        string = f.read()

    return load_objects_from_string(string)


def load_objects_from_string(string):
    lines = string.splitlines()
    filtered_lines = list(filter(lambda line: line.startswith("shape"), lines))

    shapes = parser.parseString("\n".join(filtered_lines)).get("fact")

    return list(map(lambda shape: object(shape), shapes))
