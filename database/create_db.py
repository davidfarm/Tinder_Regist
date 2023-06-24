import sqlite3


class WorkWithDB:
    def __init__(self):
        self.connection = None
        self.curs = None

    def create_db(self):
        self.connection = sqlite3.connect('database.db')
        self.curs = self.connection.cursor()
        self.curs.execute('CREATE TABLE IF NOT EXISTS accounts(id PRIMARY KEY, start_created_at TEXT,'
                          'is_finish INTEGER, main_mail TEXT, password TEXT,'
                          'second_mail TEXT, geo TEXT, photo_id TEXT, asset_id TEXT )')

        self.connection.commit()
        self.connection.close()

    def start_reg(self, ):
        request = ''
        pass


if __name__ == '__main__':
    db = WorkWithDB()
