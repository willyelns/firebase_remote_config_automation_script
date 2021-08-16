# import argparse
# import requests
# import os
# import json

# from oauth2client.service_account import ServiceAccountCredentials


# PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
# FILE_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_FILE')

# if FILE_PATH is None:
#   FILE_PATH = './service-account.json'

#   if PROJECT_ID is None:
#     raise Exception('PROJECT_ID must be not null, please set a value to the FIREBASE_PROJECT_ID environment variable')

# BASE_URL = 'https://firebaseremoteconfig.googleapis.com'
# REMOTE_CONFIG_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/remoteConfig'
# REMOTE_CONFIG_URL = BASE_URL + '/' + REMOTE_CONFIG_ENDPOINT
# SCOPES = ['https://www.googleapis.com/auth/firebase.remoteconfig']

# # [START retrieve_access_token]
# def _get_access_token():
#   """ Retrieve a valid access token that can be used to authorize requests.
#   :return: Access token.
#   """
#   credentials = ServiceAccountCredentials.from_json_keyfile_name(
#       FILE_PATH, SCOPES)
#   access_token_info = credentials.get_access_token()
#   return access_token_info.access_token
# # [END retrieve_access_token]


# def _get_app_config_list(remote_config):
#   """ "filtering" the dict to return only the App Config list from the all the remote data 
#   Args:
#     remote_config: A dictionary with all the remote config data
#   :return: Only the app config list.
#   """
#   app_config_list = json.loads(remote_config['parameters']['app_config']['defaultValue']['value'])
#   return app_config_list

# def _update_all_current_version(app_config_list, new_version=None):
#   """ Change the current version data to a new one 
#   Args:
#     app_config_list: A dictionary with all the app config list data
#     new_version: A String in the `0.0.0`format that represents the new current version
#   :return: An updated app config list
#   """
#   if new_version is None:
#     raise Exception('new_version must not be null')

#   for id in app_config_list:
#     app_config = app_config_list[id]
#     old_version = app_config['current']
#     print(f'> [ Company: {id} ] Updating the current version from {old_version} version to: {new_version} \n')
#     app_config['current'] = new_version
#   return app_config_list

# def _update_all_accepted_version(app_config_list, new_version=None):
#   """ Change the accepted version data to a new one 
#   Args:
#     app_config_list: A dictionary with all the app config list data
#     new_version: A String in the `0.0.0`format that represents the new current version
#   :return: An updated app config list
#   """
#   if new_version is None:
#     raise Exception('new_version must be not null')
#   for id in app_config_list:
#     print('id: ', id)
#     app_config = app_config_list[id]
#     old_version = app_config['accepted']
#     print('> current:', old_version)
#     app_config['accepted'] = new_version
#     print(f'> [Company: {id}] Updating the accepted version from {old_version} version to: {new_version} \n')
#   return app_config_list

# def _update_accepted_version_by_o_s(app_config_list, new_version=None):
#   """ Change the accepted version data to a new one restricted by an O.S
#   Args:
#     app_config_list: A dictionary with all the app config list data
#     new_version: A String in the `0.0.0`format that represents the new current version
#   :return: An updated app config list
#   """
#   if new_version is None:
#     raise Exception('new_version must be not null')
#   for id in app_config_list:
#     print('id: ', id)
#     app_config = app_config_list[id]
#     old_version = app_config['accepted`']
#     print('> current:', old_version)
#     app_config['accepted'] = new_version
#     print(f'> [Company: {id}] Updating the accepted version from {old_version} version to: {new_version} \n')
#   return app_config_list


# def _publish(remote_config_list, version):
#   """Publish local template to Firebase server.
#   Args:
#     remote_config_list: The remote config, used to update the previous one in the server
#     version: a string in the `0.0.0` format used to create an valid etag
#   """
#   headers = {
#     'Authorization': 'Bearer ' + _get_access_token(),
#     'Content-Type': 'application/json',
#     'If-Match': '*'
#   }
#   resp = requests.put(REMOTE_CONFIG_URL, json=remote_config_list, headers=headers)
#   if resp.status_code == 200:
#     print('Template has been published.')
#     print('ETag from server: {}'.format(resp.headers['ETag']))
#   else:
#     print('Unable to publish template.')
#     print(resp.text)

