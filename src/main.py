"""
    This handles the main program loop.
    Written by: github.com/CasperDoesCoding
    Date: -- / -- / ----

"""

from utils.custom_logger import CustomLogger


def main():
    """
    This is the main program loop.
    """
    # create the logger
    logger = CustomLogger().logger

    # log that the program has started
    logger.info("Starting program...")

    # log that the program has ended
    logger.info("Program ended.")


if __name__ == "__main__":
    main()
