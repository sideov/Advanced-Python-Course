from tex_table_loader import create_table_and_save_to_tex_file
from tex_pdf_creator import create_pdf_with_table_and_image


def main():
    create_table_and_save_to_tex_file()
    create_pdf_with_table_and_image()


if __name__ == "__main__":
    main()
