import datetime
import os
from sqlite3 import OperationalError
import sqlalchemy
from sqlalchemy import text
import uuid
from sqlalchemy.pool import StaticPool
import psycopg2

engine = sqlalchemy.create_engine(os.environ["DB_URL"])


def create_meeting(name: str, users: str) -> str:
    """Create a meeting in the database

    :param name: Human readable db name
    :param time: Unix stamp of the meeting
    :param users: String list of user id(s) in the meeting
    :return: ID of the meeting
    """
    uid = str(uuid.uuid4())

    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(text("INSERT INTO meetings (id, name, time, users) VALUES (:id, :name, :time, :users)"),
                     [{"id": uid, "name": name, "time": datetime.datetime.now(), "users": users}])
        trans.commit()

    return uid
