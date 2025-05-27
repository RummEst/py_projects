

def remove_empty_lines(fname):
    with open(fname, 'r') as file:
        lines = file.readlines()

    non_empty_lines = [line for line in lines if line.strip() != ""]

    with open(fname, 'w') as file:
        file.writelines(non_empty_lines)


# Specify the fname
fname = 'toStrip.txt'
remove_empty_lines(fname)
