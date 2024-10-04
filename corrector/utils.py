def read_report(file_path, LAST_LINE, num_lines):
    """
    Read the next num_lines from a file.

lines <class 'str'> 0,0,94,21,97,36.2,Normal
    :param file_path: path to the file
    :param LAST_LINE: last line read
    :param num_lines: number of lines to read

    :returns: a list of read lines
    """

    with open(file_path) as myfile: # SOL
        lines = myfile.readlines()[LAST_LINE:LAST_LINE+num_lines] # SOL

    return lines # SOL
