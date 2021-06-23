import sqlite3


def connect():
    return sqlite3.connect("database.db")



def getAllLinks(table):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    info = cursor.fetchall()
    conn.close()
    return info


def getCurrentLink(id, table):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE id = '{id}'")
    info = cursor.fetchone()
    conn.close()
    return info
