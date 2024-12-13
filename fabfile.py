"""
from fabric import task, Connection
from invoke import Responder
from _credentials import github_username, github_password

REMOTE_HOST = "127.0.0.1"
REMOTE_USER = "tanglin-hub"
SSH_KEY_PATH = "c/Users/34475/.ssh/id_rsa"

def _get_github_auth_responders():
    username_responder=Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder=Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{\n}'.format(github_password)
    )
    return [username_responder, password_responder]

@task
def deploy(c):
    conn = Connection(
        host=REMOTE_HOST,
        user=REMOTE_USER,
        connect_kwargs={
            "key_filename": SSH_KEY_PATH,  # 指定私钥路径
        },
    )

    supervisor_conf_path='~/etc/'
    supervisor_program_name='django_study'

    project_root_path='~/apps/django_study'

    with c.cd(supervisor_conf_path):
        cmd='supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)
    
    with c.cd(project_root_path):
        cmd='git pull git@github.com:tanglin-hub/django_test.git'
        responders=_get_github_auth_responders()
        c.run(cmd, watchers=responders)
    
    with c.cd(project_root_path):
        c.run('pipenv install --deploy --ignore-pipfile')
        c.run('pipenv run python manage.py migrate')
        c.run('pipenv run python manage.py collectstatic --nopoint')
    
    with c.cd(supervisor_conf_path):
        cmd='supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)
"""