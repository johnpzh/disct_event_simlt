def test2():
    with open('test.py') as input:
        count = 0
        for line in input:
            count += 1
            print(count, line)

def test():
    for i in range(1, 2):
        print(i)
    pack_list = []
    pack_list.append([])
    a = [1]
    pack_list.extend(a)
    print(pack_list)

    a = [[1, 'b'], [0, 'a']]
    a.sort(key=lambda x:x[0])
    print(a)

    with open('test.py') as input:
        count = 0
        for line in input:
            count += 1
            print(count, line)
            test2()


if __name__ == '__main__':
    test()