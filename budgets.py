from db import get_connection
from datetime import date as dt


def set_budget(category_id, limit_amount, month=None):
    con = get_connection()
    cur = con.cursor()
    with con:
        cur.execute("INSERT OR REPLACE INTO budgets (category_id, limit_amount, month) VALUES(?,?,?)",
                    (category_id, limit_amount, month or dt.today().strftime('%Y-%m')))


def list_budgets(month=None):
    con = get_connection()
    cur = con.cursor()
    with con:
        rows = cur.execute("SELECT b.*, c.name as category_name, "
                           "COALESCE(SUM(t.amount),0) as spent "
                           "FROM BUDGETS b "
                           "JOIN categories c on c.id = b.category_id "
                           "LEFT JOIN transactions as t ON t.category_id = b.category_id "
                           "AND t.type ='expense' "
                           "AND strftime('%Y-%m', t.date) = b.month "
                           "WHERE b.month = ? "
                           "GROUP BY b.id", (month or dt.today().strftime('%Y-%m'),)).fetchall()
    con.close()

    for row in rows:
        pct = (row['spent'] / row['limit_amount']) * 100
        print(
            f"{row['category_name']}: ${row['spent']:.2f} / ${row['limit_amount']:.2f} ({pct:.0f}%)")
