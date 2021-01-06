from fabric import Connection as connection, task
from patchwork.files import exists
from invoke import Responder
from invoke import task
from os import getenv
from time import time_ns

HOST = '52.65.42.123'
USER = 'render01'


connect_kwargs = {
    'passphrase': getenv('SSH_PASSPHRASE')
}


@task
def build(c):
    print("Building!")


@task
def remote_commands(ctx):
    # with connection(host='52.64.186.191', user='render01', connect_kwargs={"key_filename": "/Users/mike.mo/.ssh/id_rsa"}) as c:
    # with connection(host='52.64.186.191', user='render01') as c:
    with connection(host=HOST, user=USER, connect_kwargs=connect_kwargs) as c:
        c.run('ls -la')
        c.run('whoami')
        c.run('ps -ef | grep varnish')
        c.run('uname -a')


REPO_URL = 'https://cartooncatfish@github.com/cartooncatfish/word_gallary.git'
REPO_DIR = '/home/render01/trying/repo'
PRO_DIR = '/home/render01/trying/releases'
PRO_BASE = '/home/render01/trying'

git_watchers = [
    # Responder(pattern=r"Username for .*", response="git_user\n"),
    Responder(pattern=r"Password for .*", response=getenv('GITHUB_PASSPHRASE') + '\n')]


@task
def deploy(ctx):
    with connection(host=HOST, user=USER, connect_kwargs=connect_kwargs) as c:
        # check directory exist
        c.run('cd ' + REPO_DIR)
        with c.cd(REPO_DIR):
            ###########################
            # get the codes from github
            ###########################
            c.run('pwd')
            github_passphrase = getenv('GITHUB_PASSPHRASE')
            repo_folder = REPO_DIR + '/.git'
            print('repo folder is {}'.format(repo_folder))
            # result = c.run('test -d 0970432753425')
            # print('testing ' + result == True)
            # print(c.run('test -d {}'.format(repo_folder), warn=True).failed)
            # if c.run('test -d {}'.format(repo_folder), warn=True).failed:
            print(exists(c, repo_folder))
            if exists(c, repo_folder):
                # if exist('.get'):
                print('fetching code')
                # c.run('git fetch', pty=True, watchers=git_watchers)
                # fetch is not working...
                c.run('git pull', pty=True, watchers=git_watchers)
            else:
                print('clone the repo')
                # c.run(f'git clone' + REPO_URL.format(github_passphrase))
                c.run(f'git clone ' + REPO_URL.format(github_passphrase) + ' .',
                      pty=True, watchers=git_watchers)

            ###########################
            # copy files to the target directory
            ###########################
            release_dir = PRO_DIR + '/' + str(time_ns())
            print('The release directory is [{}]'.format(release_dir))
            print(repo_folder, REPO_DIR)
            # delete the old deployments
            print('deleting the old deployments')
            c.run('ls -al {}'.format(PRO_DIR))
            # c.run('rm -fr {}'.format(PRO_DIR) + '/160*')

            print('adding new version')
            c.run('mkdir -p {}'.format(release_dir))
            c.run('cp -r {} {}'.format(REPO_DIR + '/*', release_dir))
            c.run('ls -al {}'.format(PRO_DIR))

            ###########################
            # change current directory
            ###########################
            current_dir = PRO_BASE + '/current'
            c.run('rm {} && ln -s {} {}'.format(current_dir, release_dir, current_dir))

            print('Enter the release directory {} '.format(release_dir))
            with c.cd(release_dir):
                ###########################
                # install the virtual environment
                ###########################
                c.run('export PIPENV_VENV_IN_PROJECT=1')
                c.run('pipenv install --python /usr/bin/python3.8')
                # c.run('pipenv shell')
                # with c.cd(release_dir + '/app'):
                #     c.run('python manage.py runserver 0.0.0.0:8080 >> log.log 2>&1')

            # c.run('./virtualenv/bin/pip install -r requirements.txt')
