import os
import pdflatex
from latex_image_and_table_generator import generate_tex_table, generate_tex_image
import tempfile


def create_pdf_with_table_and_image():
    os.environ["PATH"] = "/Library/TeX/texbin:" + os.environ.get("PATH", "")

    img_1_path = "images/cat_image.png"
    table = [
        ["Name", "Age", "Gender", "City", "Profession"],
        ["Alice", "23", "F", "New York", "Engineer"],
        ["Bob", "25", "M", "San Francisco", "Doctor"],
        ["Charlie", "27", "M", "Los Angeles", "Artist"],
    ]

    table_tex = generate_tex_table(table)
    image_tex = generate_tex_image(img_1_path, "It is a cat")

    pdf_text = (
        f"\\documentclass{{article}}\n"
        f"\\usepackage{{graphicx}}\n"
        f"\\begin{{document}}\n"
        f"{table_tex}\n"
        f"{image_tex}\n"
        f"\\end{{document}}"
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as tmp_file:
        tmp_file.write(pdf_text)
        tex_file_path = tmp_file.name

    pdfl = pdflatex.PDFLaTeX.from_texfile(tex_file_path)
    pdfl.set_output_directory("artifacts")
    pdfl.set_pdf_filename("image_and_table")
    pdfl.create_pdf(keep_pdf_file=True)

    print(f"PDF saved to artifacts/image_and_table.pdf")


if __name__ == "__main__":
    create_pdf_with_table_and_image()
