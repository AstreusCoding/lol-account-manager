from os import path, chdir, listdir, getcwd

BUILT_IN_MARKER_FILE_NAMES: list[str] = ["setup.py", "readme.md", "requirements.txt"]

COLORS = {
    "Red": "\033[31m",
    "Green": "\033[32m",
    "Yellow": "\033[33m",
    "Blue": "\033[34m",
    "Magenta": "\033[35m",
    "Cyan": "\033[36m",
    "White": "\033[37m",
    "Light Red": "\033[91m",
    "Light Green": "\033[92m",
    "Light Yellow": "\033[93m",
    "Reset": "\033[0m",
}


def cut_off_string(input_string: str, cut_off_point: int) -> str:
    """
    Cuts off the input string if it is too long. If it is too short, adds spaces to the end of the string.
    """
    return (
        input_string[:cut_off_point]
        if len(input_string) > cut_off_point
        else input_string + " " * (cut_off_point - len(input_string))
    )


def get_project_root(marker_file_override: list = None) -> str:
    """
    Gets the project root regardless of relative or absolute path
    of the current file.

    Parameters
    ----------
    marker_override : list of str, optional
        a custom marker file names to use instead of the default marker file names.
        See the Notes section for defaults.

    Returns
    -------
    str
        The project root path.

    Notes
    -----
    If you are using a "src" folder structure, this function will find the project root.

    This also finds the root if any of the following files are in the root directory:
        - Custom file name (if given)
        - source
        - setup.py
        - readme.md
        - requirements.txt
    """
    # get the current file path
    current_file_path: str = path.abspath(__file__)

    # set the project root path
    project_root_path: str = ""

    # list of all marker file names
    marker_file_names: list[str] = BUILT_IN_MARKER_FILE_NAMES

    # check if there is a marker override
    if marker_file_override:
        # set the marker file names to the override
        marker_file_names = marker_file_override

    # Try and get the project root by going up one directory from the current file path until we find the project root.
    while not project_root_path:
        # get the parent directory of the current file path
        parent_directory: str = path.dirname(current_file_path)
        parent_directory_basename: str = path.basename(parent_directory)

        if parent_directory_basename == "src":
            # get the parent directory of the "src" directory
            project_root_path = path.dirname(parent_directory)
            break

        # get all the files in the parent directory
        parent_directory_files: list[str] = listdir(parent_directory)

        # check if any of the marker files are in the parent directory
        for marker_file_name in marker_file_names:
            if marker_file_name in parent_directory_files:
                project_root_path = parent_directory
                break

        # If we reached drive root, we didn't find the project root.
        if not parent_directory_basename:
            # break out of the loop
            break

        # set the current file path to the parent directory
        current_file_path = parent_directory

    # check if we didn't find the project root after the loop
    if not project_root_path:
        # raise an error
        raise FileNotFoundError("Could not find the project root!")

    # return the project root path
    return project_root_path


def fix_working_directory() -> None:
    """
    Sets the working directory to the project root.

    Returns
    -------
    None

    Notes
    -----
    This function should be called before any functions that use relative file paths.

    Reason
    ------
    When running the bot from the command line, the working directory is set to the
    directory from which the command was run. So, if we are using a source folder
    structure, the working directory will be set to the source folder instead of the
    project root. This caused certain files to either not be found or be created in
    wrong location, so I wrote this function to fix this issue.

    """
    # get the project root
    project_root: str = get_project_root()

    # get the current working directory before changing it so we can print it
    old_working_directory: str = str.lower(getcwd())

    # set the working directory to the project root
    chdir(project_root)

    if project_root == old_working_directory:
        print(f"Working directory is correct!\nCURRENT > {project_root}")
    else:
        print(
            f"Working directory was changed!\nOLD | {old_working_directory}\nNEW | {project_root}"
        )

    # return None
    return None
