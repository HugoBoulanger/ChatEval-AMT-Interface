import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', type=str)
    parser.add_argument('file2', type=str)
    parser.add_argument('file3', type=str)
    args = parser.parse_args()

    f = open(args.file1, 'r')
    f1 = f.readlines()
    f.close()

    f = open(args.file2, 'r')
    f2 = f.readlines()[1:]
    f.close()

    f = open(args.file3, 'w')
    f.writelines(f1 + f2)
    f.close()