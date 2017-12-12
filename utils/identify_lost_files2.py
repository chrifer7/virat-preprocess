import sys
import os

fname = 'annotation_files_list.txt'

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('Falta la ruta de los archivos')
        sys.exit(2)
    else:
        with open(fname) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        lost_files = []
        for file_name in content:
            file_path = os.path.join(sys.argv[1], file_name)
            print('Exist?: ' + file_name + ' - ' + str(os.path.isfile(file_path)))
            if not (os.path.isfile(file_path)):
                lost_files.append(file_name)

        with open("out.txt", "w") as output:
            output.write('\n'.join(lost_files))
