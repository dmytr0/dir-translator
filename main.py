import os
import re
from deep_translator import GoogleTranslator

TARGET_DIR_PATH = "/Users/username/Downloads/ChineseDirName"  # Change this to your target directory path
CHINESE_SYMBOLS_PATTERN = '[\u4e00-\u9fff]'  # If you want other languages, change this regex pattern
TARGET_LANGUAGE = 'en'  # Change this to your target language code


def contain_symbols_for_translation(text):
    return re.search(CHINESE_SYMBOLS_PATTERN, text) is not None


def translate_name(name):
    translated = GoogleTranslator(source='auto', target=TARGET_LANGUAGE).translate(name)
    translated = re.sub(r'[\\/:*?"<>|]', '_', translated)
    translated = translated.strip()
    if not translated:
        translated = "translated"
    return translated


def rename_tree(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        for filename in filenames:
            if contain_symbols_for_translation(filename):
                old_file = os.path.join(dirpath, filename)
                new_filename = translate_name(filename)
                new_file = os.path.join(dirpath, new_filename)
                if old_file != new_file:
                    os.rename(old_file, new_file)
                    print(f"Renamed file: {old_file} -> {new_file}")
        for dirname in dirnames:
            if contain_symbols_for_translation(dirname):
                old_dir = os.path.join(dirpath, dirname)
                new_dirname = translate_name(dirname)
                new_dir = os.path.join(dirpath, new_dirname)
                if old_dir != new_dir:
                    os.rename(old_dir, new_dir)
                    print(f"Renamed dir: {old_dir} -> {new_dir}")

    base = os.path.basename(root_path)
    parent = os.path.dirname(root_path)
    if contain_symbols_for_translation(base):
        new_base = translate_name(base)
        new_root = os.path.join(parent, new_base)
        os.rename(root_path, new_root)
        print(f"Renamed root dir: {root_path} -> {new_root}")


if __name__ == "__main__":
    root_folder = TARGET_DIR_PATH
    rename_tree(root_folder)
