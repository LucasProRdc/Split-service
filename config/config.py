# FLASK config
PORT = '5000'
FILE_LOG = 'logs/app.log'
#   Dev
ALLOWED_HOSTNAME = "localhost"

# SCHEDULER
CRON_EXPRESSION = '0 * * * *'
#   Horário que o novo arquivo é criado no servidor do cliente:
HOUR_NEW_FILE_SERVER = 17
SCHEDULER_ON = False

# SFTP URUGUAY
HOST_UY = ""
USER_UY = ""
KEY_UY = ""
PORT_SFTP_UY = '22'
LOCAL_PATH_UY = 'local_files/'
REMOTE_PATH_FILE_DOWNLOAD_UY = ""
REMOTE_PATH_FILE_UPLOAD_UY = ""
FILE_NAME_REMOTE_UY = ""
CONTROL_FILE_UY = "_control_ar.json"

# SFTP ARGENTINA
HOST_AR = ""
USER_AR = ""
KEY_AR = ""
PORT_SFTP_AR = '22'
LOCAL_PATH_AR = 'local_files/'
REMOTE_PATH_FILE_DOWNLOAD_AR = ""
REMOTE_PATH_FILE_UPLOAD_AR = ""
FILE_NAME_REMOTE_AR = ""
CONTROL_FILE_AR = "_control_ar.json"

# SPLIT
SPLIT_SIZE = 8000000
LOCAL_SPLITTER_PATH = 'splitted_files/'

# MESSAGES API
LIST_MESSAGES = {
    'success': 1,
    'error_auth': 2,
    'error_connection_sftp': 3,
    'error_download': 4,
    'error_send_file': 5,
    'error_remove_quotation_marks': 6,
    'error_split_files': 7,
    'error_only_one_row': 8,
    }

# USERS APP
USERS_APP = {"admin": "admin"}
