import click


@click.command()
@click.argument("file_paths", type=click.File("r"), nargs=-1)
def tail(file_paths):
    if len(file_paths) != 0:
        with_file_name = len(file_paths) > 1
        for i, file_path in enumerate(file_paths):
            file = file_path.read()
            lines = file.split("\n")
            if lines[-1] == "":
                lines.pop()
            if with_file_name:
                print(f"==> {file_path.name} <==")
            if len(lines) > 10:
                lines = lines[-10:]
            for line in lines:
                print(line)
            if i != len(file_paths) - 1:
                print()

    else:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break

        if len(lines) > 17:
            lines = lines[-17:]
        for line in lines:
            print(line)

if __name__ == '__main__':
    tail()
