import argparse
import requests
import os
import json

from oauth2client.service_account import ServiceAccountCredentials

# PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
# FILE_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_FILE')

# if FILE_PATH is None:   
#     FILE_PATH = './service-account.json'
# if PROJECT_ID is None:
#     PROJECT_ID = 'memo-receipt'
#     # raise Exception('PROJECT_ID must be not null, please set a value to the FIREBASE_PROJECT_ID environment variable')

class EnvironmentConfig:
    def __init__(self):
        self.project_id = os.getenv('FIREBASE_PROJECT_ID')
        self.file_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_FILE')
        if self.file_path is None:   
            self.file_path = './service-account.json'
        if self.project_id is None:
            self.project_id = 'memo-receipt'
            # raise Exception('PROJECT_ID must be not null, please set a value to the FIREBASE_PROJECT_ID environment variable')

class RemoteConfigController:

    def __init__(self) -> None:
        self.base_url = 'https://firebaseremoteconfig.googleapis.com'
        self.remote_config_endpoint = 'v1/projects/' + PROJECT_ID + '/remoteConfig'
        self.remote_config_url = self.base_url + '/' + self.remote_config_endpoint
        self.scopes = ['https://www.googleapis.com/auth/firebase.remoteconfig']


    # [START retrieve_access_token]
    def _get_access_token(self):
        """ Retrieve a valid access token that can be used to authorize requests.
        :return: Access token.
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            FILE_PATH, self.scopes)
        access_token_info = credentials.get_access_token()
        return access_token_info.access_token
    # [END retrieve_access_token]

    def _get_app_config_list(self, remote_config):
        """ "filtering" the dict to return only the App Config list from the all the remote data 
        Args:
            remote_config: A dictionary with all the remote config data
        :return: Only the app config list.
        """
        app_config_list = json.loads(remote_config['parameters']['app_config']['defaultValue']['value'])
        return app_config_list
    
    def _update_all_current_version(self, app_config_list, new_version=None):
        """ Change the current version data to a new one 
        Args:
            app_config_list: A dictionary with all the app config list data
            new_version: A String in the `0.0.0`format that represents the new current version
        :return: An updated app config list
        """
        if new_version is None:
            raise Exception('new_version must not be null')

        for id in app_config_list:
            app_config = app_config_list[id]
            old_ios_version = app_config['current_ios_version']
            old_android_version = app_config['current_android_version']
            print(f'> [ Company: {id} ] Updating the current version from ios: {old_ios_version} and Android: {old_android_version} version  to: {new_version} \n')
            app_config['current_ios_version'] = new_version
            app_config['current_android_version'] = new_version
            app_config['current'] = new_version
        return app_config_list

    def _update_current_version_by_platform(self, app_config_list, platform=None,new_version=None):
        """ Change the current version data to a new one restricted by an O.S
        Args:
            app_config_list: A dictionary with all the app config list data
            platform: A String in the `ios` or `android` format that represents the platform
            new_version: A String in the `0.0.0`format that represents the new current version
        :return: An updated app config list
        """
        if new_version is None:
            raise Exception('new_version must be not null')
        if platform is None:
            return self._update_all_current_version(app_config_list, new_version)
        for id in app_config_list:
            print('id: ', id)
            app_config = app_config_list[id]
            if(platform == 'ios'):
                old_ios_version = app_config['current_ios_version']
                app_config['current_ios_version'] = new_version
                print(f'> [Company: {id}] Updating the current version from {old_ios_version} version to: {new_version} \n')
            elif(platform == 'android'):
                old_android_version = app_config['current_android_version']
                app_config['current_android_version'] = new_version
                print(f'> [Company: {id}] Updating the current version from {old_android_version} version to: {new_version} \n')
            elif(platform == 'both'):
                self._update_all_current_version(app_config_list, new_version)
        return app_config_list

    def _update_all_accepted_version(self, app_config_list, new_version=None):
        """ Change the accepted version data to a new one 
        Args:
            app_config_list: A dictionary with all the app config list data
            platform: A String in the `ios` or `android` format that represents the platform
            new_version: A String in the `0.0.0`format that represents the new current version
        :return: An updated app config list
        """
        if new_version is None:
            raise Exception('new_version must be not null')
        for id in app_config_list:
            print('id: ', id)
            app_config = app_config_list[id]
            old_version = app_config['accepted']
            old_ios_version = app_config['accepted_ios_version']
            old_android_version = app_config['accepted_android_version']
            print('> current iOS:', old_ios_version)
            print('> current Android:', old_android_version)
            app_config['accepted_ios_version'] = new_version
            app_config['accepted_android_version'] = new_version
            app_config['accepted'] = new_version
            print(f'> [Company: {id}] Updating the accepted version from {old_version} version to: {new_version} \n')
        return app_config_list

    def _update_accepted_version_by_platform(self, app_config_list, platform=None,new_version=None):
        """ Change the accepted version data to a new one restricted by an O.S
        Args:
            app_config_list: A dictionary with all the app config list data
            new_version: A String in the `0.0.0`format that represents the new current version
        :return: An updated app config list
        """
        if new_version is None:
            raise Exception('new_version must be not null')
        if platform is None:
            return self._update_all_accepted_version(app_config_list, new_version)
        for id in app_config_list:
            print('id: ', id)
            app_config = app_config_list[id]
            old_version = app_config['accepted`']

            if(platform == 'ios'):
                old_ios_version = app_config['accepted_ios_version']
                print('> current:', old_version)
                app_config['accepted_ios_version'] = new_version
                print(f'> [Company: {id}] Updating the accepted version from {old_ios_version} version to: {new_version} \n')
            elif(platform == 'android'):
                old_android_version = app_config['accepted_android_version']
                print('> current:', old_version)
                app_config['accepted_android_version'] = new_version
                print(f'> [Company: {id}] Updating the accepted version from {old_android_version} version to: {new_version} \n')
            elif(platform == 'both'):
                return self._update_all_accepted_version(app_config_list, new_version)
        return app_config_list


    def _publish(self, remote_config_list):
        """Publish local template to Firebase server.
        Args:
            remote_config_list: The remote config, used to update the previous one in the server
            version: a string in the `0.0.0` format used to create an valid etag
        """
        headers = {
            'Authorization': 'Bearer ' + self._get_access_token(),
            'Content-Type': 'application/json',
            'If-Match': '*'
        }
        resp = requests.put(self.remote_config_url, json=remote_config_list, headers=headers)
        if resp.status_code == 200:
            print('Template has been published.')
            print('ETag from server: {}'.format(resp.headers['ETag']))
        else:
            print('Unable to publish template.')
            print(resp.text)

    def _add_data_to_remote_config(self, data_to_upload = None, remote_list = None, version = None):
        """ Add the new app config list to the current remote config
        Args:
            data_to_upload: A dictionary with all the app config list data (With the new version updated)
            remote_list: The remote config data, used to be merged
            version: a string in the `0.0.0` format used to create an valid etag
        """
        if data_to_upload is None or remote_list is None or version is None:
            raise Exception('function data must be not null')
        remote_list['parameters']['app_config']['defaultValue']['value'] = json.dumps(data_to_upload)
        print('calling update to all remote config')
        self._publish(remote_list)

    def _get_remote_list(self):
        """Retrieve the current Firebase Remote Config template from server.
        Retrieve the current Firebase Remote Config template from server and store it
        locally.
        :return:
            string with all the remote_config data
        """
        headers = {
            'Authorization': 'Bearer ' + self._get_access_token()
        }
        resp = requests.get(self.remote_config_url, headers=headers)

        if resp.status_code == 200:
            return json.loads(resp.text)

        else:
            print('Unable to get template')
            print(resp.text)

    def set_all_current_version(self, new_current_version, platform=None): 
        """ Orchestrator to get the current remote config. 
        Update all the app_config list to a new current version, and send it back to the remote config server
        Args:
            new_current_version: String in `0.0.0` format used to set the current version of the apps.
        """
        # getting the list
        old_remote = self._get_remote_list()
        # isolating the current app config list
        app_config_list = self._get_app_config_list(old_remote)
        # generating the new list with the updated current version
        new_config_list = self._update_curre0nt_version_by_platform(app_config_list, new_current_version, platform)
        # calling update to all remote config
        self._add_data_to_remote_config(data_to_upload = new_config_list, remote_list = old_remote, version = new_current_version)

    def set_all_accepted_version(self, new_current_version, platform=None): 
        """Orchestrator to get the current remote config. 
        Update all the app_config list to a new accepted version, and send back to remote config server
        Args:
            new_current_version: String in `0.0.0` format used to set the current version of the apps.
        """
        # getting the list
        old_remote = self._get_remote_list()
        # isolating the current app config list
        app_config_list = self._get_app_config_list(old_remote)
        # generating the new list with the updated current version
        new_config_list = self._update_all_accepted_version(app_config_list, new_current_version)
        # calling update to all remote config
        self._add_data_to_remote_config(data_to_upload = new_config_list, remote_list = old_remote, version = new_current_version)