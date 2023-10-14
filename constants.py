import json
import requests
import time
import threading

config_url = 'https://raw.githubusercontent.com/WarhioCompany/ichazybot/main/config.json'


class Constants:
    def __init__(self):
        self.config_interval = 3600
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        x = threading.Thread(target=self.get_config, daemon=True)
        x.start()
        self.config_file_prettier()

    def get_config(self):
        print(self.config)
        start_time = time.time()
        print('Getting config....')

        server_config = json.loads(requests.get(config_url).text)
        if 'CONFIG_VERSION' not in server_config or self.config['CONFIG_VERSION'] > server_config['CONFIG_VERSION']:
            print('Local version of config is greater than on the server')
            return

        print(f'{time.time()}: Got config')
        self.config = server_config

        self.config_interval = server_config['CONFIG_PARSE_DELAY_SECONDS']
        time.sleep(self.config_interval - ((time.time() - start_time) % self.config_interval))

    def __getitem__(self, item):
        return self.config[item]

    def config_file_prettier(self):
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        with open('config.json', 'w+', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))


const = Constants()
