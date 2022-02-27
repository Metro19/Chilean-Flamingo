import datetime
import os

# TODO: Optimize imports
from cogs.meeting_information import meeting

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import exists
import sqlalchemy
from sqlalchemy import text, column, table
import uuid
from sqlalchemy.pool import StaticPool
import psycopg2

engine = sqlalchemy.create_engine(os.environ["DB_URL"])


def unflatten_users(users: str) -> list[int]:
    """Unflatten users into user ids

    :param users: String form of user ids
    :return: List of user ids
    """
    real_users = []

    # iter through users
    for u in users.split("<SEP>"):
        real_users.append(int(u))

    return real_users


def flatten_users(users: list[int]) -> str:
    """Flatten list of users into a string

    :param users: List of users
    :return: String form of list
    """
    flat_users = ""

    # iter through users
    for u in users:
        flat_users += str(u) + "<SEP>"

    # strip last seperator
    return flat_users[:-5]


def create_meeting(name: str, dt: datetime.datetime, users: list[int]) -> meeting:
    """Create a meeting in the database

    :param name: Human readable db name
    :param dt: Unix stamp of the meeting
    :param users: String list of user id(s) in the meeting
    :return: ID of the meeting
    """
    uid = str(uuid.uuid4())

    # do transaction
    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(text("INSERT INTO meetings (id, name, time, users) VALUES (:id, :name, :time, :users)"),
                     [{"id": uid, "name": name, "time": dt, "users": flatten_users(users)}])
        trans.commit()

    # return meeting dataclass
    return meeting(uid, name, dt, users, "")


def adjust_meeting(meeting_obj: meeting) -> bool:
    """Adjust the time of a meeting

    :param meeting_obj: A new meeting object
    :return: T/F on success
    """

    # set up drive
    with Session(engine) as session:
        try:
            # update the meeting
            session.execute("UPDATE meetings SET name={0}, time={1}, users={2}, notes={3} WHERE id={4};"
                            .format(meeting_obj.name, meeting_obj.time, meeting_obj.users,
                                    meeting_obj.remarks, meeting_obj.id))
        except:
            # rollback if unsuccessful
            session.rollback()
            return False

        # commit if allowed
        session.commit()
        return True
