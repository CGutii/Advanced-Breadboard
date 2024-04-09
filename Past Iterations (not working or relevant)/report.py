def print_file_contents(filepath):
    try:
        with open('report.txt', 'r') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f"File not found: {'report.txt'}")

if __name__ == "__main__":
    file_name = "report.txt"
    print_file_contents(file_name)
