from io import TextIOWrapper
from os import listdir
from pathlib import Path
import uuid


import re


OPENING_ROOT = "<root>"
CLOSING_ROOT = "</root>"
CLOSING_LANGUAGE = "</language>"

XML_TAG = '<?xml version="1.0" encoding="UTF-8"?>'

ORIGINAL_FILES_PATH = Path("black_reliquary")
TRANSLATION_SOURCE_PATH = Path("data")
TRANSLATION_DESTINATION_PATH = Path("build")
REVIEW_PATH = Path("review")

MONO_LINE_PATTERN = r'<entry id=".*?"><!\[CDATA\[.*?\]\]></entry>\n'


def fake_translation():
    for original_filename in listdir(ORIGINAL_FILES_PATH):
        print(f"Localizing {original_filename}")
        open_translation(original_filename)
        translation_injection(original_filename, mock_language=True)
        close_translation(original_filename)

def translate_everything():
    for original_filename in listdir(ORIGINAL_FILES_PATH):
        print(f"Localizing {original_filename}")
        partial_duplication(original_filename)
        translation_injection(original_filename)
        close_translation(original_filename)


def partial_duplication(original_filename:str):
    original_filepath = Path(ORIGINAL_FILES_PATH, original_filename)
    destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    try:
        with open(original_filepath, mode="r", encoding="utf8") as original_file:
            with open(destination_filepath, mode="w", encoding="utf8") as destination_file:
                for line in original_file.readlines():
                    line_content = line.strip()
                    if line_content != CLOSING_ROOT:
                        destination_file.write(line)
    except UnicodeDecodeError as exception:
        print("(partial_duplication)", exception)

def translation_injection(original_filename:str, mock_language:bool=False):
    for language in listdir(TRANSLATION_SOURCE_PATH):
        source_filepath = Path(TRANSLATION_SOURCE_PATH, language, original_filename)
        destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)

        with open(source_filepath, mode="r", encoding="utf8") as source_file:
            with open(destination_filepath, mode="a", encoding="utf8") as destination_file:

                destination_file.write('\n')
                if mock_language:
                    destination_file.write('\t<language id="english">\n')
                else:
                    destination_file.write(f'\t<language id="{language}">\n')
                inject_language_file(source_file, destination_file)
                destination_file.write(f"\n\t{CLOSING_LANGUAGE}\n")


def uuid_generator(_match:re.Match[str]):
    full_uuid = str(uuid.uuid1())
    partial_uuid = full_uuid[4:8]
    return f"({partial_uuid}):"


def inject_language_file(source:TextIOWrapper, destination:TextIOWrapper):
    for line in source.readlines():
        keyword = "TODO:"
        result = re.sub(keyword, uuid_generator, line)
        # result = f"{line}"
        destination.write(result)


def close_translation(original_filename:str):
    translated_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(translated_filepath, mode="a", encoding="utf8") as translated_file:
        translated_file.write(f"\n{CLOSING_ROOT}")


def open_translation(original_filename:str):
    destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(destination_filepath, mode="w", encoding="utf8") as destination_file:
        destination_file.write(XML_TAG)
        destination_file.write(OPENING_ROOT)


def review_everything():
    for filename in listdir(TRANSLATION_DESTINATION_PATH):
        # print(f"Reviewing {filename}")
        review_translation(filename)


def review_translation(filename:str):
    language = "french"
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
    return re.sub("\n", "", text)


def add_line_returns(text:str):
    return re.sub("entry>.*?<entry", "entry>\n<entry", text)


def add_final_line_return(text:str):
    return re.sub("$", "\n", text)


def remove_valid_lines(text:str):
    return re.sub(MONO_LINE_PATTERN, '', text)
