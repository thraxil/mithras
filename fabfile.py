from fabric.api import run, sudo, local, cd, env

env.hosts = ['oolong.thraxil.org', 'maru.thraxil.org']
env.user = 'anders'
nginx_hosts = ['lilbub.thraxil.org', 'lolrus.thraxil.org']

def restart_gunicorn():
    sudo("restart mithras")

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/thraxil/mithras"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
        run("./manage.py migrate")
        run("./manage.py collectstatic --noinput")
        for n in nginx_hosts:
            run("rsync -avp --delete media/ %s:/var/www/thraxil/mithras/media/")
    restart_gunicorn()
