import constants
import requests
import importlib
import sys
import time

const = constants


def updater(interval=constants.CONFIG_PARSE_DELAY_SECONDS):
    while True:
        start_time = time.time()
        update()
        time.sleep(interval - ((time.time() - start_time) % interval))


def update():
    global const
    code = requests.get('https://raw.githubusercontent.com/WarhioCompany/ichazybot/main/constants.py').text
    print(code)
    with open('constants.py', 'w', encoding='utf-8') as file:
        file.write(code)
    import constants
    const = constants
    #module = modify_and_import('constants', None, lambda src: code)


def modify_and_import(module_name, package, modification_func):
    spec = importlib.util.find_spec(module_name, package)
    source = spec.loader.get_source(module_name)
    new_source = modification_func(source)
    module = importlib.util.module_from_spec(spec)
    codeobj = compile(new_source, module.__spec__.origin, 'exec')
    exec(codeobj, module.__dict__)
    sys.modules[module_name] = module
    return module