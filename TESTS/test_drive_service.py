import unittest
from unittest.mock import MagicMock, patch
from google_drive_service import GoogleDriveService

class TestGoogleDriveService(unittest.TestCase):

    def setUp(self):
        self.gdrive_service = GoogleDriveService(creds_file='test_credenciales.json')

    @patch('google_drive_service.InstalledAppFlow.from_client_secrets_file')
    def test_obtener_credenciales(self, mock_flow):

        mock_creds = MagicMock()
        mock_flow.return_value.run_local_server.return_value = mock_creds

        creds = self.gdrive_service.obtener_credenciales()

        self.assertEqual(creds, mock_creds)

    @patch('google_drive_service.build')
    def test_inicializar_servicio_drive(self, mock_build):
        mock_drive_service = MagicMock()
        mock_build.return_value = mock_drive_service

        servicio_drive = self.gdrive_service.inicializar_servicio_drive('mocked_credentials')

        self.assertEqual(servicio_drive, mock_drive_service)

    @patch('google_drive_service.build')
    def test_buscar_archivos(self, mock_build):
        mock_drive_service = MagicMock()
        mock_files_response = {'files': [{'id': '123', 'name': 'archivo1.txt'}, {'id': '456', 'name': 'archivo2.txt'}]}
        mock_drive_service.files().list().execute.return_value = mock_files_response
        mock_build.return_value = mock_drive_service

        archivos = self.gdrive_service.buscar_archivos(mock_drive_service)

        self.assertEqual(archivos, mock_files_response['files'])

    @patch('google_drive_service.build')
    @patch('builtins.input', side_effect=['s', 'n'])
    def test_modificar_visibilidad_archivos(self, mock_input, mock_build):
        mock_drive_service = MagicMock()
        mock_files_response = {'files': [{'id': '123', 'name': 'archivo1.txt', 'permissions': [{'role': 'reader', 'type': 'anyone', 'id': 'perm_id'}]}]}
        mock_drive_service.files().list().execute.return_value = mock_files_response
        mock_build.return_value = mock_drive_service

        modificaciones_realizadas = self.gdrive_service.modificar_visibilidad_archivos(mock_drive_service)

        self.assertTrue(modificaciones_realizadas)

if __name__ == '__main__':
    unittest.main()



