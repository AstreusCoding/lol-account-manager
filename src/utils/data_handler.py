from os import getcwd, makedirs, remove, path, walk
from typing import Dict, Optional

DEFAULT_FOLDERS = ["settings", "logs"]
ERRORS = {
    "invalid_file_path": ValueError(
        "path '{file_path}' is not a valid file path. It may not exist."
    ),
    "no_longer_valid_file_path": FileNotFoundError(
        "'{file_path}' is no longer a valid file path. It may have been deleted already."
    ),
    "file_path_cant_be_none": ValueError("file_path can't be None"),
}


class File:
    """
    A file class meant to mimick files in the project.

    Notes
    -----
    This class is not meant to be used for creating files. It is meant to be used for representing files in the project.
    """

    def _is_file_path_valid(self):
        """
        Checks if the file path is valid.

        Parameters
        ----------
        file_path : str
            The path to the file.

        """
        if self.path is None:
            raise ERRORS["file_path_cant_be_none"]
        if not path.isfile(self.path):
            raise ERRORS["invalid_file_path"]

    def _does_file_exist(self):
        """
        Checks if the file exists.
        """
        if not path.isfile(self.path):
            raise ERRORS["no_longer_valid_file_path"]

    def __init__(self, file_path: str):
        self.path: str = file_path
        self._is_file_path_valid()

    def delete(self) -> None:
        """
        Deletes the file.
        """
        self._does_file_exist()

        remove(self.path)

        return None

    def get(self) -> str:
        """
        Gets the file.

        Returns
        -------
        str
            The file.
        """
        with open(self.path, "r") as file:
            return file.read()


class Folder:
    """
    A folder class meant to mimick folders in the project.
    """

    def _create_self(self) -> None:
        """
        Creates the folder.
        """
        makedirs(self.path, exist_ok=True)

        return None

    def __init__(self, folder_path: str, should_create: bool = False) -> None:
        """
        Initializes the folder.

        Parameters
        ----------
        folder_path : str
            The path to the folder.
        should_create : bool, optional
            Whether or not to create the folder if it doesn't exist. Defaults to False.

        Returns
        -------
        Folder
            The folder.
        """
        self.path: str = folder_path

        if not path.isdir(self.path):
            if should_create:
                self._create_self()

            else:
                raise ValueError(
                    f"path '{self.path}' is not a valid path. It may not exist consider using the 'should_create' parameter."
                )
        self.name: str = path.basename(self.path)

        # get the subfolders and files
        self.subfolders: dict[str, Folder] = {}
        self.files: list[File] = []

        # get all the subfolders in the folder
        folders, files = next(walk(self.path))[1:]

        for folder in folders:
            self.add_subfolder(path.join(self.path, folder))

        for file in files:
            self.add_file(path.join(self.path, file))

        return None

    def search_for_subfolder(self, folder_name: str) -> Optional["Folder"]:
        """
        Searches for a subfolder in the folder.

        Parameters
        ----------
        folder_name : str
            The name of the subfolder to search for.

        Returns
        -------
        Folder
            The subfolder.
        """
        # search for the folder
        if self.subfolders.get(folder_name) is not None:
            return self.subfolders[folder_name]

        return None

    def recursive_search_for_subfolder(
        self,
        folder_name: str,
        required_parent_name: str = None,
    ) -> Optional["Folder"]:
        """
        Recursively searches for a subfolder in the folder.

        Parameters
        ----------
        folder_name : str
            The name of the subfolder to search for.

        Returns
        -------
        Folder
            The subfolder.
        """
        folder: None | Folder = None
        if required_parent_name is None:
            for subfolder in self.subfolders.values():
                if subfolder.name == folder_name:
                    return subfolder
                else:
                    folder = subfolder.recursive_search_for_subfolder(folder_name)

        elif self.name == required_parent_name:
            return self.search_for_subfolder(folder_name)
        else:
            for subfolder in self.subfolders.values():
                folder = subfolder.recursive_search_for_subfolder(
                    folder_name, required_parent_name
                )
        return folder

    def create_subfolder(self, folder_name: str) -> "Folder":
        """
        Creates a subfolder in the folder.

        Parameters
        ----------
        folder_name : str
            The name of the subfolder.

        Returns
        -------
        Folder
            The subfolder.
        """
        # create the subfolder
        subfolder = Folder(path.join(self.path, folder_name), True)

        # add the subfolder to the subfolders dict
        self.subfolders[folder_name] = subfolder

        return subfolder

    def add_subfolder(self, folder_path: str) -> None:
        """
        Adds a subfolder to the folder.

        Parameters
        ----------
        folder_path : str
            The path to the subfolder.
        """
        # make sure there is no subfolder with the same path already
        for subfolder in self.subfolders.values():
            if subfolder.path == folder_path:
                raise ValueError(
                    f"folder '{folder_path}' is already in the subfolders of folder '{self.name}'."
                )

        # create the folder
        folder = Folder(folder_path)

        # add the folder to the subfolders
        self.subfolders[folder.name] = folder

        return None

    def add_file(self, file_path: str) -> None:
        """
        Adds a file to the folder.

        Parameters
        ----------
        file_path : str
            The path to the file.
        """
        # make sure there is no file with the same path already
        for file in self.files:
            if file.path == file_path:
                raise ValueError(
                    f"file '{file_path}' is already in the files of folder '{self.name}'."
                )

        # create the file
        file = File(file_path)

        # add the file to the files
        self.files.append(file)

        return None


class DataHandler:
    """
    The data handler class that handles all data / files in the project.
    """

    def __init__(self, folder_name: str = "data", project_path: str = None) -> None:
        """
        Initializes the data handler.

        Parameters
        ----------
        folder_name : str
            The name of the data folder.
        project_path : str, optional
            The path to the project. Defaults to the current working directory. Should be the path containing your src folder.

        Returns
        -------
        DataHandler
            The data handler for the project.
        """
        # set the project name and path
        self.folder_name = folder_name
        self.project_path = project_path if project_path is not None else getcwd()

        self.default_folders: Dict[str, Folder] = {}

        # create the data folder and default folders
        self._create_data_folder()
        self._create_default_folders()

    def create_folder(self, folder_name: str, parent_folder: Folder = None) -> Folder:
        """
        Creates a folder in the project.

        Parameters
        ----------
        folder_name : str
            The name of the folder to create.
        parent_folder : Folder, optional
            The parent folder of the folder to create. Defaults to the data folder.
        can_exist : bool, optional
            Whether or not the folder can already exist. Defaults to False.
        """
        if parent_folder is None:
            parent_folder = self.data_folder

        new_folder_path = path.join(parent_folder.path, folder_name)

        return Folder(new_folder_path, should_create=True)

    def search_for_folder(
        self, folder_name: str, required_parent_name: str = None
    ) -> Optional[Folder]:
        """
        Searches for a folder in the project.

        Parameters
        ----------
        folder_name : str
            The name of the folder to search for.
        required_parent_name : str, optional
            The name of the parent folder that the folder must be in. Defaults to None.
        """
        # search for the folder
        return self.data_folder.recursive_search_for_subfolder(
            folder_name, required_parent_name
        )

    def _create_data_folder(self) -> None:
        """
        Creates the data folder for the project.
        """
        # create the data folder
        self.data_folder: Folder = Folder(
            path.join(self.project_path, self.folder_name), True
        )

        return None

    def _create_default_folders(self) -> None:
        """
        Creates the default folders for the project.
        """
        for folder_name in DEFAULT_FOLDERS:
            self.default_folders[folder_name] = Folder(
                path.join(self.data_folder.path, folder_name), True
            )

        return None
