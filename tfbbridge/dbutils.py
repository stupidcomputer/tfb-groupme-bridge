"""
Database shenanigans
"""

import sqlite3
import os
from flask import current_app, g

def get_and_init_db(database: str):
    # check if the file exists first
    new_database = not os.path.exists(database)

    db = sqlite3.connect(
        database,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    if new_database:
        with current_app.open_resource("schema.sql") as handle:
            schema = handle.read().decode('utf8')
            db.executescript(schema)

        print("I've initialized the database!")

    return db

def get_db():
    # given a global object, populate it if necessary and return the db

    if 'db' not in g:
        g.db = get_and_init_db(current_app.config["DATABASE_LOCATION"])
    
    return g.db