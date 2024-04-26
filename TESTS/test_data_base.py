import unittest
from database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(':memory:')  
        self.db_manager.create_tables()  

    def tearDown(self):
        self.db_manager.close_connection()

    def test_create_tables(self):
        current_files_table = self.db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='current_files'").fetchone()
        self.assertIsNotNone(current_files_table)

        public_files_history_table = self.db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='public_files_history'").fetchone()
        self.assertIsNotNone(public_files_history_table)

    def test_insert_current_file_info(self):
        file_info = {
            'id': '123',
            'name': 'file.txt',
            'mimeType': 'text/plain',
            'owners': [{'displayName': 'User1'}, {'displayName': 'User2'}],
            'shared': False,
            'modifiedTime': '2022-04-28 10:00:00'
        }

        self.db_manager.insert_current_file_info(file_info)

        
        inserted_file = self.db_manager.cursor.execute("SELECT * FROM current_files WHERE id='123'").fetchone()
        self.assertIsNotNone(inserted_file)
        self.assertEqual(inserted_file[0], '123')  
        self.assertEqual(inserted_file[1], 'file.txt')
        self.assertEqual(inserted_file[2], 'text/plain')  
        self.assertEqual(inserted_file[3], 'User1, User2') 
        self.assertEqual(inserted_file[4], 'Privado')  
        self.assertEqual(inserted_file[5], '2022-04-28 10:00:00') 

    def test_insert_public_files_history(self):
        file_info = {
            'id': '123',
            'name': 'file.txt',
            'mimeType': 'text/plain',
            'owners': [{'displayName': 'User1'}, {'displayName': 'User2'}],
            'shared': True,
            'modifiedTime': '2022-04-28 10:00:00'
        }

        self.db_manager.insert_public_files_history(file_info)

        
        inserted_file = self.db_manager.cursor.execute("SELECT * FROM public_files_history WHERE id='123'").fetchone()
        self.assertIsNotNone(inserted_file)
        self.assertEqual(inserted_file[0], '123')  
        self.assertEqual(inserted_file[1], 'file.txt') 
        self.assertEqual(inserted_file[2], 'text/plain')  
        self.assertEqual(inserted_file[3], 'User1, User2')  
        self.assertEqual(inserted_file[4], 'Público') 
        self.assertEqual(inserted_file[5], '2022-04-28 10:00:00')  

if __name__ == '__main__':
    unittest.main()
