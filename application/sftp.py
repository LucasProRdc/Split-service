import logging
import paramiko
from typing import List

from config import config
from application.file import File
from application.utils import get_message_code


class Sftp:
    def __init__(self, host, username, private_key):
        self.logger = logging.getLogger('SFTPService')
        self.host = host
        self.username = username
        self.private_key = private_key
        self.sshc = None
        self.sftp = None
        self.file_download = None

    def connect(self):
        """
        Função responsável por criar a conexão via SFTP

        """
        try:
            key = paramiko.RSAKey.from_private_key_file(self.private_key)
            self.sshc = paramiko.SSHClient()
            self.sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.logger.info(f"Conectando a {self.host} via SFTP...")
            self.sshc.connect(hostname=self.host, username=self.username, pkey=key)
            self.sftp = self.sshc.open_sftp()
            self.logger.info(f"Conectado a {self.host} via SFTP")

        except paramiko.AuthenticationException as e:
            self.logger.error(f"Erro de autenticação SSH: {e}")
            return {'code': get_message_code('error_auth'), 'description': str(e)}

        except Exception as e:
            self.logger.error(f"Não foi possível conectar a {self.host} via SFTP", exc_info=e)
            return {'code': get_message_code('error_connection_sftp'), 'description': str(e)}

    def disconnect(self):
        """
        Função responsavel por  fechar a conexão SFTP

        """
        if self.sshc is not None:
            self.sshc.close()
            self.logger.info(f"Desconectado de {self.host}")

    def download_file(self, remote_path, local_path):
        """
        Função responsavel por fazer o download do arquivo e o retornar

        :param remote_path:
        :param local_path:
        :return:
        """
        try:
            file = File(path=local_path)
            self.logger.info(f"Baixando arquivo {remote_path} via SFTP...")
            self.sftp.get(remote_path, file.path + file.file_name)
            self.logger.info(f"Arquivo {remote_path} baixado para {local_path}")
            self.file_download = file

        except Exception as e:
            self.logger.error(f"Erro ao baixar arquivo: {str(e)}")
            return {'code': get_message_code('error_download'), 'description': str(e)}

    def upload_files(self, files: List[File], remote_path):
        for file in files:
            response = self.__upload_file(file, remote_path)
            if response:
                return response

    def __upload_file(self, file, remote_path):
        """
        Função responsavel por fazer o upload da lista de arquivos recebido como parametro
        :param files:
        :param remote_path:
        :return:
        """
        try:
            self.logger.info(f"Enviando {file.file_name} via SFTP...")
            self.sftp.put(file.path + file.file_name, remote_path + file.file_name)
            self.logger.info(f"Arquivo {file.file_name} enviado para {remote_path}")

        except Exception as e:
            self.logger.error(f"Erro ao enviar arquivo: {str(e)}")
            return {'code': get_message_code('error_send_file'), 'description': str(e)}

    @staticmethod
    def __get_error_code(error_name):
        return config.LIST_MESSAGES[error_name]
