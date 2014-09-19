Title: Deployment at TrackMaven
Summary: TrackMaven implemented a custom deployment pipeline for Amazon Web
Services after migrating away from Heroku. The result supported multiple
environments, continuous integration, seamless fast deployments by using
Ansible, boto and Fabric. Come hear the behind the scenes details about what
works and what's still in progress for TrackMaven's all-AWS deployment
pipeline. 


Talk:

Senior software Maven at trackmaven

mattcamilli.com is my blog although not gonna lie I don't blog too often
although I'm trying to step that game up, I find everytime I go to blog I end
up rengineering the blog itself instead of writing. 
------------------------------------------

The Product: In short TrackMaven is a competitive intelligence platform for data-driven
marketers. 

Basically we track and collect data from over 13 different marketing channels
for your company and the companies you track (typically competitors or
influencers). 


With all the data we have collected we provide a feed of all of those marketing
items and sort them by date or impact. Impact or engagement is measured by that
particular item's social shares or views compared to that of content of the
same type in a thirty day scope. 

We then allow customers to set custom alerts and daily, weekly 
and monthly scorecards based on all the data we are collecting. 
For instance if you want to be notified the second a competitor
publishes a piece of content that is 5x as engaging as most and likely to go
viral, you would set that alert to email you. (Text alerts might be added in
the future)

Next we have our brand overview page that allows you to general overviews of
the brands you track and data collected about them. It also allows you to see
how your brand stacks up against the competition.

Lastly we have our data visualizer which allows you to graph and export all the
data we have collected for your workspace. (Example is a share of voice graph
of twitter interactions, you can see where target was killing it until jc penny
started taking over. We allow you then to click that area and see what content
might have been driving that change.)

Python/Django app with AngularJS on the frontend. We use celery with rabbbitmq
for our data collecction tasks and store our data in Postgres and Redis. 


--------------------------------------------

Where we were

So when I first joined TrackMaven we were on Heroku.
Now before I start stating our reasons for leaving I want to make it clear that
Heroku is awesome, and for a lot of applications it is everything you could
want and more. I personally use it for side projects and have used it
previously for several production apps. 

That being said we did have several problems with Heroku. First of all they had
a very suspect SLA (service level agreement). They didn't guarantee 99% uptime, they had no money back
guarantee, we experienced a lot of unplanned downtimes which they would notify
us of typically an hour or so after it was resolved so in the meantime we would
be wondering what was wrong with our app. Also they had a lot of just really
inconvenient planned downtimes during what we would consider at times peak
hours. 

Heroku was also expensive when it came to scale, being pretty much linear at
best. Also twice they changed their plans around which forced us into bigger
price increases despite the fact that Amazon, the system they are built on, was
decreasing their prices. Lastly, as our application became more advanced, we
lacked the control and insight into the devops to really accomplish what we
needed to. For example we currently have a dual database setup, a write database if you
will which our backend data collection tasks constantly write to and update,
and a read database that our web app interacts with that follows the write one,
to provide a faster user experience. 

-----------------------------------------------

Where we ended up

AWS

Basically we decided to cut out the middle man and create our own devops
infrastructure on top of AWS, custom suited to our needs.

Why aws?
The SLA at amazon is notoriously amazing, with a monetary guarantee of a 99.95%
uptime. Since we have transitioned, sometime in march, we have had 0 downtime
due to Amazon.

It is cheap, with prices constantly decreasing and reserved instances we have
drastically reduced server costs. For example we have two databases now, the
same size of the previous one we had on heroku, for nowhere near the same cost. 
 
It has unmanaged options, you don't have to use beanstalk you can implement
your own infrastructure and they provide the tools to do so. Mainly their api.

Now that we had a platform chosen we pretty much set out  a few things that we
needed out of our devops infrastructure.

Ability to access the project shell - We often have data fixes or customer
issues that are solved quite easily through django's interactive shell. Heroku
had the ability to just bring up a shell and let us interact with the app via
a terminal and we wanted that same functionality and simplicity with our
solution. 

Ability to scale - Heroku made it really easy to scale, it was as simple as
a one line command to just spin up more dynos for your app.

Deployments from source control - With heroku it was very convenient to just
git push a branch and then have your deployment kick off, something we wanted
to mimic in our solution as well.

Lastly we wanted to be able to set environment variables with ease. Our app
uses over 50 different external apis and every single one has their own key,
most of which expire, so the ability to be able to update them when needed fwas
very important. 

-------------------------------------------------------
So basically how I structured this talk is I'm gonna talk about all the tools
we use individually and then show in the end how they all interact with one
another to make  up our deployment.

Our custom infrastructure uses all python tools (as we are a python shop) the
first of which I'll talk about is fabric. 

Fabric is a python command-line tool for streamlining the use of SSH for
application deployment or systems administration tasks. We use it mainly to
provide an easy interface for our developers to interact with Ansible and Boto. 

Basically in our project folder we have a fabfile which hosts all of our devops
commands. The commands are invoked when you preface them with the fab command. 

For example: fab prod shell

This is how we pull up an interactive terminal on our production server.

fab invokes a fabric command, prod sets fabrics environment dictionary to
production, which basically just sets host specific information about that
environment such as ip address, project location, ssh information. Lastly
shell executes the command below which simply changes directory into the
project path, and runs the command seen below which results in our interactive
terminal where we can make all the data changes we need.

