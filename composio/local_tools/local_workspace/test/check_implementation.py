# flake8: noqa

from pprint import pprint

from composio.local_tools.local_workspace.cmd_manager.actions.clone_github import (
    GithubCloneCmd,
    GithubCloneRequest,
)
from composio.local_tools.local_workspace.cmd_manager.actions.cmds import (
    CreateFileCmd,
    CreateFileRequest,
)
from composio.local_tools.local_workspace.cmd_manager.actions.edit_cmd import (
    EditFile,
    EditFileRequest,
)
from composio.local_tools.local_workspace.cmd_manager.actions.run_cmd import (
    RunCommandOnWorkspace,
    RunCommandOnWorkspaceRequest,
)
from composio.local_tools.local_workspace.commons.history_processor import (
    HistoryProcessor,
)
from composio.local_tools.local_workspace.commons.local_docker_workspace import (
    LocalDockerArgumentsModel,
    WorkspaceManagerFactory,
)


def check_simple_implementation():
    args = LocalDockerArgumentsModel(
        image_name="sweagent/swe-agent:latest",
        verbose=True,
    )

    w = WorkspaceManagerFactory()
    h = HistoryProcessor()
    workspace_id = w.get_workspace_manager(args)

    # clone git repo
    git_clone = GithubCloneCmd()
    git_clone.set_workspace_and_history(w, h)
    git_clone_output = git_clone.execute(
        GithubCloneRequest(
            workspace_id=workspace_id,
            github_token="",
            repo_name="https://github.com/SWE-bench/SWE-bench.git",
        ),
        authorisation_data={},
    )
    print(git_clone_output)

    # create file
    create_file_cmd = CreateFileCmd()
    create_file_cmd.set_workspace_and_history(w, h)
    create_file_output = create_file_cmd.execute(
        CreateFileRequest(workspace_id=workspace_id, file_name="/SWE-bench/tmp-pv.py"),
        authorisation_data={},
    )
    print(create_file_output)

    # edit file
    edit_file_cmd = EditFile()
    edit_file_cmd.set_workspace_and_history(w, h)
    edit_file_output = edit_file_cmd.execute(
        EditFileRequest(
            workspace_id=workspace_id,
            start_line=1,
            end_line=1,
            replacement_text="""print("this is a test")""",
        ),
        authorisation_data={},
    )
    print(edit_file_output)

    run_command = RunCommandOnWorkspace()
    run_command.set_workspace_and_history(w, h)
    output = run_command.execute(
        RunCommandOnWorkspaceRequest(
            workspace_id=workspace_id, input_cmd="python /SWE-bench/tmp-pv.py"
        ),
        authorisation_data={},
    )

    print(output)


if __name__ == "__main__":
    check_simple_implementation()