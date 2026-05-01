from db import get_connection
from datetime import date as dt


def monthly_summary(month=None):
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT c.name as category, t.type, SUM(t.amount) as total "
                       "FROM transactions t "
                       "LEFT JOIN categories c ON c.id = t.category_id "
                       "WHERE strftime('%Y-%m', t.date) = ? "
                       "GROUP BY t.category_id, t.type", (month or dt.today().strftime(
                           '%Y-%m'),)).fetchall()
    con.close()

    if not rows:
        print('No transactions found for this month')
        return

    for row in rows:
        print(f"{row['category']}: ${row['total']:.2f} ({row['type']})")

    total_income = sum(r['total'] for r in rows if r['type'] == 'income')
    total_expenses = sum(r['total'] for r in rows if r['type'] == 'expense')
    net = total_income - total_expenses

    return {
        "income": total_income,
        "expenses": total_expenses,
        "net": net,
        "rows": [dict(r) for r in rows]
    }
