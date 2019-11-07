import sys


def parse_var_line(line):
    tokens = line.split(";")
    var_str = tokens[0].strip()
    comment_str = tokens[1].strip()

    tokens = var_str.split(",")
    name = tokens[2]

    tokens = comment_str.strip("!- ").split("[")
    comment = tokens[0].strip()
    unit = tokens[1].split("]")[0].strip()

    return {"name": name, "comment": comment, "unit": unit}


def parse_file(f_path):
    v = []

    with open(f_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] == "!":
                continue
            v.append(parse_var_line(line))

    return v


def mine_rdd(f_path_1, f_path_2, name):
    v_1 = parse_file(f_path_1)
    v_2 = parse_file(f_path_2)

    v_1 = sorted(v_1, key=lambda i: (i["name"]))
    v_2 = sorted(v_2, key=lambda i: (i["name"]))

    with open('RDDMissing_{}.csv'.format(name), 'w+') as f_missing, open('RDDBoth_{}.csv'.format(name), 'w+') as f_both:
        for d in v_1:
            if d not in v_2:
                f_missing.write("{},{},{},{},{},{}\n".format(d["name"], d["comment"], d["unit"], "", "", ""))
            else:
                f_both.write("{},{},{}\n".format(d["name"], d["comment"], d["unit"]))

        for d in v_2:
            if d not in v_1:
                f_missing.write("{},{},{},{},{},{}\n".format("", "", "", d["name"], d["comment"], d["unit"]))


if __name__ == "__main__":
    mine_rdd(sys.argv[1], sys.argv[2], sys.argv[3])
