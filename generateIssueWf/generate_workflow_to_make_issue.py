# Library by default
from distutils.log import error
from time import time
import traceback
from pathlib import Path
# Library by third party
# nothing
# Library in the local
# nothing
# Library in landmasterlibrary
from landmasterlibrary.generaltool import get_str_by_zero_padding, get_src_path_from_test_path, read_txt_lines, read_csv_lines, get_indcies_containing_words, append_items, generate_cron_from_datetime_now


def rewrite_cron_of_remove_workflow(is_there_issue_to_generate : bool, minutes_scheduled_later : int, time_difference : int):
    file_name = "removeWfForIssuesAndCsvContent.yml"
    dir_having_file = ".github/workflows"
    file_full_name = get_src_path_from_test_path(__file__, file_name, dir_having_file, isChecking=False)

    read_wf_lines = read_txt_lines(__file__, [file_name], dir_having_file)[0]
    mark_of_schedule = "  schedule:"
    index_of_workflow_schedule = get_indcies_containing_words(read_wf_lines, [mark_of_schedule])[0]
    mark_of_cron = "  - cron: '"
    index_of_workflow_cron = get_indcies_containing_words(read_wf_lines, [mark_of_cron])[0]
    cron = generate_cron_from_datetime_now(minutes_scheduled_later, time_difference)

    read_wf_lines[index_of_workflow_schedule] = "  schedule:"
    read_wf_lines[index_of_workflow_cron] = f"  - cron: '{cron}'  # https://crontab.guru"

    read_wf_lines_str = "\n".join(map(str, read_wf_lines))
    with open(file_full_name, "w") as fw:
        fw.write(read_wf_lines_str)
    print(read_wf_lines_str)
    print("==================================")

def generate_workflow():
    labels = ["book", "blog"]
    read_files = []
    count_of_zero_length = 0
    is_there_issue_to_generate = True
    for i in range(0, len(labels)):
        read_files.append(f"{labels[i]}s.csv")
    txt_lines = read_csv_lines(__file__, read_files, "generateIssueWf")
    for i in range(0, len(txt_lines)):
        txt_lines[i].pop(0) # remove "title,milestone" row.
        if len(txt_lines[i]) == 0:
            count_of_zero_length += 1
    print(txt_lines)

    if count_of_zero_length == len(labels):
        txt_lines = [[["dummytitle", 0, "dummybody"]]]
        is_there_issue_to_generate = False

    minutes_scheduled_later = 10
    time_difference = 0
    cron = generate_cron_from_datetime_now(minutes_scheduled_later, time_difference)
    rewrite_cron_of_remove_workflow(is_there_issue_to_generate, minutes_scheduled_later + 20, time_difference)

    cron_lines = []
    if is_there_issue_to_generate:
        cron_lines.append("  schedule:")
        cron_lines.append(f"  - cron: '{cron}'  # https://crontab.guru")
    else:
        cron_lines.append("#   schedule:")
        cron_lines.append(f"#   - cron: '{cron}'  # https://crontab.guru")
        print("No generated workflows to make issues today.")
        # return False

    str_of_workflow_dispatch = "  workflow_dispatch:"
    read_wf_lines = read_txt_lines(__file__, ["generateIssues.yml"], ".github/workflows")[0]
    index_of_workflow_dispatch = read_wf_lines.index(str_of_workflow_dispatch)
    read_wf_lines = append_items(read_wf_lines, cron_lines, index_of_workflow_dispatch + 1)

    str_of_scheduled_issue = "    - name: Scheduled Issue to landmaster135"
    index_of_name_of_scheduled_issue = read_wf_lines.index(str_of_scheduled_issue)

    src_file_name = "generateIssues.yml"
    generated_files = []
    for i in range(0, len(txt_lines)):
        for j in range(0, len(txt_lines[i])):
            # write contents
            read_wf_lines[index_of_name_of_scheduled_issue + 3] = f"        title: {txt_lines[i][j][0]}" # title
            label = str(labels[i])
            read_wf_lines[index_of_name_of_scheduled_issue + 5] = f"        labels: \"{label}\"" # labels
            read_wf_lines[index_of_name_of_scheduled_issue + 8] = f"        template: \".github/ISSUE_TEMPLATE/custom.md\"" # template
            read_wf_lines[index_of_name_of_scheduled_issue + 9] = f"        project: 1" # project
            read_wf_lines[index_of_name_of_scheduled_issue + 10] = f"        column: Todo" # column
            milestone = ""
            initial_of_milestone = "        milestone: "
            if txt_lines[i][j][1] == "0":
                pass
            else:
                milestone = f"{initial_of_milestone}{str(txt_lines[i][j][1])}"
            read_wf_lines[index_of_name_of_scheduled_issue + 11] = milestone # milestone
            read_wf_lines[index_of_name_of_scheduled_issue + 12] = f"        body: {txt_lines[i][j][2]}" # body

            # decide file name
            j_padded = get_str_by_zero_padding(j, 2)
            src_file_name = f"generateIssues_{label}_{j_padded}.yml"
            generated_file_full_name = get_src_path_from_test_path(__file__, src_file_name, ".github/workflows", isChecking=False)

            # generate workflow files
            read_wf_lines_str = "\n".join(map(str, read_wf_lines))
            with open(generated_file_full_name, "w") as fw:
                fw.writelines(read_wf_lines_str)
            generated_files.append(src_file_name)

    # genereate text memo file.
    generated_files_str = "\n".join(map(str, generated_files))
    file_name_written_file_to_remove = "generatedWfFiles.txt"
    generated_file_full_name = get_src_path_from_test_path(__file__, file_name_written_file_to_remove, ".github/workflows", isChecking=False)
    with open(generated_file_full_name, "w") as fw:
        fw.write(generated_files_str)
    for i in read_wf_lines:
        print(i)

    return True

def main():
    generate_workflow()

if __name__ == "__main__":
    main()
