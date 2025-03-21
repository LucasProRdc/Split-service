import logging
from datetime import datetime
import os
from filesplit.split import Split
import json

from application.utils import get_message_code


class File:
    def __init__(self, path, file_name=None):
        self.logger = logging.getLogger('FileService')
        self.path = path
        self.file_name = self.__create_name(file_name)
        self.list_files_split = []

    @staticmethod
    def __create_name(file_name):
        """
        Função responsavel por criar e retornar o nome do arquivo

        :param file_name:
        :return:
        """
        if file_name is None:
            return datetime.now().strftime('file_%d%m%Y%H%M%S%f.csv')
        else:
            return file_name

    def split(self, size, output_dir):
        """'Splita' o arquivo e retorna uma lista de objetos 'File'"""

        try:
            split = Split(self.path + self.file_name, output_dir)
            split.bysize(size, newline=True, callback=self.add_list_files, includeheader=True)

            self.logger.info(f"Arquivo dividido com sucesso e enviado para: {output_dir}")

        except Exception as e:
            self.logger.error(f"Erro ao dividir arquivo {str(e)}")
            return {'code': get_message_code('error_split_files'), 'description': str(e)}

    def add_list_files(self, f, s):
        """
        Função responsavel por retornar uma lista dos arquivos splitados
        :param f:
        :param s:
        :return:
        """
        position = f.rfind('/')
        file = File(f[:position + 1], f[position + 1:])
        self.list_files_split.append(file)

    def remove_quotation_marks(self):
        """
        Função responsavel por remover as apas duplas do arquivo
        :return:
        """
        try:
            rows = self.__get_rows_file(self)
            file = self.__remove_marks(rows)
            self.__save_in_file(self, file)

        except Exception as e:
            self.logger.error(f'Erro ao remover aspas e salvar arquivo: {str(e)}')
            return {'code': get_message_code('error_remove_quotation_marks'), 'description': str(e)}

    @staticmethod
    def __get_rows_file(self):
        """
        Lê a linha do arquivo
        :param self:
        :return:
        """
        with open(self.path + self.file_name, 'r', encoding='ISO-8859-1') as file:
            rows = file.readlines()

        return rows

    @staticmethod
    def __remove_marks(rows):
        """
        Remove as aspas duplas
        :param rows:
        :return:
        """
        file = []
        for row in rows:
            r = row.strip()

            if r[-1] == '"':
                row = row.replace('","', '|quote|comma|quote')
                row = row.replace(',"', '|comma|quote')
                row = row.replace('",', '|quote|comma')
                row = row.replace('"', '')
                row = row.replace('|quote', '"')
                row = row.replace('|comma', ',')
                row = row.strip()
                row = '"' + row + '"\n'
            else:
                row = row.replace('","', '|quote|comma|quote')
                row = row.replace(',"', '|comma|quote')
                row = row.replace('",', '|quote|comma')
                row = row.replace('"', '')
                row = row.replace('|quote', '"')
                row = row.replace('|comma', ',')
                row = '"' + row
            file.append(row)
        return file

    @staticmethod
    def __save_in_file(self, file):
        """
        salva linha sem aspas duplas em um novo arquivo

        :param self:
        :param file:
        :return:
        """
        with open(self.path + self.file_name, 'w', encoding='ISO-8859-1') as f:
            f.writelines(file)

    def save_dict_in_json(self, dict):
        json_string = json.dumps(str(dict))
        json_file = open(self.path + self.file_name, "w")
        json_file.write(json_string)
        json_file.close()

    def delete_files_split(self):
        """
        Função responsavel por deletar os arquivos splitados

        :return:
        """
        for file in self.list_files_split:
            self.delete_file(file)

    def delete_file(self, file=None):
        """
        Deleta um arquivo

        :param file:
        :return:
        """
        if file is None:
            file = File(self.path, self.file_name)

        try:
            file_path = os.path.join(file.path, file.file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                self.logger.info(f'Arquivo {file.path, file.file_name} deletado com sucesso!')
        except OSError:
            self.logger.error("Error occurred while deleting files.")

    @staticmethod
    def delete_all_files_in_path(log, path):
        try:
            files = os.listdir(path)
            for file in files:
                if os.path.isfile(os.path.join(path, file)):
                    f = File(path, file)
                    f.delete_file()
            if files:
                log.info(f'Diretório {path} vazio!')

        except OSError:
            log.error("Error occurred while deleting files.")

    def count_numbers_row(self):
        rows = self.__get_rows_file(self)
        if len(rows) == 1:
            self.logger.error('Arquivo contem somente uma linha')
            return {'code': get_message_code('error_only_one_row'),
                    'description': 'Arquivo contem somente uma linha'}
        return False
