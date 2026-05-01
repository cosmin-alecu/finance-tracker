import sqlite3


def get_connection():
    con = sqlite3.connect("finance.db")
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")  # enforce fk constraint
    return con


def init_db():
    con = get_connection()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT"
                ", name TEXT NOT NULL"
                ", type TEXT NOT NULL CHECK(type in ('checking','savings','credit','cash'))"
                ", balance REAL"
                ", created_at TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS categories("
                "id INTEGER PRIMARY KEY AUTOINCREMENT"
                ", name TEXT NOT NULL"
                ", type TEXT NOT NULL CHECK(type in ('income', 'expense'))"
                ")")
    cur.execute("CREATE TABLE IF NOT EXISTS transactions("
                "id INTEGER PRIMARY KEY AUTOINCREMENT"
                ", account_id INTEGER NOT NULL REFERENCES accounts(id)"
                ", category_id INTEGER REFERENCES categories(id)"
                ", amount REAL"
                ", type TEXT NOT NULL CHECK(type IN ('income','expense'))"
                ", description TEXT"
                ", date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS budgets("
                "id INTEGER PRIMARY KEY AUTOINCREMENT"
                ", category_id INTEGER NOT NULL REFERENCES categories(id)"
                ", limit_amount REAL"
                ", month TEXT NOT NULL)")

    con.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
