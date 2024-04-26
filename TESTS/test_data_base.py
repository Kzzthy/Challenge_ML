import unittest
from database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(':memory:')  # Usar una base de datos en memoria
        self.db_manager.create_tables()  # Crear las tablas antes de cada prueba

    def tearDown(self):
        self.db_manager.close_connection()

    def test_create_tables(self):
        # Verificar si las tablas existen en la base de datos
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

        # Verificar si la información del archivo se insertó correctamente en la tabla current_files
        inserted_file = self.db_manager.cursor.execute("SELECT * FROM current_files WHERE id='123'").fetchone()
        self.assertIsNotNone(inserted_file)
        self.assertEqual(inserted_file[0], '123')  # id
        self.assertEqual(inserted_file[1], 'file.txt')  # name
        self.assertEqual(inserted_file[2], 'text/plain')  # extension
        self.assertEqual(inserted_file[3], 'User1, User2')  # owner
        self.assertEqual(inserted_file[4], 'Privado')  # shared
        self.assertEqual(inserted_file[5], '2022-04-28 10:00:00')  # last_modified

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

        # Verificar si la información del archivo se insertó correctamente en la tabla public_files_history
        inserted_file = self.db_manager.cursor.execute("SELECT * FROM public_files_history WHERE id='123'").fetchone()
        self.assertIsNotNone(inserted_file)
        self.assertEqual(inserted_file[0], '123')  # id
        self.assertEqual(inserted_file[1], 'file.txt')  # name
        self.assertEqual(inserted_file[2], 'text/plain')  # extension
        self.assertEqual(inserted_file[3], 'User1, User2')  # owner
        self.assertEqual(inserted_file[4], 'Público')  # shared
        self.assertEqual(inserted_file[5], '2022-04-28 10:00:00')  # last_modified

if __name__ == '__main__':
    unittest.main()
