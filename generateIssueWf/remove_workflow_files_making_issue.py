# Library by default
from distutils.log import error
import traceback
from pathlib import Path
import os
# Library by third party
# nothing
# Library in the local
# nothing
# Library in landmasterlibrary
from landmasterlibrary.generaltool import get_src_path_from_test_path, read_txt_lines, get_files_by_extensions

def remove_workflow():
    # remove workflow files.
    file_names_written_file_to_remove = ["generatedWfFiles.txt"]
    target_dir = ".github/workflows"
    file_names = read_txt_lines(__file__, file_names_written_file_to_remove, target_dir)[0]
    for i in range(0, len(file_names)):
        file_full_name = get_src_path_from_test_path(__file__, file_names[i], target_dir)
        os.remove(file_full_name)
    file_full_name_written_file_to_remove = get_src_path_from_test_path(__file__, file_names_written_file_to_remove[0], target_dir)
    with open(file_full_name_written_file_to_remove, "w") as fw:
        fw.write("")

    # delete issue titles from csv files.
    extension = [".csv"]
    csv_files = get_files_by_extensions("./", extension)
    print(csv_files)
    for i in range(0, len(csv_files)):
        with open(csv_files[i], "r") as fr:
            read_lines = fr.readlines()
            print(read_lines)
        with open(csv_files[i], "w") as fw:
            fw.writelines(read_lines[0])
        with open(csv_files[i], "r") as fr:
            read_lines = fr.readlines()
            print(read_lines)

def main():
    remove_workflow()

if __name__ == "__main__":
    main()
