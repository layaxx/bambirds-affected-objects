from object import object
from parser import parser


def load_objects_from_file(path):
    with open(path) as f:
        string = f.read()

    return load_objects_from_string(string)


def load_objects_from_string(string):
    lines = string.splitlines()
    filtered_lines = list(filter(lambda line: line.startswith("shape"), lines))

    parsed_facts = parser.parseString("\n".join(filtered_lines)).get("fact")
    shapes = filter(lambda f: f[0] == "shape", parsed_facts)

    return list(map(lambda shape: object(shape), shapes))
