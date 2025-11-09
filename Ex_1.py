import os
import shutil
from concurrent.futures import ThreadPoolExecutor

def copy_file(src_path, dest_dir):
    ext = os.path.splitext(src_path)[1].lower().lstrip(".")
    if not ext:
        ext = "no_extension"
    ext_dir = os.path.join(dest_dir, ext)
    os.makedirs(ext_dir, exist_ok=True)
    shutil.copy(src_path, os.path.join(ext_dir, os.path.basename(src_path)))

def process_directory(source_dir, dest_dir, executor):
    try:
        with os.scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    executor.submit(copy_file, entry.path, dest_dir)
                elif entry.is_dir():
                    executor.submit(process_directory, entry.path, dest_dir, executor)
    except PermissionError:
        pass

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(base_path, "Хлам")
    dest_dir = os.path.join(base_path, "dist")


    if not os.path.exists(source_dir):
        print(f"У проєкті немає папки 'Хлам'")
        return

    os.makedirs(dest_dir, exist_ok=True)


    with ThreadPoolExecutor(max_workers=8) as executor:
        process_directory(source_dir, dest_dir, executor)

    print(f"Усі файли з '{source_dir}' скопійовані до '{dest_dir}' за розширеннями.")

if __name__ == "__main__":
    main()
