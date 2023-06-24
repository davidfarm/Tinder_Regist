class BanDp:
    def __init__(self):
        self.driver = None
        self.work_status = 'Active'

    @property
    def get_status(self):
        return self.work_status

    def set_status(self, new_status):
        self.work_status = new_status

    def set_dp(self, driver):
        self.driver = driver

    @property
    def get_driver(self):
        return self.driver


ban_dp = BanDp()
