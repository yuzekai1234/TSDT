from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/yuzekai1234/TSDT.git'  #(1)

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  #(2)(3)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)  #(2)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')  #(1)(2)
def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):  #(1)
        run(f'cd {source_folder} && git fetch')  #(2)(3)
    else:
        run(f'git clone {REPO_URL} {source_folder}')  #(4)
    # current_commit = local("git log -n 1 --format=%H", capture=True)  #(5)
    # run(f'cd {source_folder} && git reset --hard {current_commit}')  #(6)
def _update_settings(source_folder, site_name):
    source_folder= source_folder + '/notes'  #(1)
    settings_path = source_folder + '/notes/settings.py'  #(1)
    sed(settings_path, "DEBUG = True", "DEBUG = False")  #(2)
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )  #(3)
    secret_key_file = source_folder + '/notes/secret_key.py'  #(4)
    if not exists(secret_key_file):  #(5)
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')  #(6)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')  #(7)
def _update_virtualenv(source_folder):
    source_folder = source_folder + '/notes'
    virtualenv_folder = source_folder + '/../../virtualenv'  #(1)
    if not exists(virtualenv_folder + '/bin/pip'):  #(2)
        run(f'python3.9 -m venv {virtualenv_folder}')  #(3)
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')  #(4)
def _update_static_files(source_folder):
    source_folder = source_folder + '/notes'
    run(
        f'cd {source_folder}'
        ' && ../../virtualenv/bin/python manage.py collectstatic --noinput'
    )  #(1)
def _update_database(source_folder):
    source_folder = source_folder + '/notes'
    run(
        f'cd {source_folder}'
        ' && ../../virtualenv/bin/python manage.py migrate --noinput'
    )  #(1)
if __name__ == '__main__':
    local('fab -f /path/to/fabfile.py deploy')