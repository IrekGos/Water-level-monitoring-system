import sqlite3
from dotenv import dotenv_values
from hashlib import sha3_512


class CredentialsDB:
    def __init__(self) -> None:
        CONFIG = dotenv_values(".env")
        self.__connection = sqlite3.connect(CONFIG["DB_LOCATION"])
        self.__cursor = self.__connection.cursor()

    def authenticate(self, username: str, password: str) -> bool:
        hashed_password = sha3_512(password.encode('utf-8')).hexdigest()
        self.__cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM CREDENTIALS WHERE Username = ? AND Password = ?)", (username, hashed_password))
        user = self.__cursor.fetchall()
        assert (len(user) == 1)
        return bool(user[0][0])

    def __del__(self) -> None:
        self.__connection.close()
