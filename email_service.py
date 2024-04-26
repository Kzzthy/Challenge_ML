from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


class EmailService:
    def enviar_correo(self, destinatario, asunto, cuerpo, creds):
        service = build('gmail', 'v1', credentials=creds)
        message = self.crear_mensaje("ml.challenge.mc@gmail.com", "ml.challenge.mc@gmail.com", asunto, cuerpo) #MODIFICAR eMail 
        self.enviar_mensaje(service, "me", message)

    def crear_mensaje(self, sender, destinatario, asunto, cuerpo):
        message = MIMEText(cuerpo)
        message['to'] = destinatario
        message['from'] = sender
        message['subject'] = asunto
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def enviar_mensaje(self, service, user_id, message):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print('------------------- Se envió un correo a el owner informado las modificaciones ---------------------')
        except Exception as e:
            print(f'Error al enviar el correo: {str(e)}')