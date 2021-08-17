import os

class EnvironmentConfig:
    def __init__(self):
        self.project_id = os.getenv('FIREBASE_PROJECT_ID')
        self.file_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_FILE')
        if self.file_path is None:   
            self.file_path = './service-account.json'
        if self.project_id is None:
            raise Exception('PROJECT_ID must be not null, please set a value to the FIREBASE_PROJECT_ID environment variable')