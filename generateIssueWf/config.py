class Config:
    labels = ["book", "blog"]
    file_ext_for_read = "csv"
    dir_of_this_app = "generateIssueWf"
    dir_having_workflow = ".github/workflows"
    file_ext_of_workflow = "yml"
    file_for_remove = f"removeWfForIssuesAndCsvContent.{file_ext_of_workflow}"
    mark_of_schedule = "  schedule:"
    mark_of_cron = "  - cron:"
    mark_of_workflow_dispatch = "  workflow_dispatch:"
    src_file_name_wituout_ext = "generateIssues"
    file_written_files_to_remove = "generatedWfFiles.txt"
    str_of_scheduled_issue = "    - name: Scheduled Issue to landmaster135"
    dir_having_issue_template = ".github/ISSUE_TEMPLATE"
    file_issue_template = f"{dir_having_issue_template}/custom.md"
    indent_of_part_of_setting_attrs = "        "
    obj_of_attrs = {"3": "title"
                    , "5": "labels"
                    , "8": "template"
                    , "9": "project"
                    , "10": "column"
                    , "11": "milestone"
                    , "12": "body"
    }
    project_id = 1
    milestone_id_no_registering = 0
    target_column_in_project = "Todo"
    dummy_text_list = ["dummytitle", 0, "dummybody"]
    ref_url_for_cron = "https://crontab.guru"
