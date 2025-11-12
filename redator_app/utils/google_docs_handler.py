"""
Google Docs Handler
Gerencia a criação e formatação de documentos no Google Docs
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

class GoogleDocsHandler:
    """Gerencia integração com Google Docs e Drive"""
    
    # Escopos necessários
    SCOPES = [
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/drive.file'
    ]
    
    def __init__(self, credentials_path: str = None):
        """
        Inicializa o handler do Google Docs
        
        Args:
            credentials_path: Caminho para o arquivo credentials.json
        """
        if credentials_path is None:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'config/credentials.json')
        
        self.credentials_path = credentials_path
        self.creds = None
        self.docs_service = None
        self.drive_service = None
        self._autenticar()
    
    def _autenticar(self):
        """Autentica com Google APIs usando OAuth2"""
        token_path = Path('config/token.json')
        
        # Verificar se já tem token salvo
        if token_path.exists():
            self.creds = Credentials.from_authorized_user_file(str(token_path), self.SCOPES)
        
        # Se não tem credenciais válidas, fazer login
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not Path(self.credentials_path).exists():
                    raise FileNotFoundError(
                        f"Arquivo de credenciais não encontrado: {self.credentials_path}\n"
                        "Por favor, siga as instruções em GOOGLE_API_SETUP.md para configurar."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Salvar token para próximas execuções
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
        
        # Criar serviços
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
    
    def criar_documento(
        self, 
        titulo: str, 
        conteudo: str, 
        imagem_path: str = None
    ) -> str:
        """
        Cria um novo documento no Google Docs com formatação
        
        Args:
            titulo: Título do documento
            conteudo: Conteúdo em Markdown
            imagem_path: Caminho para a imagem de destaque (opcional)
            
        Returns:
            str: URL do documento criado
        """
        
        # Criar documento vazio
        doc = self.docs_service.documents().create(body={'title': titulo}).execute()
        document_id = doc.get('documentId')
        
        # Preparar requisições de formatação
        requests = []
        
        # 1. Inserir imagem (se fornecida)
        if imagem_path and Path(imagem_path).exists():
            # Fazer upload da imagem para o Drive
            image_url = self._upload_imagem(imagem_path)
            
            if image_url:
                requests.append({
                    'insertInlineImage': {
                        'location': {'index': 1},
                        'uri': image_url,
                        'objectSize': {
                            'height': {'magnitude': 300, 'unit': 'PT'},
                            'width': {'magnitude': 600, 'unit': 'PT'}
                        }
                    }
                })
                
                # Adicionar quebra de linha após imagem
                requests.append({
                    'insertText': {
                        'location': {'index': 1},
                        'text': '\n\n'
                    }
                })
        
        # 2. Converter Markdown para formato Google Docs
        formatted_requests = self._markdown_para_docs(conteudo, 1)
        requests.extend(formatted_requests)
        
        # Executar todas as formatações
        if requests:
            self.docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
        
        # Retornar URL do documento
        return f"https://docs.google.com/document/d/{document_id}/edit"
    
    def _upload_imagem(self, imagem_path: str) -> str:
        """Faz upload da imagem para o Google Drive e retorna a URL"""
        try:
            file_metadata = {
                'name': Path(imagem_path).name,
                'mimeType': 'image/png'
            }
            
            media = MediaFileUpload(
                imagem_path,
                mimetype='image/png',
                resumable=True
            )
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink, webContentLink'
            ).execute()
            
            # Tornar arquivo público (somente leitura)
            self.drive_service.permissions().create(
                fileId=file.get('id'),
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
            
            # Retornar URL direta da imagem
            file_id = file.get('id')
            return f"https://drive.google.com/uc?export=view&id={file_id}"
            
        except Exception as e:
            print(f"Erro ao fazer upload da imagem: {e}")
            return None
    
    def _markdown_para_docs(self, markdown: str, start_index: int) -> list:
        """
        Converte Markdown para requisições do Google Docs API
        
        Args:
            markdown: Texto em Markdown
            start_index: Índice inicial para inserção
            
        Returns:
            list: Lista de requisições para a API
        """
        requests = []
        linhas = markdown.split('\n')
        current_index = start_index
        
        for linha in linhas:
            if not linha.strip():
                # Linha vazia - adicionar quebra
                requests.append({
                    'insertText': {
                        'location': {'index': current_index},
                        'text': '\n'
                    }
                })
                current_index += 1
                continue
            
            # Detectar tipo de linha e formatar
            texto_limpo = linha.strip()
            
            # Headers
            if texto_limpo.startswith('# '):
                texto = texto_limpo[2:] + '\n'
                start = current_index
                requests.append({'insertText': {'location': {'index': current_index}, 'text': texto}})
                current_index += len(texto)
                # Formatar como H1
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': current_index - 1},
                        'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                        'fields': 'namedStyleType'
                    }
                })
            
            elif texto_limpo.startswith('## '):
                texto = texto_limpo[3:] + '\n'
                start = current_index
                requests.append({'insertText': {'location': {'index': current_index}, 'text': texto}})
                current_index += len(texto)
                # Formatar como H2
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': current_index - 1},
                        'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                        'fields': 'namedStyleType'
                    }
                })
            
            elif texto_limpo.startswith('### '):
                texto = texto_limpo[4:] + '\n'
                start = current_index
                requests.append({'insertText': {'location': {'index': current_index}, 'text': texto}})
                current_index += len(texto)
                # Formatar como H3
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': start, 'endIndex': current_index - 1},
                        'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                        'fields': 'namedStyleType'
                    }
                })
            
            # Lista com marcadores
            elif texto_limpo.startswith('- ') or texto_limpo.startswith('* '):
                texto = '• ' + texto_limpo[2:] + '\n'
                requests.append({'insertText': {'location': {'index': current_index}, 'text': texto}})
                current_index += len(texto)
            
            # Lista numerada
            elif texto_limpo[0].isdigit() and texto_limpo[1:3] == '. ':
                texto = texto_limpo + '\n'
                requests.append({'insertText': {'location': {'index': current_index}, 'text': texto}})
                current_index += len(texto)
            
            # Texto normal
            else:
                texto = linha + '\n'
                requests.append({'insertText': {'location': {'index': current_index}, 'text': texto}})
                current_index += len(texto)
        
        return requests
    
    def listar_documentos(self, limite: int = 10) -> list:
        """Lista os últimos documentos criados"""
        try:
            results = self.drive_service.files().list(
                pageSize=limite,
                fields="files(id, name, createdTime, webViewLink)",
                q="mimeType='application/vnd.google-apps.document'",
                orderBy="createdTime desc"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            print(f"Erro ao listar documentos: {e}")
            return []

