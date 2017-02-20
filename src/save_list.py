'''Write the list to a file.'''

def save_list(l, file, opt):
    with open(file, opt) as output:
        x = [str(v) for v in l]
        line = ' '.join(x) + '\n'
        output.write(line)