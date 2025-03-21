from datetime import datetime, timedelta
import logging

from config import config
from application import constants
from application.sftp import Sftp
from application.file import File
from application.utils import get_message_code
from application.models import ControlSftp, db


class Core:

    def __init__(self, country, app):
        self.logger = logging.getLogger('Core')
        self.__configure_country(country)
        self.country = country
        self.SUCCESS = "success"
        self.app = app

    def __configure_country(self, country):
        match country:
            case constants.URUGUAY:
                self.__sftp = Sftp(config.HOST_UY, config.USER_UY, config.KEY_UY)
                self.__remote_path_file_download = config.REMOTE_PATH_FILE_DOWNLOAD_UY
                self.__local_path = config.LOCAL_PATH_UY
                self.__remote_path_file_upload = config.REMOTE_PATH_FILE_UPLOAD_UY
                self.__control_file = config.CONTROL_FILE_UY

            case constants.ARGENTINA:
                self.__sftp = Sftp(config.HOST_AR, config.USER_AR, config.KEY_AR)
                self.__remote_path_file_download = config.REMOTE_PATH_FILE_DOWNLOAD_AR
                self.__local_path = config.LOCAL_PATH_AR
                self.__remote_path_file_upload = config.REMOTE_PATH_FILE_UPLOAD_AR
                self.__control_file = config.CONTROL_FILE_AR

    def execute_split(self):
        """
        Responsável por executar toda a regra de negócio da aplicação.
        - download do arquivo principal;
        - split do arquivo em arquivos menores; e
        - envio dos arquivos menores via SFTP.
        :return:
        """
        self.logger.info(f"Iniciando processo de Split para {self.country}")

        response = self.__sftp.connect()
        if response:
            return response

        response = self.__sftp.download_file(self.__remote_path_file_download, self.__local_path)
        if response:
            return response

        file = self.__sftp.file_download

        response = file.count_numbers_row()
        if response:
            return response

        response = file.remove_quotation_marks()
        if response:
            file.delete_file()
            return response

        response = file.split(config.SPLIT_SIZE, config.LOCAL_SPLITTER_PATH)
        file.delete_file()
        if response:
            return response

        response = self.__sftp.upload_files(file.list_files_split, self.__remote_path_file_upload)
        file.delete_files_split()
        if response:
            return response

        date_now = datetime.now()
        response_success = {'code': get_message_code('success'),
                            'description': 'success',
                            'date': str(date_now),
                            'file': file.file_name
                            }
        control_file = File(config.LOCAL_SPLITTER_PATH, file.file_name + self.__control_file)
        control_file.save_dict_in_json(response_success)

        response = self.__sftp.upload_files([control_file], self.__remote_path_file_upload)
        control_file.delete_file()
        if response:
            return response

        self.__register_success_in_db(date_now)
        self.__sftp.disconnect()

        return response_success

    def execute_split_to_scheduler(self):
        with self.app.app_context():
            if self.__is_execute_necessary():
                self.execute_split()

    def __is_execute_necessary(self):
        """
        Verifica se já houve processo executado, conforme registro no banco de dados na tabela 'ControlSftp', após
        o horário parametrizado na constante HOUR_NEW_FILE_SERVER.
        :return:
        """
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        hour_new_file_server = config.HOUR_NEW_FILE_SERVER

        register = ControlSftp.query.get(self.country)

        if register is None:
            return True

        date_last_send = register.date

        # se hora atual depois da hour_new_file_server
        if today.hour > hour_new_file_server:
            # se último processamento é de hoje antes do hour_new_file_server
            if self.__is_same_day(today, date_last_send) and date_last_send.hour < hour_new_file_server:
                return True

            # se qualquer dia antes de hoje
            if self.__is_day_before(today, date_last_send):
                return True

        # se hora atual antes de hour_new_file_server
        if today.hour < hour_new_file_server:
            # se último processamento é de ontem antes do hour_new_file_server
            if self.__is_same_day(yesterday, date_last_send) and date_last_send.hour < hour_new_file_server:
                return True

            # se qualquer dia antes de ontem
            if self.__is_day_before(yesterday, date_last_send):
                return True

        return False

    @staticmethod
    def __is_same_day(date_1, date_2):
        """
        Compara se as duas datas são iguais em relação a dia,mês e ano.
        :param date_1: data de referência
        :param date_2: data a ser comparada
        :return:
        """
        date_1_in_day = datetime(date_1.year, date_1.month, date_1.day)
        date_2_in_day = datetime(date_2.year, date_2.month, date_2.day)

        if date_1_in_day == date_2_in_day:
            return True
        return False

    @staticmethod
    def __is_day_before(date_1, date_2):
        """
        Compara se date_2 é anterior ao date_1 em relação a dia, mês e ano.
        :param date_1: data de referência
        :param date_2: data a ser comparada se é anterior à data de referência
        :return:
        """
        date_1_in_day = datetime(date_1.year, date_1.month, date_1.day)
        date_2_in_day = datetime(date_2.year, date_2.month, date_2.day)

        if date_1_in_day > date_2_in_day:
            return True
        return False

    def __register_success_in_db(self, date_now):
        register = ControlSftp.query.get(self.country)
        if register is None:
            new_register = ControlSftp(
                country=self.country,
                date=date_now,
                message=self.SUCCESS,
                file_name=self.__sftp.file_download.file_name)
            db.session.add(new_register)
            db.session.commit()
        else:
            register.date = date_now
            register.message = self.SUCCESS
            register.file_name = self.__sftp.file_download.file_name
            db.session.commit()
