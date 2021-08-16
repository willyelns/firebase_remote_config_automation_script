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