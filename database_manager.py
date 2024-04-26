import sqlite3

class DatabaseManager:
    def __init__(self, db_file='ChallengeML.db'):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.conn.commit()
        
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS current_files (
                id TEXT PRIMARY KEY,
                name TEXT,
                extension TEXT,
                owner TEXT,
                shared TEXT,
                last_modified TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS public_files_history (
                id TEXT,
                name TEXT,
                extension TEXT,
                owner TEXT,
                shared TEXT,
                last_modified TEXT
            )
        ''')
        self.conn.commit()

    def insert_current_file_info(self, file_info):
        owners = ", ".join(owner['displayName'] for owner in file_info.get('owners', []))
        shared = 'Privado' if not file_info.get('shared', False) else 'Público'
        self.cursor.execute('INSERT OR REPLACE INTO current_files (id, name, extension, owner, shared, last_modified) VALUES (?, ?, ?, ?, ?, ?)',
                            (file_info['id'], file_info['name'], file_info.get('mimeType', ''), owners, shared, file_info.get('modifiedTime', '')))
        self.conn.commit()


        if shared == 'Público':
            self.cursor.execute('SELECT * FROM public_files_history WHERE id=?', (file_info['id'],))
            existing_public_file = self.cursor.fetchone()
            if not existing_public_file:
                self.insert_public_files_history(file_info)

    def insert_public_files_history(self, file_info):
        owners = ", ".join(owner['displayName'] for owner in file_info.get('owners', []))
        self.cursor.execute('INSERT INTO public_files_history VALUES (?, ?, ?, ?, ?, ?)',
                            (file_info['id'], file_info['name'], file_info.get('mimeType', ''), owners, 'Público', file_info.get('modifiedTime', '')))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
