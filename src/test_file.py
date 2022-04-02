import os
from parser import BinaryFile


test_file_name = "test_file.txt"


def test_file():
    with BinaryFile(test_file_name, "wb") as file:
        file.write("Hello World!\n")
        file.write("olleH\n")
        file.write("!dlroW\n")

    with BinaryFile(test_file_name, "r") as file:
        assert(file.readline() == "Hello World!\n")
        assert(file.read(6) == "olleH\n")
        file.move_cursor_left(6)
        assert(file.read(6) == "olleH\n")
        file.move_cursor_right(7)
        assert(not file.read(1))


def cleanup():
    os.system(f"rm {test_file_name}")


if __name__ == '__main__':
    test_file()
    cleanup()
