def connection():
    import psycopg2
    conn = psycopg2.connect(
                host='gws-finance-non-prod.ct9chwaushor.us-east-1.rds.amazonaws.com',
                database='gws_finance',
                user='gws_finance_app_admin',
                password='RkxndFy6@U'
                )
    cur = conn.cursor()
    return conn, cur
