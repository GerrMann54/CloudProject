import yadisk

class Connection():

    def init_folder(self, folder):

        if not self.disk.exists(folder):
            self.disk.mkdir(folder)

    def __init__(self, user_token, folder):

        self.successfully = True

        try:
            print("Connecting to YaDisk...")
            self.disk = yadisk.YaDisk(token=user_token)
            print("Token:", self.disk.check_token())
        except:
            print("Unable to connect to YaDisk")
            self.successfully = False

        try:
            self.folder = f'/{folder}/'
            self.init_folder(self.folder)
            print('Current folder:', self.folder)
        except:
            print("Unable to init folder")
            self.successfully = False
