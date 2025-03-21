from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import logging

from config import config
from config.database_config import configure_database
from application.constants import ARGENTINA, URUGUAY, ARGENTINA_JOB, URUGUAY_JOB
from application.core import Core
from application.scheduler import Scheduler


app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename=config.FILE_LOG, format="%(asctime)s - %(levelname)s - %(message)s")
app.logger.info('Aplicação sendo iniciada.')

configure_database(app)

if config.SCHEDULER_ON:
    Scheduler(config.CRON_EXPRESSION, Core(URUGUAY, app).execute_split_to_scheduler, URUGUAY_JOB).start()
    Scheduler(config.CRON_EXPRESSION, Core(ARGENTINA, app).execute_split_to_scheduler, ARGENTINA_JOB).start()

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user, password):
    if user in config.USERS_APP and config.USERS_APP[user] == password:
        return user


@app.before_request
def validation_hostname():
    if request.headers.get('Host').split(":")[0] != config.ALLOWED_HOSTNAME:
        return "Acesso negado. Somente permitido a partir de {}".format(config.ALLOWED_HOSTNAME), 403


@app.route('/execute_split', methods=['GET'])
@auth.login_required
def execute():
    country = request.args.get('country')
    response = Core(country, app).execute_split()
    return jsonify(response)


@app.route('/get_messages_list', methods=['GET'])
@auth.login_required
def get_messages_list():
    return jsonify(config.LIST_MESSAGES)


if __name__ == '__main__':
    app.run(port=config.PORT)
