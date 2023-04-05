from io import TextIOWrapper


CLOSING_ROOT = "</root>"
CLOSING_LANGUAGE = "</language>"


# TODO : more automation
french_filepath = "data/french/miscellaneous.string_table.xml"
original_filepath = "black_reliquary/miscellaneous.string_table.xml"
new_filepath = "build/miscellaneous.string_table.xml"


def duplicate_original_file(original_file, new_file):
    for line in original_file.readlines():
        line_content = line.strip()
        if line_content != CLOSING_ROOT:
            new_file.write(line)


def inject_translation(language, language_file:TextIOWrapper, new_file:TextIOWrapper):
    new_file.write(f'\t<language id="{language}">\n')
    inject_file_content(language_file, new_file)
    new_file.write(f"\n\t{CLOSING_LANGUAGE}")


def inject_file_content(file_source:TextIOWrapper, file_destination:TextIOWrapper):
    for line in file_source.readlines():
        line_with_tabs = f"\t\t{line}"
        file_destination.write(line_with_tabs)


def add_closing_root(file_target:TextIOWrapper):
    file_target.write(f"\n{CLOSING_ROOT}")


def main():
    with open(original_filepath, mode="r", encoding="utf8") as original_file:
        with open(new_filepath, mode="w", encoding="utf8") as new_file:
            with open(french_filepath, mode="r", encoding="utf8") as french_file:
                duplicate_original_file(original_file, new_file)
                inject_translation("french", french_file, new_file)
                add_closing_root(new_file)


if __name__ == "__main__":
    main()
