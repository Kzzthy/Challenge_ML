from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow 


class GoogleDriveService:
    def __init__(self, creds_file='credenciales.json'):
        self.creds_file = creds_file

    def obtener_credenciales(self):
        scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send']
        flow = InstalledAppFlow.from_client_secrets_file(self.creds_file, scope)
        creds = flow.run_local_server(port=0)
        return creds

    def inicializar_servicio_drive(self, creds):
        return build('drive', 'v3', credentials=creds)

    def buscar_archivos(self, drive_service):
        response = drive_service.files().list(fields='files(id, name, mimeType, owners, modifiedTime, shared)').execute()
        return response.get('files', [])

    def modificar_visibilidad_archivos(self, drive_service):
        response = drive_service.files().list(fields='files(id, name, permissions)').execute()
        archivos = response.get('files', [])
        modificaciones_realizadas = False
        archivos_publicos_encontrados = False  # Variable para verificar si se encontraron archivos públicos

        for archivo in archivos:
            file_id = archivo['id']
            file_name = archivo['name']  
            permissions = archivo.get('permissions', [])
            
            for permission in permissions:
                if permission.get('role', '') == 'reader' and permission.get('type', '') == 'anyone':
                    archivos_publicos_encontrados = True
                    drive_service.permissions().delete(fileId=file_id, permissionId=permission['id']).execute()
                    print(f"El archivo '{file_name}' ha cambiado de público a privado.")
                    modificaciones_realizadas = True
                    break
        
        if not archivos_publicos_encontrados:
            print("-" * 30 + " No se encontraron archivos publicos " + "-" * 30)

        return modificaciones_realizadas
