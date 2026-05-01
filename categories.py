from db import get_connection


def add_category(name, type):
    con = get_connection()
    cur = con.cursor()
    with con:
        cur.execute(
            "INSERT INTO categories (name, type) VALUES (?,?)", (name, type))
    con.close()
    print(f"Category {name} added")


def list_categories():
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM categories").fetchall()
    con.close()
    if not rows:
        print('No categories')
        return

    for row in rows:
        print(
            f"{row['id']} {row['name']} {row['type']}")
