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
    def get_name_variation(self):
        return self.config.get('Settings', 'name_variation')

    @property
    def get_city(self):
        return self.config.get('Settings', 'geo')

    @property
    def get_group_id(self):
        try:
            return self.config.get('Settings', 'group_id')
        except configparser.NoOptionError:
            pass

    @property
    def proxy_soax_password(self):
        return self.config.get('Settings', 'soax_password')

    @property
    def get_activate_key(self):
        return self.config.get('Settings', 'sms-activate_key')

    @property
    def get_change_account(self):
        return bool(self.config.get('Settings', 'change_account_settings'))

    @property
    def get_min_age(self):
        return int(self.config.get('Settings', 'minimum_age'))

    @property
    def get_max_age(self):
        return int(self.config.get('Settings', 'maximum_age'))



config_data = Config()
log_dispatcher.info(to_write=f'CONFIG:\n'
                             f'{config_data.get_reg_variable}\n{config_data.get_photos_dir}\n'
                             f'{config_data.get_city}\n{config_data.get_group_id}\n'
                             f'{config_data.get_change_account}\n')
