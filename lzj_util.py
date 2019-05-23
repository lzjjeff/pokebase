

def read_file_to_str(file_path, mode="r+", encoding="utf-8"):
    str = ""
    with open(file_path, mode, encoding=encoding) as fi:
        if fi.readable():
            str += fi.read()
            fi.close()
            return str
        else:
            print("==== error: unreadable ====")
            exit(0)


def output_str_to_file(str, file_path, mode="w+", encoding="utf-8"):
    with open(file_path, mode, encoding=encoding) as fo:
        if fo.writable():
            fo.write(str)
        else:
            print("==== error: unwritable ====")
            exit(0)


