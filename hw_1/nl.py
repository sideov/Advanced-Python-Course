import click


@click.command()
@click.argument("file_path", type=click.File("r"), required=False)
def nl(file_path: click.File("r")):
    if file_path is not None:
        file = file_path.read()
        lines = file.split("\n")
        if lines[-1] == "":
            lines.pop()

        for i, line in enumerate(lines):
            print(f"      {i + 1}  {line}")
    else:
        line_idx = 0
        while True:
            try:
                line = input()
                line_idx += 1
                print(f"     {line_idx}  {line}")
            except EOFError:
                break

if __name__ == "__main__":
    nl()
