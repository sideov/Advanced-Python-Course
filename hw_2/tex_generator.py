

def make_rows(data: list[list[str]]) -> str:
    match data:
        case []: return "\t"
        case [header]: return make_row_with_splitter_recursive(header, " & ") + " \\\\"
        case [header, *rows]:
            return make_row_with_splitter_recursive(
                header, " & ") + " \\\\\n" + make_rows(rows)


def make_row_with_splitter_recursive(data: list[str], splitter: str) -> str:
    match data:
        case []: return ""
        case [item]: return item
        case [item, *rest]: return item + splitter + make_row_with_splitter_recursive(rest, splitter)


def generate_tex_table(data: list[list[str]]) -> str:
    return f"\\begin{{tabular}}{{{make_row_with_splitter_recursive(["c"] * len(data[0])," ")}}}\n{make_rows(data)}\n\\end{{tabular}}\n"


def generate_tex_image(path_to_image, caption):
    return f"\\begin{{figure}}\n\\centering\n\\includegraphics{{ {path_to_image} }}\n\\caption{{ {caption} }}\n\\end{{figure}}\n"
