Title: Heroku to AWS Part 2
Date: 2014-05-19
Category: 
Tags: 
Slug: heroku-to-aws-part-2
Author: Matt Camilli
Description: 



## Exporting Procfiles to Supervisor Confs

Heroku uses a ruby gem called [foreman](https://github.com/ddollar/foreman)
which allows you to run Procfiles in an isolated environment with
specific environment variables which are stored in a .env file. This was
a paradigm we liked and wanted to keep with our new solution.

This is what our web procfile looks like:    
    
    web: newrelic-admin run-program uwsgi --ini deployment/confs/uwsgi.ini

and of course our celery one was a bit more complicated:

    blog: newrelic-admin run-program celery -A trackmaven.config worker -c
    3 --loglevel=DEBUG -Q blog -n blog.%%h
    news: newrelic-admin run-program celery -A trackmaven.config worker -c
    4 --loglevel=DEBUG -Q news -n news.%%h
    facebook: newrelic-admin run-program celery -A trackmaven.config worker -c
    4 --loglevel=DEBUG -Q facebook -n facebook.%%h
    twitter: newrelic-admin run-program celery -A trackmaven.config worker -c
    4 --loglevel=DEBUG -Q twitter -n twitter.%%h
    youtube: newrelic-admin run-program celery -A trackmaven.config worker -c
    2 --loglevel=DEBUG -Q youtube -n youtube.%%h
    instagram: newrelic-admin run-program celery -A trackmaven.config worker -c
    2 --loglevel=DEBUG -Q instagram -n instagram.%%h


The .env file was simply a key=value list of environment variables. The problem
we were faced with was given the Procfile and .env file, we now needed to
generate a supervisor configuration file with the contents of those files.

My solution to this was creating a custom script that would use jinja to
dynamically create a supervisor configuration file based on the procfile
inputted and whatever happend to be in the .env file on that instance. 

    {% for program in programs %}
    [program:{{ program.name }}]
    command=/bin/bash -c "source /somepath/.virtualenvs/trackmaven/bin/activate
    && exec {{program.command}}"
    autostart=true
    autorestart=true
    stopsignal=QUIT
    stdout_logfile=syslog
    stderr_logfile=syslog
    user={{user}}
    directory=/somepath/TrackMaven
    environment={{ ','.join(environment) }}
    {% endfor %}
    [group:{{app}}]
    programs={{ ','.join(names) }}
    
This is the basic jinja template where each program represents a line from the
procfile, so given the celery example the `program.name` would represent blog
or news or facebook etc. `environment` was a list of key=value strings that
were read in from the .env file. So after running the export command which
looked something like:

    kwargs = {
        'environment': ['{}="{}"'.format(key,value.replace('%', '%%'))
            for key, value in environment.items()],
        'programs': programs,
        'user': 'ubuntu',
        'app': 'trackmaven',
        'names': [program['name']
            for program in programs]
    }
    with open('/etc/supervisor/conf.d/trackmaven.conf', 'w') as f:
                f.write(template.render(**kwargs))

which resulted in a configuration file looking like:


    [program:trackmaven-facebook]
    command=/bin/bash -c "source /somepath/.virtualenvs/trackmaven/bin/activate &&
    exec newrelic-admin run-program celery -A trackmaven.config worker -c
    2 --loglevel=DEBUG -Q facebook -n facebook.%%h"
    autostart=true
    autorestart=true
    stopsignal=QUIT
    stdout_logfile=syslog
    stderr_logfile=syslog
    user=ubuntu
    directory=/somepath/TrackMaven
    environment=SOMEVARIABLE=SOMEVALUE,FACEBOOK_TOKEN=1235FA,DEBUG=False

    [program:trackmaven-blog]
    command=/bin/bash -c "source /somepath/.virtualenvs/trackmaven/bin/activate &&
    exec newrelic-admin run-program celery -A trackmaven.config worker -c
    4 --loglevel=DEBUG -Q blog -n blog.%%h"
    autostart=true
    autorestart=true
    stopsignal=QUIT
    stdout_logfile=syslog
    stderr_logfile=syslog
    user=ubuntu
    directory=/somepath/TrackMaven
    environment=SOMEVARIABLE=SOMEVALUE,FACEBOOK_TOKEN=1235FA,DEBUG=False


    [group:trackmaven]
    programs=trackmaven-blog,trackmaven-facebook
