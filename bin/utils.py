from io import TextIOWrapper
from os import listdir
from pathlib import Path


OPENING_ROOT = "<root>"
CLOSING_ROOT = "</root>"
CLOSING_LANGUAGE = "</language>"

XML_TAG = '<?xml version="1.0" encoding="UTF-8"?>'

ORIGINAL_FILES_PATH = Path("black_reliquary")
TRANSLATION_SOURCE_PATH = Path("data")
TRANSLATION_DESTINATION_PATH = Path("build")


def fake_translation(language:str):
    for original_filename in listdir(ORIGINAL_FILES_PATH):
        print(original_filename)
        open_translation(original_filename)
        translation_injection(original_filename, mock_language=True)
        close_translation(original_filename)

def translate_everything():
    for original_filename in listdir(ORIGINAL_FILES_PATH):
        print(original_filename)
        partial_duplication(original_filename)
        translation_injection(original_filename)
        close_translation(original_filename)


def partial_duplication(original_filename:str):
    original_filepath = Path(ORIGINAL_FILES_PATH, original_filename)
    destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(original_filepath, mode="r", encoding="utf8") as original_file:
        with open(destination_filepath, mode="w", encoding="utf8") as destination_file:
            for line in original_file.readlines():
                line_content = line.strip()
                if line_content != CLOSING_ROOT:
                    destination_file.write(line)


def translation_injection(original_filename:str, mock_language:bool=False):
    for language in listdir(TRANSLATION_SOURCE_PATH):
        source_filepath = Path(TRANSLATION_SOURCE_PATH, language, original_filename)
        destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
        
        with open(source_filepath, mode="r", encoding="utf8") as source_file:
            with open(destination_filepath, mode="a", encoding="utf8") as destination_file:

                destination_file.write(f'\n')
                if mock_language:
                    destination_file.write(f'\t<language id="english">\n')
                else:
                    destination_file.write(f'\t<language id="{language}">\n')
                inject_language_file(source_file, destination_file)
                destination_file.write(f"\n\t{CLOSING_LANGUAGE}\n")


def inject_language_file(source:TextIOWrapper, destination:TextIOWrapper):
    for line in source.readlines():
        line_with_tabs = f"\t\t{line}"
        destination.write(line_with_tabs)


def close_translation(original_filename:Path):
    translated_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(translated_filepath, mode="a", encoding="utf8") as translated_file:
        translated_file.write(f"\n{CLOSING_ROOT}")


def open_translation(original_filename:Path):
    destination_filepath = Path(TRANSLATION_DESTINATION_PATH, original_filename)
    with open(destination_filepath, mode="w", encoding="utf8") as destination_file:
        destination_file.write(XML_TAG)
        destination_file.write(OPENING_ROOT)
