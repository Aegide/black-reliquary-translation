from io import TextIOWrapper
from os import listdir
from pathlib import Path


CLOSING_ROOT = "</root>"
CLOSING_LANGUAGE = "</language>"


def duplicate_original_file(original_filepath:Path, build_filepath:Path):
    with open(original_filepath, mode="r", encoding="utf8") as original_file:
        with open(build_filepath, mode="w", encoding="utf8") as build_file:
            for line in original_file.readlines():
                line_content = line.strip()
                if line_content != CLOSING_ROOT:
                    build_file.write(line)


def inject_translation(language, language_file:TextIOWrapper, new_file:TextIOWrapper):
    new_file.write(f'\t<language id="{language}">\n')
    inject_file_content(language_file, new_file)
    new_file.write(f"\n\t{CLOSING_LANGUAGE}\n")


def inject_file_content(file_source:TextIOWrapper, file_destination:TextIOWrapper):
    for line in file_source.readlines():
        line_with_tabs = f"\t\t{line}"
        file_destination.write(line_with_tabs)


def add_closing_root(build_filepath:Path):
    with open(build_filepath, mode="a", encoding="utf8") as build_file:
        build_file.write(f"{CLOSING_ROOT}")


def translate_language(language:str):
    for filename in listdir(Path("data", language)):
        translate_file(language, filename)


def translate_file(language:str, filename:str):
    original_filepath = Path("black_reliquary", filename)
    build_filepath =    Path("build", filename)
    data_filepath =     Path("data", language, filename)

    with open(original_filepath, mode="r", encoding="utf8") as original_file:
        with open(build_filepath, mode="a", encoding="utf8") as build_file:
            with open(data_filepath, mode="r", encoding="utf8") as data_file:
                # duplicate_original_file(original_file, build_file)
                inject_translation(language, data_file, build_file)
                # add_closing_root(build_file)


def main():
    for filename in listdir(Path("black_reliquary")):
        original_filepath = Path("black_reliquary", filename)
        build_filepath =    Path("build", filename)
        duplicate_original_file(original_filepath, build_filepath)

    for language in listdir(Path("data")):
        translate_language(language)

    for filename in listdir(Path("black_reliquary")):
        build_filepath =    Path("build", filename)
        add_closing_root(build_filepath)


if __name__ == "__main__":
    main()
