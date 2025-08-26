from io import TextIOWrapper
from os import listdir
from pathlib import Path
from uuid import uuid4
from re import sub


CLOSING_ROOT = "</root>"
CLOSING_LANGUAGE = "</language>"

ORIGINAL_FILES_PATH = Path("black_reliquary")
TRANSLATION_SOURCE_PATH = Path("data")
TRANSLATION_DESTINATION_PATH = Path("build")
REVIEW_PATH = Path("review")

MONO_LINE_PATTERN = r'<entry id="[\w\|\+\-.\[\]( )]+"><!\[CDATA\[[^>]*?\]\]><\/entry>\n'
CAPTURE_GROUP_START = r'<entry id="'
CAPTURE_GROUP_END = r'"><![CDATA['


def translate_everything():
    """Create the new translation files, in the folder `build`."""
    for original_filename in listdir(ORIGINAL_FILES_PATH):
        print(f"Localizing {original_filename}")
        partial_duplication(original_filename)
        translation_injection(original_filename)
        close_translation(original_filename)


def partial_duplication(original_filename:str):
    """Duplicate the original (_english_) files, but without the closing XML tag `</root>`.<br>
    Which will allow non-original translations to be added."""
    original_filepath = Path(ORIGINAL_FILES_PATH, original_filename)
    destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(original_filepath, mode="r", encoding="utf8") as original_file:
        with open(destination_filepath, mode="w", encoding="utf8") as destination_file:
            for line in original_file.readlines():
                if not is_closing_root(line):
                    destination_file.write(line)


def is_closing_root(line:str):
    """Checks if a line is the closing XML tag `</root>`."""
    return line.strip() == CLOSING_ROOT


def translation_injection(original_filename:str):
    """Appends non-original translations, to the translation files currently being built."""
    for language in listdir(TRANSLATION_SOURCE_PATH):
        source_filepath = Path(TRANSLATION_SOURCE_PATH, language, original_filename)
        destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
        with open(source_filepath, mode="r", encoding="utf8") as source_file:
            with open(destination_filepath, mode="a", encoding="utf8") as destination_file:
                destination_file.write('\n')
                destination_file.write(f'<language id="{language}">\n')
                inject_language_file(source_file, destination_file)
                destination_file.write(f"\n\t{CLOSING_LANGUAGE}\n")


def uuid_generator() -> str:
    """Function designed for the `sub` function, for the parameter `repl`.<br>
    Only the first 4 characters are used. The entire UUID would be too large to be displayed in-game.<br>
    The game will display translation "_values_", but not translation "_keys_".<br>
    These UUIDs are designed to connect any "_value_" to its respective _key_"."""
    return f"({str(uuid4())[0:4]}):"


def inject_language_file(source:TextIOWrapper, destination:TextIOWrapper):
    """Before the translation injection, replaces non-translated values with UUIDs.<br>
    Non-translated values should start with `TODO:`."""
    for line in source.readlines():
        result = sub("TODO:", uuid_generator(), line)
        destination.write(result)


def close_translation(original_filename:str):
    """Appends the closing XML tag `</root>."""
    translated_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(translated_filepath, mode="a", encoding="utf8") as translated_file:
        translated_file.write(f"\n{CLOSING_ROOT}")


def review_everything():
    """Checks if the translations are valid."""
    for filename in listdir(TRANSLATION_DESTINATION_PATH):
        # print(f"Reviewing {filename} ({TRANSLATION_DESTINATION_PATH})")
        review_translation(filename)
        # key_analysis(filename)


def key_analysis(filename:str, language:str = "french"):
    """Checks if the amount of keys is the same. Otherwise, it could mean that :
    - the custom translation is missing key/values from the original
    - the custom translation is translating key/values that don't exist in the original

    Currently unused, does not support multiple language at the same time."""
    translation_filepath = Path(TRANSLATION_SOURCE_PATH, language, filename)
    original_filepath = Path(ORIGINAL_FILES_PATH, filename)

    translation_key_list = get_key_list_from_file_path(translation_filepath)
    original_key_list = get_key_list_from_file_path(original_filepath)

    destination_filepath = Path(REVIEW_PATH, filename)
    # "w" will over-write previous results
    with open(destination_filepath, mode="w", encoding="utf8") as destination_file:

        key_difference = len(translation_key_list)-len(original_key_list)
        if key_difference != 0:
            destination_file.write(f"Different amount of keys: {key_difference}\n")
            for element in set(translation_key_list)-set(original_key_list):
                destination_file.write(f"[Missing from original] {element}\n")
            for element in set(original_key_list)-set(translation_key_list):
                destination_file.write(f"[Missing from translation] {element}\n")


def get_key_list_from_file_path(file_path:Path) -> list[str]:
    """Get the list of "_keys_" from the file content of a given file path."""
    key_list = []
    with open(file_path, mode="r", encoding="utf8") as file:
        file_content = file.read()
        for element in file_content.split(CAPTURE_GROUP_START):
            key_list.append(element.split(CAPTURE_GROUP_END)[0])
    return key_list


def review_translation(filename:str, language:str = "french") -> None:
    """Lists the anomalies it could detect, into the folder `review`.<br>
    Currently, does not support multiple language at the same time."""
    source_filepath = Path(TRANSLATION_SOURCE_PATH, language, filename)
    destination_filepath = Path(REVIEW_PATH, filename)
    with open(source_filepath, mode="r", encoding="utf8") as source_file:
        with open(destination_filepath, mode="w", encoding="utf8") as destination_file:
            file_content = source_file.read()
            file_content = remove_multi_lines(file_content)
            file_content = add_line_returns(file_content)
            file_content = add_final_line_return(file_content)
            file_content = remove_valid_lines(file_content)
            destination_file.write(file_content)


def remove_multi_lines(text:str):
    """Converts the file content into one line.<br>
    Which avoids having the deal with multi-lines values.<br>
    **Example**:<br>
    - `<entry id="str_vo_bad_BR_torchlight_03_0"><![CDATA[When the path is unclear, rely `<br>
    - `upon each other.]]></entry>`
    """
    return sub("\n", "", text)


def add_line_returns(text:str):
    """Adds line return at end of each key/value.<br>
    Which guarantees that 1 line is 1 key/value.<br>
    **Example**:<br>
    - `<entry id="str_vo_bad_BR_torchlight_03_0"><![CDATA[When the path is unclear, rely upon each other.]]></entry>`
    """
    return sub("</entry>.*?<entry ", "</entry>\n<entry ", text)


def add_final_line_return(text:str):
    """Adds the final line return, at end of the file.<br>
    Which guarantees that the pattern `MONO_LINE_PATTERN` will work properly.
    """
    return sub("$", "\n", text)


def remove_valid_lines(text:str):
    """It's easier to create a pattern to detect what's "_valid_"."""
    return sub(MONO_LINE_PATTERN, '', text)


def main():
    review_everything()


if __name__ == "__main__":
    main()
