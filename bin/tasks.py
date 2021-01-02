from fabric import Connection as connection, task
from invoke import task
from os import getenv

connect_kwargs = {
    'passphrase': getenv('SSH_PASSPHRASE')
}


@task
def build(c):
    print("Building!")


@task
def deploy(ctx):
    # with connection(host='52.64.186.191', user='tde-ssh', connect_kwargs={"key_filename": "/Users/mike.mo/.ssh/id_rsa"}) as c:
    # with connection(host='52.64.186.191', user='tde-ssh') as c:
    with connection(host='52.64.186.191', user='tde-ssh', connect_kwargs=connect_kwargs) as c:
        c.run('ls -la')
        c.run('whoami')
        c.run('ps -ef | grep varnish')
        c.run('uname -a')
