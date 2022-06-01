from parser import parser
import os
import subprocess


def update_material(line, have_moved_ids, were_destroyed_ids):
    if line.startswith("hasMaterial"):
        id = get_id(line)
        if id in have_moved_ids:
            return f"hasMaterial({get_id(line)}, yellow, 1, 2, 3, 4)."
        if id in were_destroyed_ids:
            return f"hasMaterial({get_id(line)}, red, 1, 2, 3, 4)."
    return line


def handle_output(situation_path, have_moved, were_destroyed, have_not_moved, path_to_bambirds, debug):
    with open(situation_path) as f:
        string = f.read()

    lines = string.splitlines()

    shape_lines = [line for line in lines if line.startswith("shape")]
    non_shape_lines = [line for line in lines if not line.startswith("shape")]

    have_moved_ids = [obj.id for obj in have_moved]
    have_not_moved_ids = [obj.id for obj in have_not_moved]
    were_destroyed_ids = [obj.id for obj in were_destroyed]

    # only useful for PDF output
    complete = [update_material(line,
                                have_moved_ids,
                                were_destroyed_ids) for line in lines]

    lines_have_moved = list(filter(lambda line: get_id(
        line) in have_moved_ids, shape_lines))
    lines_have_not_moved = list(filter(lambda line: get_id(
        line) in have_not_moved_ids, shape_lines))

    if not os.path.exists('./output'):
        os.makedirs('./output')

    write_file_curried = (lambda lines1, lines2, postfix: write_single_file(
        situation_path, lines1, lines2, postfix, path_to_bambirds, debug))

    write_file_curried(non_shape_lines, lines_have_moved, "has-moved")
    write_file_curried(non_shape_lines, lines_have_not_moved, "has-not-moved")
    write_file_curried(complete, [], "combined")


def write_single_file(situation_path, non_shape_lines, specific_lines, postfix, path_to_bambirds, debug):

    file_name = os.path.basename(situation_path)
    file = os.path.splitext(file_name)[0]

    content = build_content(non_shape_lines, specific_lines, file, postfix)
    filename = os.path.join(
        "./output/", file + "-" + postfix + ".pl")

    with open(filename, "w") as f:
        print('writing: ' + filename)
        f.write(content)
    try:
        subprocess.run(
            "swipl -s {}/planner/main.pl draw.pl -- {}".format(
                path_to_bambirds, filename),
            shell=True,
            stdout=None if debug else subprocess.DEVNULL,
            stderr=None if debug else subprocess.DEVNULL)
    except:
        print("Failed to produce PDF Output.")


def build_content(non_shape_lines, shape_lines, file, postfix):
    return "\n".join(
        [line for line in non_shape_lines if not line.startswith(
            "situation_name(")]) \
        + "\nsituation_name('{}-{}').\n".format(file, postfix) \
        + "\n".join(shape_lines)


# returns the first argument in a Prolog fact, which usually is the id.
def get_id(line):
    return parser.parseString(line).get("fact")[0][1]
