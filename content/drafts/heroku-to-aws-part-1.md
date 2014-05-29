Title: Heroku to AWS Part 1: Boto, Fabric, and Ansible Oh My!
Date: 2014-05-19
Category: DevOps
Tags: aws, heroku, supervisor, foreman
Slug: heroku-to-aws-part-1
Author: Matt Camilli
Description: Migrating from a managed Heroku environment to our custom
AWS platform was a bit of a hassle, here is how we did it. :

As TrackMaven scaled it became more and more apparent that we needed a more
custom solution for our platform. Now before I really dive into this blog post
I want to make it abundantly clear that I like Heroku. As far as PaaS's go,
it is one of the best, which is why I use it for a lot of my local projects. 

However, in TrackMaven's case, it got to the point where their database pricing
didn't scale well with our app, and too many times we would have unexplained
outages shortly followed by apology emails from the Heroku staff. Since
there was no SLA, we were kind of out of luck. We decided that a custom
solution that we would implement and host on AWS would be better in the long
term. 

As a fan of Heroku, I wanted the "developer experience" in our new platform to
mimic the simplicity and function of the heroku command line interface. Through
a bit of research I landed on using fabric with ansible and several custom
python scripts to achieve this. 

To give context, the new cluster would consiste of 3 types of EC2 instances:
A web instance to serve our app to our users, a celery instance to run the data
collection tasks, and a manager instance to allow us access to the database for
customer experience purposes. The instances would have a pretty typical python
stack: [Supervisor](http://supervisord.org/) as the process control system and 
nginx to serve the content to port 80. These EC2 instances would be supported by
a Postgres database served by RDS, and a redis instance hosted on elasticache. 


