import sqlite3


class Banking:
    database = "accounts.db"
    table = "accounts"
    def __init__(self):
        self.account_data = ()

    @staticmethod
    def db_connect(f):
        def open(self, *args):
            con = sqlite3.connect(self.database)
            cur = con.cursor()
            try:
                res = f(self, *args, cursor=cur)
            except Exception:
                con.rollback()
                print("Failed to interact with database!")
                raise
            else:
                con.commit()
            finally:
                con.close()
            return res
        return open

    @db_connect
    def find_account(self, id, email, **kwargs):
        cur = kwargs.pop("cursor")
        if not id and not email:
            return False
        data = (id, email)
        res = cur.execute(f'''
            SELECT 1 FROM {self.table} WHERE AccountNumber = ? OR Email = ?
        ''', data)
        res = res.fetchone()
        return bool(res)

    @db_connect
    def login(self, passcode, id=0, email="", **kwargs):
        if not self.find_account(id, email):
            return False
        cur = kwargs.pop("cursor")
        data = (id, email)
        res = cur.execute(f'''
            SELECT * FROM {self.table} WHERE AccountNumber = ? OR Email = ?
        ''', data)
        res = res.fetchone()
        if passcode != res[4]:
            return False
        else:
            self.account_data = res
            return True
    
    @db_connect
    def create_account(self, email, first_name, last_name, passcode, **kwargs):
        if self.find_account(0, email):
            return False
        cur = kwargs.pop("cursor")
        data = (email, first_name, last_name, passcode)
        self.account_data = data
        cur.execute(f'''
            INSERT INTO {self.table} (Email, FirstName, LastName, Passcode)
                VALUES (?, ?, ?, ?)
        ''', data)
        self.account_data = (cur.lastrowid,) + data
        return True

    @db_connect
    def delete_account(self, passcode, **kwargs):
        cur = kwargs.pop("cursor")
        data = self.account_data
        if not data:
            return False
        res = cur.execute(f'''
            SELECT Passcode FROM {self.table} WHERE AccountNumber = ?
        ''', (data[0],))
        res = res.fetchone()
        if passcode != res[0]:
            return False
        cur.execute(f'''
            DELETE FROM {self.table} WHERE AccountNumber = ?
        ''', (data[0],))
        return True

"""
conn = sqlite3.connect('accounts.db')  
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE accounts(
             AccountNumber integer primary key, 
             Email varchar(255), 
             FirstName varchar(255), 
             LastName varchar(255), 
             Passcode varchar(255), 
             Balance integer DEFAULT 0
             )''')
conn.commit()
conn.close()
"""
