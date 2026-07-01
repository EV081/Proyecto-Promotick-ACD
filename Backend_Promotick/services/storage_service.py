import os
import sqlite3

from fastapi import UploadFile

UPLOAD_DIR = "uploads"
DB_NAME = "app.db"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

def save_file(
    file: UploadFile
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            file.file.read()
        )

    return file_path


def get_connection():

    conn = sqlite3.connect(
        DB_NAME
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()