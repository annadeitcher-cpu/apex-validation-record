from db import get_connection

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute(
            "insert into accounts (name, industry) values (%s, %s) returning id",
            ("Roundtrip Test Co", "Test"),
        )
        account_id = cur.fetchone()[0]

        cur.execute("select id, name, industry from accounts where id = %s", (account_id,))
        row = cur.fetchone()
        print("inserted + selected:", row)

        cur.execute("delete from accounts where id = %s", (account_id,))
        conn.commit()

        cur.execute("select id from accounts where id = %s", (account_id,))
        print("after delete:", cur.fetchone())