# def _add_data_to_remote_config(data_to_upload = None, remote_list = None, version = None):
#   """ Add the new app config list to the current remote config
#   Args:
#     data_to_upload: A dictionary with all the app config list data (With the new version updated)
#     remote_list: The remote config data, used to be merged
#     version: a string in the `0.0.0` format used to create an valid etag
#   """
#   if data_to_upload is None or remote_list is None or version is None:
#     raise Exception('function data must be not null')
#   remote_list['parameters']['app_config']['defaultValue']['value'] = json.dumps(data_to_upload)
#   print('calling update to all remote config')
#   _publish(remote_list, version)

# def _get_remote_list():
#   """Retrieve the current Firebase Remote Config template from server.
#   Retrieve the current Firebase Remote Config template from server and store it
#   locally.
#   :return:
#     string with all the remote_config data
#   """
#   headers = {
#     'Authorization': 'Bearer ' + _get_access_token()
#   }
#   resp = requests.get(REMOTE_CONFIG_URL, headers=headers)

#   if resp.status_code == 200:
#     return json.loads(resp.text)

#   else:
#     print('Unable to get template')
#     print(resp.text)

# def _set_all_current_version(new_current_version): 
#   """ Orchestrator to get the current remote config. 
#   Update all the app_config list to a new current version, and send it back to the remote config server
#   Args:
#     new_current_version: String in `0.0.0` format used to set the current version of the apps.
#   """
#   # getting the list
#   old_remote = _get_remote_list()
#   # isolating the current app config list
#   app_config_list = _get_app_config_list(old_remote)
#   # generating the new list with the updated current version
#   new_config_list = _update_all_current_version(app_config_list, new_current_version)
#   # calling update to all remote config
#   _add_data_to_remote_config(data_to_upload = new_config_list, remote_list = old_remote, version= new_current_version)

# def _set_all_accepted_version(new_current_version): 
#   """Orchestrator to get the current remote config. 
#   Update all the app_config list to a new accepted version, and send back to remote config server
#   Args:
#     new_current_version: String in `0.0.0` format used to set the current version of the apps.
#   """
#   # getting the list
#   old_remote = _get_remote_list()
#   # isolating the current app config list
#   app_config_list = _get_app_config_list(old_remote)
#   # generating the new list with the updated current version
#   new_config_list = _update_all_accepted_version(app_config_list, new_current_version)
#   # calling update to all remote config
#   _add_data_to_remote_config(data_to_upload = new_config_list, remote_list = old_remote, version = new_current_version)


# def main():
#   parser = argparse.ArgumentParser()
#   parser.add_argument('--action')
#   parser.add_argument('--version')
#   args = parser.parse_args()

#   if args.action and args.action == 'current_version' and args.version:
#     _set_all_current_version(args.version)
#   elif args.action and args.action == 'accepted_version' and args.version:
#     _set_all_accepted_version(args.version)
#   else:
#     print('''Invalid command. Please use one of the following commands:
# python remote_config.py --action=current_version --version=<APP_NEW_CURRENT_VERSION>
# python remote_config.py --action=accepted_version --version=<APP_NEW_ACCEPTED_VERSION>''')

# if __name__ == '__main__':
#   main()

import argparse
from remote_config_controller import RemoteConfigController


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--version')
  parser.add_argument('--platform')
  args = parser.parse_args()
  remote_config_controller = RemoteConfigController()

  if args.action and args.action == 'current_version' and args.version:
    remote_config_controller.set_all_current_version(args.version, args.platform)
  elif args.action and args.action == 'accepted_version' and args.version:
    remote_config_controller.set_all_accepted_version(args.version, args.platform)
  else:
    print('''Invalid command. Please use one of the following commands:
python remote_config.py --action=current_version --version=<APP_NEW_CURRENT_VERSION>
python remote_config.py --action=current_version --platform=<ios/android> --version=<APP_NEW_CURRENT_VERSION>
python remote_config.py --action=accepted_version --version=<APP_NEW_ACCEPTED_VERSION>
python remote_config.py --action=accepted_version --platform<ios/android> --version=<APP_NEW_ACCEPTED_VERSION>''')

if __name__ == '__main__':
  main()