from config import config


def get_message_code(error_name):
    return config.LIST_MESSAGES[error_name]
