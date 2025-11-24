#!/usr/bin/env python3
"""
filter_datum
"""
from typing import List
import re
import logging
import os
import mysql.connector


patterns = {
        'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
        'replace': lambda x: r'\g<field>={}'.format(x)
        }
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """ function to hide user data
    """
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)

def get_logger() -> logging.Logger:
    """Only Log upto the INFO level
     - The object returned must be named user_data
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a connector to a secure database
    """
    USERNAME = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    HOST = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    NAME = os.getenv('PERSONAL_DATA_DB_NAME')
    if NAME is None:
        return
    try:
        connection = mysql.connector.connect(
                host=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=NAME
                )
        return connection
    except Exception as e:
        return None


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the incoming logs using filter_datum"""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)

