from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging


class Scheduler:
    def __init__(self, cron_expression: str, job_function: callable, name_job: str):
        self.logger = logging.getLogger('Scheduler')
        self.cron_expression = cron_expression
        self.job_function = job_function
        self.name_job = name_job

    def start(self) -> None:
        """
        Função responsável por iniciar o processo de scheduler conforme expressão cron informada como
        atributo ('cron_expression') na função também informada como atributo ('job_function').
        - Somente executa se a configuração SCHEDULER_ON em config estiver == True.
        """

        self.logger.info(f"Scheduler sendo iniciado {self.name_job}")
        scheduler = BackgroundScheduler()
        trigger = CronTrigger.from_crontab(self.cron_expression)
        scheduler.add_job(self.job_function, trigger=trigger, name=self.name_job)
        scheduler.start()
