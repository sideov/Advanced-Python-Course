from tex_generator import generate_tex_table


def create_table_and_save_to_tex_file():
    table = [
        ["Name", "Age", "Gender", "City", "Profession"],
        ["Alice", "23", "F", "New York", "Engineer"],
        ["Bob", "25", "M", "San Francisco", "Doctor"],
        ["Charlie", "27", "M", "Los Angeles", "Artist"],
    ]
    with open("artifacts/table.tex", "w") as file:
        to_write = f"\\documentclass{{article}}\n\\begin{{document}}\n{
            generate_tex_table(table)}\\end{{document}}"
        file.write(to_write)

    print("Table saved to artifacts/table.tex")


if __name__ == "__main__":
    create_table_and_save_to_tex_file()
