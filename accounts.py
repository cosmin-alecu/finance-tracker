from db import get_connection
from datetime import date


def add_account(name, type, balance):
    con = get_connection()
    cur = con.cursor()
    with con:
        cur.execute(
            "INSERT INTO accounts (name, type, balance, created_at) VALUES (?,?,?,?)", (name, type, balance, str(date.today())))
    con.close()
    print(f"Account '{name}' created")


def list_accounts():
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM accounts").fetchall()
    con.close()
    if not rows:
        print('No accounts')
        return

    for row in rows:
        print(
            f"{row['id']} {row['name']} {row['type']} {row['balance']} {row['created_at']}")


def delete_account(id):
    con = get_connection()
    cur = con.cursor()
    with con:
        cur.execute("DELETE FROM accounts WHERE id = ?", (id,))
    con.close()
    print(f"Account {id} deleted")
