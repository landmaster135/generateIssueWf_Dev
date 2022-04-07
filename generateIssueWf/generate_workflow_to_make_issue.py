# Library by default
from distutils.log import error
from time import time
import traceback
from pathlib import Path
# Library by third party
# nothing
# Library in the local
from config import Config
# Library in landmasterlibrary
from landmasterlibrary.generaltool import get_str_by_zero_padding, get_src_path_from_test_path, read_txt_lines, read_csv_lines, get_indcies_containing_words, append_items, generate_cron_from_datetime_now


def rewrite_cron_of_remove_workflow(is_there_issue_to_generate : bool, minutes_scheduled_later : int, time_difference : int):
    file_name = Config.file_for_remove
    dir_having_workflow = Config.dir_having_workflow
    file_full_name = get_src_path_from_test_path(__file__, file_name, dir_having_workflow, isChecking=False)

    read_wf_lines = read_txt_lines(__file__, [file_name], dir_having_workflow)[0]
    mark_of_schedule = Config.mark_of_schedule
    # mark_of_schedule = mark_of_schedule
    index_of_workflow_schedule = get_indcies_containing_words(read_wf_lines, [mark_of_schedule])[0]
    mark_of_cron = Config.mark_of_cron
    index_of_workflow_cron = get_indcies_containing_words(read_wf_lines, [mark_of_cron])[0]
    cron = generate_cron_from_datetime_now(minutes_scheduled_later, time_difference)

    read_wf_lines[index_of_workflow_schedule] = mark_of_schedule
    read_wf_lines[index_of_workflow_cron] = f" {mark_of_cron} '{cron}'  # {Config.ref_url_for_cron}"

    read_wf_lines_str = "\n".join(map(str, read_wf_lines))
    with open(file_full_name, "w") as fw:
        fw.write(read_wf_lines_str)
    print(read_wf_lines_str)
    print("==================================")

def generate_workflow():
    # labels = ["book", "blog"]
    labels = Config.labels
    read_files = []
    count_of_zero_length = 0
    is_there_issue_to_generate = True
    for i in range(0, len(labels)):
        read_files.append(f"{labels[i]}s.{Config.file_ext_for_read}")
    txt_lines = read_csv_lines(__file__, read_files, Config.dir_of_this_app)
    for i in range(0, len(txt_lines)):
        txt_lines[i].pop(0) # remove "title,milestone" row.
        if len(txt_lines[i]) == 0:
            count_of_zero_length += 1
    print(txt_lines)

    if count_of_zero_length == len(labels):
        txt_lines = [[Config.dummy_text_list]]
        is_there_issue_to_generate = False

    minutes_scheduled_later = 10
    time_difference = 0
    cron = generate_cron_from_datetime_now(minutes_scheduled_later, time_difference)
    rewrite_cron_of_remove_workflow(is_there_issue_to_generate, minutes_scheduled_later + 20, time_difference)

    cron_lines = []
    mark_of_cron = Config.mark_of_cron
    mark_of_schedule = Config.mark_of_schedule
    if is_there_issue_to_generate:
        cron_lines.append(mark_of_schedule)
        cron_lines.append(f" {mark_of_cron} '{cron}'  # {Config.ref_url_for_cron}")
    else:
        cron_lines.append(f"# {mark_of_schedule}")
        cron_lines.append(f"#  {mark_of_cron} '{cron}'  # {Config.ref_url_for_cron}")
        print("No generated workflows to make issues today.")
        # return False

    src_file_name = f"{Config.src_file_name_wituout_ext}.{Config.file_ext_of_workflow}"
    mark_of_workflow_dispatch = Config.mark_of_workflow_dispatch
    dir_having_workflow = Config.dir_having_workflow
    read_wf_lines = read_txt_lines(__file__, [src_file_name], dir_having_workflow)[0]
    index_of_workflow_dispatch = read_wf_lines.index(mark_of_workflow_dispatch)
    read_wf_lines = append_items(read_wf_lines, cron_lines, index_of_workflow_dispatch + 1)

    str_of_scheduled_issue = Config.str_of_scheduled_issue
    index_of_name_of_scheduled_issue = read_wf_lines.index(str_of_scheduled_issue)

    generated_files = []
    indent_of_part_of_setting_attrs = Config.indent_of_part_of_setting_attrs
    obj_of_attrs = Config.obj_of_attrs
    for i in range(0, len(txt_lines)):
        for j in range(0, len(txt_lines[i])):
            # write contents
            index_of_attr = 3
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: {txt_lines[i][j][0]}" # title
            label = str(labels[i])
            index_of_attr = 5
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: \"{label}\"" # labels
            index_of_attr = 8
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: \"{Config.file_issue_template}\"" # template
            index_of_attr = 9
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: {Config.project_id}" # project
            index_of_attr = 10
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: {Config.target_column_in_project}" # column
            milestone = ""
            index_of_attr = 11
            initial_of_milestone = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: "
            if txt_lines[i][j][1] == str(Config.milestone_id_no_registering):
                pass
            else:
                milestone = f"{initial_of_milestone}{str(txt_lines[i][j][1])}"
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = milestone # milestone
            index_of_attr = 12
            read_wf_lines[index_of_name_of_scheduled_issue + index_of_attr] = f"{indent_of_part_of_setting_attrs}{obj_of_attrs[str(index_of_attr)]}: {txt_lines[i][j][2]}" # body

            # decide file name
            j_padded = get_str_by_zero_padding(j, 2)
            src_file_name = f"{Config.src_file_name_wituout_ext}_{label}_{j_padded}.{Config.file_ext_of_workflow}"
            generated_file_full_name = get_src_path_from_test_path(__file__, src_file_name, dir_having_workflow, isChecking=False)

            # generate workflow files
            read_wf_lines_str = "\n".join(map(str, read_wf_lines))
            with open(generated_file_full_name, "w") as fw:
                fw.writelines(read_wf_lines_str)
            generated_files.append(src_file_name)

    # genereate text memo file.
    generated_files_str = "\n".join(map(str, generated_files))
    file_written_files_to_remove = Config.file_written_files_to_remove
    generated_file_full_name = get_src_path_from_test_path(__file__, file_written_files_to_remove, dir_having_workflow, isChecking=False)
    with open(generated_file_full_name, "w") as fw:
        fw.write(generated_files_str)
    for i in read_wf_lines:
        print(i)

    return True

def main():
    generate_workflow()

if __name__ == "__main__":
    main()
