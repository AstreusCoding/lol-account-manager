import coloredlogs
import logging
import logging.handlers

from .data_handler import DataHandler, File, Folder
from .utils import cut_off_string, COLORS as colors

LOGGER_NAME_CUT_OFF_POINT = 4

logging.logThreads = False
logging.logProcesses = False
logging._srcfile = None

# Define a dictionary mapping logger names to color codes
mapped_logger_colors = {
    "main": colors["Green"],
}


def ensure_logs_folder_exists(data_handler: DataHandler) -> Folder:
    """
    Ensures that the logs folder exists.
    """
    # create the configuration folder if it does not exist
    return data_handler.create_folder("logs")


def ensure_logger_folder_exists(
    data_handler: DataHandler, logs_folder: Folder, logger_name: str
) -> Folder:
    """
    Ensures that the logger folder exists.
    """
    # make sure the folder for this logger exists
    return data_handler.create_folder(logger_name, logs_folder)


class CustomLogger:
    """
    A custom logger class that allows for easy logging in the project.
    """

    def __init__(self, name: str = "main", logging_level=logging.DEBUG) -> None:
        """
        Initializes the custom logger.

        Parameters
        ----------
        name : str
            The name of the logger.
        logging_level : logging._Level, optional
            The logging level of the logger. Defaults to logging.INFO.
        """
        # set the logger name and logging level
        self.logger_name = name
        self.logging_level = logging_level

        # create the logger
        self.logger = logging.getLogger(self.logger_name)

        # create the folders for the logger
        self._create_folders()
        # setup the logging
        self._setup_logger()

    def _create_folders(self) -> None:
        """
        Creates the folders for the logger.
        """
        # get the data handler
        self.data_handler = DataHandler()

        # make sure the logs folder exists
        self.logs_folder: Folder = ensure_logs_folder_exists(self.data_handler)

        # make sure the folder for this logger exists
        self.logger_folder: Folder = ensure_logger_folder_exists(
            self.data_handler, self.logs_folder, self.logger_name
        )

        self.output_dir = self.logger_folder.path

        return None

    def _create_colored_logging_formatter(self) -> coloredlogs.ColoredFormatter:
        # define the logging format for dates
        dt_fmt = "%H:%M:%S"

        # set the logging level
        self.logger.setLevel(self.logging_level)

        # create the output string
        logger_name = self.logger_name
        cut_logger_name = cut_off_string(self.logger_name, LOGGER_NAME_CUT_OFF_POINT)
        if self.logger_name in mapped_logger_colors.keys():
            logger_name = (
                mapped_logger_colors[self.logger_name]
                + cut_logger_name
                + colors["Reset"]
            )

        output_str = f"%(asctime)s | {logger_name} | %(levelname)-5s | %(message)s"

        return coloredlogs.ColoredFormatter(fmt=output_str, datefmt=dt_fmt)

    def _create_logging_formatter(self) -> logging.Formatter:
        # define the logging format for dates
        dt_fmt = "%Y-%m-%d %H:%M:%S"

        # set the logging level
        self.logger.setLevel(self.logging_level)

        # create the output string
        output_str = "%(asctime)s | %(levelname)-5s | %(message)s"

        return logging.Formatter(fmt=output_str, datefmt=dt_fmt)

    def _create_file_handler(
        self, logging_formatter: logging.Formatter
    ) -> logging.FileHandler:
        # create the file handler
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=f"{self.output_dir}/latest.log",
            when="midnight",
            encoding="utf-8",
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setFormatter(logging_formatter)

        return file_handler

    def _create_console_handler(
        self, logging_formatter: logging.Formatter
    ) -> logging.StreamHandler:
        # make the console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging_formatter)

        return console_handler

    def _setup_logger(self) -> None:
        """
        Sets up the logging for the logger.
        """
        # create the logging formatters
        colored_logging_formatter = self._create_colored_logging_formatter()
        logging_formatter = self._create_logging_formatter()

        # create the file handler
        # create the console handler
        file_handler = self._create_file_handler(logging_formatter)
        console_handler = self._create_console_handler(colored_logging_formatter)

        # add the handlers to the discord logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # log the success
        self.logger.info(f"{self.logger_name} logger setup complete!")

        return None
