from db import get_connection
from datetime import date as dt


def add_transaction(account_id, category_id, amount, type, description, date=None):
    con = get_connection()
    cur = con.cursor()
    delta = amount if type == "income" else -amount
    if amount <= 0:
        print('Amount must be positive')
        return
    with con:
        cur.execute("INSERT INTO transactions (account_id, category_id, amount, type, description, date) VALUES(?,?,?,?,?,?)",
                    (account_id, category_id, amount, type, description, date or str(dt.today())))
        cur.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ? ", (delta, account_id))
    con.close()
    print(f"Transaction added: {type} ${amount:.2f}")


def list_transaction(account_id=None):
    con = get_connection()
    cur = con.cursor()
    b_query = (
        "SELECT t.*, a.name as account_name, c.name as category_name "
        "FROM transactions t "
        "JOIN accounts a ON a.id = t.account_id "
        "LEFT JOIN categories c on c.id = t.category_id")
    if account_id:
        rows = cur.execute(b_query + " WHERE t.account_id = ?",
                           (account_id,)).fetchall()
    else:
        rows = cur.execute(b_query).fetchall()
    con.close()
    if not rows:
        print("No transactions found")
        return

    for row in rows:
        print(
            f"{row['date']} | {row['account_name']} | {row['category_name']} | {row['type']} | ${row['amount']:.2f}")


def delete_transaction(id):
    con = get_connection()
    cur = con.cursor()

    with con:
        row = cur.execute(
            "SELECT account_id, amount, type FROM transactions WHERE id = ?",
            (id,)
        ).fetchone()

        if not row:
            print(f"Transaction {id} not found")
            return

        account_id, amount, type = row["account_id"], row["amount"], row["type"]

        reverse_delta = -amount if type == "income" else amount

        cur.execute("DELETE FROM transactions WHERE id = ?", (id,))

        cur.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (reverse_delta, account_id)
        )

    con.close()
    print(f"Transaction {id} deleted and balance updated")