-----------------------------------------------------------

Next tool that we use is Boto.
Boto is a python module that interacts with the infrastructural API  of AWS.

It allows us to add or remove instances, control load balancers, create and
manage images, and fetch instance data. The last part is very important as
you'll see soon for supplying ansible with the information needed to carry out
tasks. 

Before I show the next example I just want to go over a feature of AWS that
I love and use all the time and that's tagging. In EC2 you can set as many tags
as you want to any instance, we use 3 main ones for devops functionality
purposes as you will soon see. 

The three tags we have are:

Env- describes which environment that instance belongs to, which can be Prod,
puppystream or puppycrate, which are our production qa and test servers.

Type- which describes that instances functionality, whether it is a web worker,
a celery worker (data collection) or a manager instance which serves as a box
where we can run our shell on or execute tasks on that won't use up the
resources of our data collection or web app.

Lastly every box has a name which follows the pattern envrionment type and
number, prodcelery1 for example. 

Utilizing  these tags and the boto library we can do things like type specific scaling. For instance if we
wanted to scale our webservers up all we would have to do is type
fab prod scale:web,3

This fabric command calls a method on our AWSManager which is a custom python
object we made to simplify all regularly used boto commands.

This is a snippet of that manager object and I really just want to focus on the
scaling up portion of it. 

We first see how many web workers we have, and then scale by the difference. We
don't allow scaling below 2 for obvious reason. The actual scaling  simply
fetches the Master instance, which for us is the first of its type, so if we
were scaling our web workers for production, prodweb1 would be our master
instance. 


Upon every deploy we create an image of the master instance, and keep up to
3 images back. So for scaling what we do is we create a new instance with
identical details of the master instance, and use the latest image to quickly
create it. Usually only takes a minute or two. We tag it appropriately, so if
it is the third web instance we are spawning it would be named prodweb3. And
lastly if it is a web instance, we add it to our elastic load balancer.


--------------------------------------------------------------

This brings us to our last tool: Ansible

Ansible is an open source orchestration engine that manages nodes over SSH.

Now while ansible supports ad-hoc commands we don't really use them at all and
use what are called playbooks. 

Playbooks are the language by which ansible orchestrates configures administers
or deploys systems.
 
Playbooks consist of plays which are mappings between a set of hosts and the
tasks which run on those hosts.

Some quick pluses about playbooks are they are human readable, made with YAML
and Jinja2(Python templating engine), they can be synchronous or
asynchronous, and they have extensive module support.

Modules are the units of work that Ansible ships out to remote machines. They
can be imnplemented in any language. Ansible comes with a number of modules
called the module library that can be executed locally or on remote machines. 
This is an example of the git module, which we use in our deploy playbook.
Ansible supports user written modules as well. 

Here is an example ansible playbook that uses a yum module and linux service
module. 

This ansible playbook ensures that apache is the latest version, writes an
apache config, and then restarts apache on all webservers in the inventory. 

handlers - just like regular tasks but are only run if the task contains
a notify directive and also indicates that it changed something. So if nothing
changed in that apache playbook, it wouldn't restart apache as there would be
no point. 

Inventory is a file that describes hosts and groups in ansible (ini or json). 
Most inventories are static however ansible also supports dynamic inventories.

------------------------------------------------------------
Now that we have gone over all the tools I want to go over how they all play
together with our Deployment (by the way that is our office pup maven)


fab prod deploy

This is our deployment command that deploys  the latest master branch to
production. Fabric creates this command which it calls locally ( as we will let
ansible manage the remote host interactions). All this is doing is setting an
environment variable called ENVIRONMENT to prod, and executing the ansible
playbook deploy, specifying the folder that holds the hosts, and passing in the
variable branch=master.

 As mentioned earlier ansible supports dynamic hosts, and while they provide
 a host file for amazon specifically we found it didn't include everything we
 wanted so we implemented our own. This is a simple executable python script
 that outputs json. It grabs the envrionment variable ENVIRONMENT which we set
 earlier and using boto and the AWS api fetches all instances whose environment
 tag is prod. We then group these instances by type and name and assign
 variables to them that ansible will be able to use.

This is the resulting json.

So here is the actual playbook for our deploy. 

What this first play is saying is for the subset of hosts web run the deploy
role synchronously with the variable branch being whatever we passed it which
in this case is master. After the web hosts have been deployed, deploy to the
celery servers and manager servers asynchronously. 

Roles- are just simply a unit of organization and abstraction in ansible.
Allows certain tasks and variables to be grouped together usually by behavior,
for the purpose of reusability and readability.

The deploy role, for web workers, uses the ec2_elb module locally to
de-register the current web worker being deployed to synchronously. On our load
balancer we have connection draining enabled which allows existing requests to
complete before the load balancer shifts traffic away from a deregistered
instance. This option coupled with the synchronous deployment of our two
webworkers is how we achieve our seamless deploy rather easily. 

After the instance is de-registered or if the instance is a celery or manager
instance it runs the included deploy.yml file which simply contains all of the
actual deployment tasks.

Go over basic deployment tasks.

-----------------------------------------------------

That's it!

Thanks for listening to me ramble on

questions?

 
