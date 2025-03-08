import click


def file_stats(lines: list[str]) -> tuple[int, int, int]:
    lines_count = len(lines)
    if lines[-1] == "":
        lines_count -= 1
    words_count = sum(len(line.split()) for line in lines)
    bytes_count = sum(len(line.encode('utf-8')) for line in lines) + lines_count
    return lines_count, words_count, bytes_count


def print_file_stats(entries: list[tuple[tuple[int, int, int], str]]):
    col_widths = [0, 0, 0]
    for stats, _ in entries:
        for i, num in enumerate(stats):
            col_widths[i] = max(col_widths[i], len(str(num)))

    for stats, file_name in entries:
        stat_str = [f"{" ":>{4}}{num:>{col_widths[i]}}" for i, num in enumerate(stats)]
        print(" ", end = "")
        print(" ".join(stat_str), end=" ")
        print(file_name)


@click.command()
@click.argument("file_paths", type=click.File("r"), nargs=-1)
def wc(file_paths):
    if len(file_paths) != 0:
        entries = []
        total = (0, 0, 0)
        for fp in file_paths:
            file = fp.read()
            lines = file.split("\n")
            stats = file_stats(lines)
            total = [total[i] + stats[i] for i in range(3)]
            entries.append((stats, fp.name))
        print_file_stats(entries)
        if len(file_paths) > 1:
            print_file_stats([(total, "total")])

    else:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        stats = file_stats(lines)
        print_file_stats([(stats, "")])


if __name__ == "__main__":
    wc()