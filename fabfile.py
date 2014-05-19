from fabric.api import local, env, hosts
import fabric.contrib.project as project
from datetime import datetime
from pytz import timezone
import shutil
import os


# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


def build():
    local('pelican -s pelicanconf.py')
    local("echo 'mattcamilli.com' > {}/CNAME".format(env.deploy_path))


def rebuild():
    clean()
    build()


def regenerate():
    local('pelican -r -s pelicanconf.py')


def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))


def reserve():
    build()
    serve()


def preview():
    local('pelican -s publishconf.py')


def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))


def new(article_name):
    slug = article_name.lower().replace(' ', '-')
    filename = slug + '.md'
    with open('content/drafts/{}'.format(filename), 'w') as writer:
        writer.write('Title: {}\n'.format(article_name))
        writer.write('Date: {}\n'.format(timezone('US/Eastern').localize(
            datetime.now()).strftime('%Y-%m-%d %I:%M %p')))
        writer.write('Category: \n')
        writer.write('Tags: \n')
        writer.write('Slug: {}\n'.format(slug))
        writer.write('Author: Matt Camilli\n')
        writer.write('Description: \n')


def drafts():
    drafts = sorted(os.listdir('content/drafts/'))
    for count, draft in enumerate(drafts):
        print '{}: {}'.format(count, draft)


def finish(draft_number):
    drafts = sorted(os.listdir('content/drafts/'))
    draft = drafts[int(draft_number)]
    shutil.move('content/drafts/{}'.format(draft), 'content/{}'.format(draft))


def push():
    rebuild()
    local('git push origin master:source')
    local('ghp-import {}'.format(env.deploy_path))
    local('git push origin gh-pages:master --force')


@hosts(production)
def publish():
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
