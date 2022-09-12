"""
    This handles the database connection and queries.
    Written by: github.com/CasperDoesCoding
    Date: September / 9 / 2022
"""
import sqlite3
from logzero import logger
from account import Account


connection = None


class Database:

    connection = None

    def __init__(self) -> None:
        self.establish_connection()
        self.create_data_tables()

    def establish_connection(self) -> sqlite3.Connection:
        """
        Establishes a connection to the database.
        """
        global connection
        if self.connection is not None:
            return self.connection

        if connection is None:
            logger.info("Database connection is None establishing connection...")
            try:
                self.connection = sqlite3.connect("database.sqlite")
            except Exception as e:
                logger.error(f"Failed to establish database connection. {e}")
                return None
            finally:
                logger.info("Database connection established.")
                connection = self.connection
                return self.connection
        else:
            logger.info(
                "Database connection already established. Using existing connection..."
            )
            self.connection = connection
            return self.connection

    def create_data_tables(self) -> None:
        """
        Creates the data tables.
        """
        if self.establish_connection() is None:
            return False

        try:
            logger.info("Creating data tables...")
            cursor = self.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, region TEXT, display_name TEXT)"  # noqa: E501
            )
        except Exception as e:
            logger.error(f"Failed to create data tables. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Data tables created.")
            return True

    def get_account_by_username(self, username) -> Account:
        """
        Gets an account by username.
        """
        if self.establish_connection() is None:
            return

        try:
            logger.info("Getting account by username...")
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")
        except Exception as e:
            logger.error(f"Failed to get account by username. {e}")
        finally:
            account_details = cursor.fetchone()
            if account_details is None:
                return None

            account = Account(
                account_details[1],
                account_details[2],
                account_details[3],
                account_details[4],
            )
            logger.info("Account found.")
            cursor.close()
            return account

    def get_account_by_id(self, id) -> Account:
        """
        Gets an account by id.
        """
        if self.establish_connection() is None:
            return

        try:
            logger.info("Getting account by id...")
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM accounts WHERE id = '{id}'")
        except Exception as e:
            logger.error(f"Failed to get account by id. {e}")
        finally:
            account_details = cursor.fetchone()
            account = Account(
                account_details[1],
                account_details[2],
                account_details[3],
                account_details[4],
            )
            cursor.close()
            return account

    def get_all_accounts(self) -> list[Account]:
        """
        Gets all accounts from the database.
        """
        if self.establish_connection() is None:
            return

        try:
            logger.info("Getting all accounts...")
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM accounts")
        except Exception as e:
            logger.error(f"Failed to get all accounts. {e}")
        finally:
            account_details = cursor.fetchall()
            accounts = []
            for account in account_details:
                accounts.append(
                    Account(
                        account[1],
                        account[2],
                        account[3],
                        account[4],
                    )
                )
            cursor.close()
            return accounts

    def update_account_password(self, username, password) -> None:
        """
        Updates an account's password.
        """
        if self.establish_connection() is None:
            return False

        try:
            logger.info("Updating account...")
            cursor = self.connection.cursor()
            cursor.execute(
                f"UPDATE accounts SET password = '{password}' WHERE username = '{username}'"  # noqa: E501
            )
        except Exception as e:
            logger.error(f"Failed to update account. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Account updated.")
            return True

    def update_account_region(self, username, region) -> None:
        """
        Updates an account's region.
        """
        if self.establish_connection() is None:
            return False

        try:
            logger.info("Updating account...")
            cursor = self.connection.cursor()
            cursor.execute(
                f"UPDATE accounts SET region = '{region}' WHERE username = '{username}'"  # noqa: E501
            )
        except Exception as e:
            logger.error(f"Failed to update account. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Account updated.")
            return True

    def update_account_display_name(self, username, display_name) -> None:
        """
        Updates an account's display name.
        """
        if self.establish_connection() is None:
            return False

        try:
            logger.info("Updating account...")
            cursor = self.connection.cursor()
            cursor.execute(
                f"UPDATE accounts SET display_name = '{display_name}' WHERE username = '{username}'"  # noqa: E501
            )
        except Exception as e:
            logger.error(f"Failed to update account. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Account updated.")
            return True

    def add_account(self, username, password, region, display_name=None) -> None:
        """
        Adds an account to the database.
        """
        if self.establish_connection() is None:
            return False

        if self.get_account_by_username(username) is not None:
            logger.info("Account already exists.")
            return False

        try:
            logger.info("Adding account to database...")
            cursor = self.connection.cursor()
            cursor.execute(
                f"INSERT INTO accounts (username, password, region, display_name) VALUES ('{username}', '{password}', '{region}', '{display_name}')"  # noqa: E501
            )
        except Exception as e:
            logger.error(f"Failed to add account to database. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Account added to database.")

    def remove_account(self, username) -> None:
        """
        Removes an account from the database.
        """
        if self.establish_connection() is None:
            return

        try:
            logger.info("Removing account...")
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM accounts WHERE username = '{username}'")
        except Exception as e:
            logger.error(f"Failed to remove account. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Account removed.")

    def flush(self) -> None:
        """
        Flushes the database.
        """
        if self.establish_connection() is None:
            return

        try:
            logger.info("Flushing database...")
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM accounts")
        except Exception as e:
            logger.error(f"Failed to flush database. {e}")
        finally:
            cursor.close()
            self.connection.commit()
            logger.info("Database flushed.")
