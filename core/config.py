import configparser

from core.logger import log_dispatcher


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    @property
    def get_reg_variable(self):
        return self.config.get('Settings', 'reg_variable')

    @property
    def get_photos_dir(self):
        return self.config.get('Settings', 'photos_dir')

    @property
    def get_port(self):
        return self.config.get('Settings', 'port')

    @property
    def get_name_variation(self):
        return self.config.get('Settings', 'name_variation')

    @property
    def get_city(self):
        return self.config.get('Settings', 'geo')

    @property
    def get_group_id(self):
        return self.config.get('Settings', 'group_id')

    @property
    def get_change_account(self):
        return bool(self.config.get('Settings', 'change_account_settings'))


config_data = Config()
log_dispatcher.info(to_write=f'CONFIG:\n'
                             f'{config_data.get_reg_variable}\n{config_data.get_photos_dir}\n'
                             f'{config_data.get_port}\n{config_data.get_name_variation}\n'
                             f'{config_data.get_city}\n{config_data.get_group_id}\n'
                             f'{config_data.get_change_account}\n')
