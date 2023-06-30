import logging
import os
import colorlog


class Logger:
    def __init__(self, filename):
        self.logger_name = filename
        self.filename = f'{filename}/{filename}.txt'
        if not os.path.exists(filename):
            os.makedirs(filename)

        error_filter = logging.Filter()
        error_filter.filter = lambda record: record.levelno != logging.ERROR

        self.console_logger = logging.getLogger(f'console_logger_{self.logger_name}')
        self.console_logger.setLevel(logging.DEBUG)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)

        self.formatter_console = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s:%(message)s%(reset)s',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',

            },
        )
        self.formatter_file = logging.Formatter('{asctime} - {levelname} - {message}', style='{')

        self.console_handler.setFormatter(self.formatter_console)
        self.console_logger.addFilter(error_filter)
        self.console_logger.addHandler(self.console_handler)
        self.file_logger = logging.getLogger(f'file_logger_{self.logger_name}')
        self.file_logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler(self.filename)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter_file)
        self.file_handler.addFilter(error_filter)
        self.file_logger.addHandler(self.file_handler)

    def set_color(self, type_message):
        if type_message == 'error':
            self.formatter_console.log_colors['DEBUG'] = 'red'
        elif type_message == 'info':
            self.formatter_console.log_colors['DEBUG'] = 'green'

    def to_console(self, msg, type_message):
        self.console_logger = logging.getLogger(f'console_logger_{self.logger_name}')
        self.set_color(type_message)
        self.console_logger.debug(msg)

    def to_file(self, msg):
        self.file_logger = logging.getLogger(f'file_logger_{self.logger_name}')
        self.file_logger.debug(msg)

    def info(self, to_print='', to_write='', msg_type='info'):
        if to_write:
            self.to_file(msg=to_write)
        if to_print:
            self.to_console(msg=to_print, type_message=msg_type)

    def __call__(self, to_print='', to_write='##### NEW SESSION #####', *args, **kwargs):
        self.info(to_print, to_write)


log_dispatcher = Logger('log')
session_dp = Logger('invalid sessions')
# log_dispatcher.info(to_print='info', msg_type='info')
