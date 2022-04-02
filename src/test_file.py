from parser import BinaryFile


def test_file():
    with BinaryFile("test_file.txt", "w") as file:
        file.write("Hello World!\n")
        file.write("olleH\n")
        file.write("!dlroW\n")

    with BinaryFile("test_file.txt", "r") as file:
        assert(file.readline() == "Hello World!\n")
        assert(file.read(6) == "olleH\n")
        file.move_cursor_left(6)
        assert(file.read(6) == "olleH\n")
        file.move_cursor_right(7)
        assert(not file.read(1))


if __name__ == '__main__':
    test_file()
