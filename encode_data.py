import sqlite3
import csv
import json
from datetime import datetime
from pathlib import Path

con = sqlite3.connect('data.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS tickers(isin TEXT, ticker TEXT, UNIQUE(isin, ticker))")
cur.execute("""
    CREATE TABLE IF NOT EXISTS 
        pricing(ticker TEXT, date TEXT, open REAL, high REAL, low REAL, close REAL, 
                UNIQUE(ticker, date))
""")

with open('data/tickers.json', 'r') as f:
    tickers = json.load(f)
    
for isin, ticker in tickers.items():
    # c.execute("INSERT INTO events (name, event_date) VALUES (?, ?)", ('Sample Event', formatted_date))
    cur.execute(f"""
        INSERT OR IGNORE INTO tickers VALUES(?, ?)
    """, (isin, ticker))

    with open(f'data/{isin}-{ticker}.csv', 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            date = datetime.fromisoformat(row['Date'])

            # TODO: dividends row
            if row['Open'] == '':
                continue
            
            cur.execute("""
                INSERT OR IGNORE INTO pricing
                VALUES(?, ?, ?, ?, ?, ?)
            """, (
                ticker,
                date.date().isoformat(),
                float(row['Open']),
                float(row['High']),
                float(row['Low']),
                float(row['Close']),
            ))

    con.commit()

con.close()