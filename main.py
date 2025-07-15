import os
import re
from deep_translator import GoogleTranslator

def is_chinese(text):
    return re.search('[\u4e00-\u9fff]', text) is not None

def translate_name(name):
    translated = GoogleTranslator(source='auto', target='en').translate(name)
    translated = re.sub(r'[\\/:*?"<>|]', '_', translated)
    translated = translated.strip()
    if not translated:
        translated = "translated"
    return translated

def rename_tree(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Файли
        for filename in filenames:
            if is_chinese(filename):
                old_file = os.path.join(dirpath, filename)
                new_filename = translate_name(filename)
                new_file = os.path.join(dirpath, new_filename)
                if old_file != new_file:
                    os.rename(old_file, new_file)
                    print(f"Renamed file: {old_file} -> {new_file}")
        # Папки
        for dirname in dirnames:
            if is_chinese(dirname):
                old_dir = os.path.join(dirpath, dirname)
                new_dirname = translate_name(dirname)
                new_dir = os.path.join(dirpath, new_dirname)
                if old_dir != new_dir:
                    os.rename(old_dir, new_dir)
                    print(f"Renamed dir: {old_dir} -> {new_dir}")

    # Перейменування кореневої папки (опційно)
    base = os.path.basename(root_path)
    parent = os.path.dirname(root_path)
    if is_chinese(base):
        new_base = translate_name(base)
        new_root = os.path.join(parent, new_base)
        os.rename(root_path, new_root)
        print(f"Renamed root dir: {root_path} -> {new_root}")

if __name__ == "__main__":
    root_folder = "/Users/dmytro.polishchuk/Downloads/BMCU-master/files/bmcu"   # заміни на свій шлях
    rename_tree(root_folder)
