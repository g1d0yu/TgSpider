import sqlite3
import sys
import datetime

import pytz as pytz

##from datetime import datetime, timedelta
class RecoderUtil:
    def __init__(self):
        self.conn = sqlite3.connect('recoder.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            query = f"CREATE TABLE IF NOT EXISTS last_run_time (user_id INTEGER PRIMARY KEY,last_run_time DATETIME);"
            self.conn.cursor().execute(query)

    def get_last_run_time(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT last_run_time FROM last_run_time WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except:
            return None

    def update_last_run_time(self,user_id, new_time):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                        INSERT INTO last_run_time (user_id, last_run_time) VALUES (?, ?)
                        ON CONFLICT(user_id) DO UPDATE SET last_run_time=excluded.last_run_time;
                    """, (user_id, new_time))

if __name__ == "__main__":
    recoder = RecoderUtil()
    curr = datetime.datetime.now().replace(microsecond=0)
    now = curr.astimezone(datetime.timezone.utc)

    last = recoder.get_last_run_time(222)
    recoder.update_last_run_time(222,now)
    print(type(last))
    from datetime import datetime

    tod = datetime.today().replace(microsecond=0)
    tod1 = tod.astimezone(pytz.utc)
    dt = datetime.fromisoformat(last)
    print(dt)
    print(type(dt))
    pass