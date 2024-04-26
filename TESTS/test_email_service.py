import unittest
from unittest.mock import MagicMock, patch
from email_service import EmailService

class TestEmailService(unittest.TestCase):
    @patch('email_service.build')
    def test_enviar_correo(self, mock_build):
        destinatario = 'destinatario@example.com'
        asunto = 'Asunto del correo'
        cuerpo = 'Cuerpo del correo'
        creds = 'mocked_credentials'

        mock_service = MagicMock()
        mock_build.return_value = mock_service

        email_service = EmailService()

        email_service.enviar_correo(destinatario, asunto, cuerpo, creds)
        mock_service.users().messages().send.assert_called_once()

    def test_crear_mensaje(self):
        sender = 'sender@example.com'
        destinatario = 'destinatario@example.com'
        asunto = 'Asunto del mensaje'
        cuerpo = 'Cuerpo del mensaje'
        email_service = EmailService()
        mensaje = email_service.crear_mensaje(sender, destinatario, asunto, cuerpo)
        self.assertIn('raw', mensaje)
        self.assertIsInstance(mensaje['raw'], str)

    @patch('email_service.build')
    def test_enviar_mensaje(self, mock_build):
        service = MagicMock()
        user_id = 'me'
        message = {'raw': 'mocked_raw_message'}

        mock_service = MagicMock()
        mock_service.users().messages().send.return_value.execute.return_value = {'id': 'mocked_message_id'}
        mock_build.return_value = mock_service

        email_service = EmailService()

        message_id = email_service.enviar_mensaje(service, user_id, message)

        self.assertEqual(message_id, 'mocked_message_id')

if __name__ == '__main__':
    unittest.main()
