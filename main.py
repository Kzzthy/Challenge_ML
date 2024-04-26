import os.path
import time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from database_manager import DatabaseManager
from google_drive_service import GoogleDriveService
from email_service import EmailService

MAX_SESSION_DURATION = 15 * 60

def main():
    db_manager = DatabaseManager()
    google_drive_service = GoogleDriveService()

    token_path = 'token.json'

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)
    
    if not creds or not creds.valid:
        creds = google_drive_service.obtener_credenciales()
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    if creds.expired and creds.valid:
        creds.refresh(Request())

    if 'expiry' in creds.token and time.time() > creds.token['expiry'] - MAX_SESSION_DURATION:
        creds.refresh(Request())

    drive_service = google_drive_service.inicializar_servicio_drive(creds)

    archivos = google_drive_service.buscar_archivos(drive_service)
    if not archivos:
        print("No hay archivos públicos en Google Drive.")
        return

    for archivo in archivos:
        db_manager.create_tables()
        db_manager.insert_current_file_info(archivo)

    modificaciones_realizadas = google_drive_service.modificar_visibilidad_archivos(drive_service)
    if modificaciones_realizadas:
        email_service = EmailService()
        db_manager.cursor.execute('SELECT DISTINCT owner FROM current_files')
        owner = db_manager.cursor.fetchone()[0]
        destinatario = owner
        asunto = 'Modificación en Google Drive'
        cuerpo = 'Se han realizado modificaciones en tu Google Drive. Por favor, verifica los cambios.'
        email_service.enviar_correo(destinatario, asunto, cuerpo, creds)

    db_manager.close_connection()

if __name__ == "__main__":
    print("*" * 35 + " Challenge Mercado Libre " + "*" * 35)
    main()
