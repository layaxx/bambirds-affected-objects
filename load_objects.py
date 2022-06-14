from object import object
from parser import parser


def load_objects_from_file(path):
    with open(path) as f:
        string = f.read()

    return load_objects_from_string(string)


def load_objects_from_string(string):
    lines = string.splitlines()
    shape_lines = list(
        filter(lambda line: line.startswith("shape"), lines))
    material_lines = list(
        filter(lambda line: line.startswith("hasMaterial"), lines))

    shapes = parser.parseString("\n".join(shape_lines)).get("fact")

    objects = list(map(lambda shape: object(shape), shapes))

    return (objects, material_lines + shape_lines)


def get_id(fact):
    return fact[1]
