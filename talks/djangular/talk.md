Title: Deployment at TrackMaven
Summary: TrackMaven implemented a custom deployment pipeline for Amazon Web
Services after migrating away from Heroku. The result supported multiple
environments, continuous integration, seamless fast deployments by using
Ansible, boto and Fabric. Come hear the behind the scenes details about what
works and what's still in progress for TrackMaven's all-AWS deployment
pipeline. 
  

Talk:

Senior software Maven at trackmaven, full stack engineer with an emphasis lately on the devops part of our stack


mattcamilli.com is my blog although not gonna lie I don't blog too often
although I'm trying to step that game up, I find everytime I go to blog I end
up rengineering the blog itself instead of writing. 

By the way this talk and fletchers data talk from yesterday will both be available online on our github accounts, I'll tweet when they go out.

Also to note, I like to keep my talks open if you have any questions or comments at any point in time just speak up.
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


----------------------------------------------
The Problem - Or How this talk came to be

At TrackMaven we wanted a fast and fluid UI/UX while working with a lot of
variable and constantly changing data. 

But at the time all we had was Django Templates. While Django Templates are
great, they are also very limited. Data only flows in one direction, from the
controllers to the template, asynchronous calls aren't possible without using
jQuery and those implementations always came off as janky.

So the solution we came to was that we would serve all of our data from
a backend Rest API and have the front end asynchronously interact with it using
a Javascript mvc framework which in this case was Angular.

I'm sure we have all seen this screen before, this is the first page in the
Django Tutorial. For this talk I'm going to essentially implement their same
polling app, but in the manner previously described, separating the client side and server side of the app entirely.

--------------------------------------------------------

I want to start on the backend with Django Rest Framework.


Django REST framework is a powerful and flexible toolkit
that makes it easy to build Web AyPIs it was started and is maintained by Tom
Christie.

It is 100% production ready and is even used by large companies such as Mozilla
and Eventbrite. 

As a quick shoutout they currently have a kickstarter campaign going to provide funding for a new major release of django rest framework which has currently already hit 5x their original goal and still has about 20 days to go. 

There are a couple rest frameworks for django but django rest framework has
a few notable features that put it above the rest. Web Browsable API
Authentication includes OAuth1 and OAuth2,Serialization support,Customizable,Extensive Documentation

Now to finally jump into some code, here are the django models for the polling
app. Pretty basic stuff, the question model contains a text field to hold the
question and a datetime field to store when it was written. The choice model
contains the text of the choice, how many votes it has, and what question it
ties too.

So in Django Rest Framework we have serializers which look similar to django
forms, but basically serve to serailize and desearilize models into json
objects, making them easy to read and consume on the front end.

Since these models are fairly simple and do not have any custom fields or types
that a database couldn't handle easily, we can simply use modelserializers
which just require that we point to the model we want to serialize, and then in
this use case we specifically state which fields we want to be serialized.

Given the simplicity of this app, we can use Class based views to easily serve
and consume our data. Django Rest Framework includes several class based views
that will solve most use cases.

As you can see the first class based view we have is the Question List, which
is a ListCreateAPIView, meaning this view allows gets that will return a list
of all questions, as well as a post which will allow any user with permissions
to make a new question.

The second view here is a simple retrieve view, allowing gets based on an
inputted criteria, in this case, we base it on the question_pk.

The last view type is the UpdateView, which will come in handy when we vote
a particular way on a poll question and need to update a particular choice's
vote count. 

And lastly this is the URLS.py which will basically connect the class based
views we just made with URL endpoints.

If we navigate to one of those endpoints we will see a feature I mentioned
previously which is the Web Browsable API. With the web api you can in browser
make different requests, gets posts puts, and see the output.

---------------------------
Coffeescript

Now I just want to come right out and say I'm mainly a python developer, I like
just too many things about the language and the syntax. Now as a developer it
is my misfortune to have to program javascript. I am not a fan of brackets,
there is a reason I left the java and microsoft world. So because I'm a python
developer and I like myself, I use coffeescript.

Compiles into JS
Inspired by Ruby and Python
Focuses on readability and brevity
Has built-in list comprehension and pattern matching

But the best justification for using coffeescript is to show the example they
have on their homepage. The left side is the python like coffeescript while the
right side is the horrifically verbose javascript

The reason I'm saying this is because all of my angular examples will be in
coffeescript

------------------------------
Angular JS

AngularJS is a client-side MVC framework written in Javascript, used to write
single page web applications. Through its dependency injection,two way data, 
binding, and what is known as the Zen of Angular, it has made itself stand out
amongst all the other clientside MVC frameworks, and is the main reason we
chose to use it with our app. 

I want to quickly share the zen of angular as it really speaks to the strengths
of the framework. 


Now let's start jumping into the code. This first file here is basically where
we define the angular module we are making, which we have named pollApp. We
specificy all the dependencies the module is based on, which we will get into
a bit later. 

Now by default, the angular templating language uses double brackets, just like
django, so this small snippet of code here makes it so that angular will use
square brackets, which will allow us to seamlessly use django's templating
engine and angular together. 

The last step for making angular and django play nice together is this quick
CSRF fix which simply grabs django's csrftoken and includes it in the necessary
header. The reason I am making this its own slide is because you would not
believe the amount of time it took for us to realize this was breaking most of
our app. 

Now that we have defined our angular module the next step is to then create a template, where you specify in the body tag, an ng-app directive which will point to the name of the angular module you just made. Directives are markers on a DOM
element (such as an attribute, element name, comment or CSS class) that tell
AngularJS's HTML compiler ($compile) to attach a specified behavior to that DOM
element or even transform the DOM element and its children. You can define your
own directives which we will show an example of in a little bit.

So now that we have our module and the template associated with it, let's get
some data to display on the app.Angular has what is known as services, which
are reusable business logic independent of the views wired together using
dependency injection. So for our purposes in this particular app we use services to create objects that will interact with the backend REST api we previously made to populate models on the front end. 

The first service we define here is a factory called Questions, it is dependent
on the log module, http module, and our defined service called Question which
we will get to next. It is initialized with a dictionary, with a key all that
points to an empty list, this is where we will store all the questions from the
backend. The first method we have defined is called fromServer which simply
takes question data and creates and stores Question objects from them. The
fetch method uses the http module to execute a get request to the rest api's
question list endpoint and then calls that fromServer command. Lastly we have
a data method which is a simple getter for the questions.


This brings us to the question class. this service depends on the log and http
modules as well as the Choice service. It creates a class Question which
includes a constructor to instantiate new Question objects with the init method
we have defined. This init method sets the total votes to 0 then for every
choice the data returns we add the choices votes to our current total and add
it to the question object as an instantiated choice. 

Lastly we have our choice class which contains that choice text, the id so we
can know which object to update on the backend, and the current number of votes
it has. It also has an update method that does a put request to the choices
endpoint we created to update the amount of votes that choice has.


Now that we have our data defined and the interactions with the backend
handled, it is time to define some views for this front end app. This is done
by states. To do that we use the ui-router module which isn't by default
included with angular, but has become a community accepted better alternative
to what angular comes default with. We start out by first using the built in angular router urlRouterProvider to define an otherwise, basically stating that if someone hits an endpoint that isn't defined, we will default to the home view. The first state we define, which will act as our home view, is our questionList. In this state we define the url in regex that will point to this state, the templateUrl, the controller, and the resolve which allows us to provide our template or controller with content or data that is custom to that particular state.


The next state we have is the questionDetail, which takes a question id as part
of the url, specifies the question Detail template with the
questionDetailController and the resolve simply fetches the question with that
id and passes it to the state.

This brings us to the controllers. Controllers are javascript functions that
hold the business logic behind views. They are mainly used to augment the
angular scope. Now scopes are basically  the glue between
application controller and the view. They are used to expose the domain model
to a view. We can assing properties to scope instances which then become
available on our template. The scope can be augmented with data and
functionatlity specific to a given view or state. Scopes will be your most
confusing part of programming angular, as sometimes it isn't exactly apparent
which scope you are in and exactly where you are in the hierarchy of scopes. 

Our first controller here simply takes the scope of our questionList and adds
all the questions our app has to it, allowing us to display those questions on
the template. 

The next controller is a tad more complicated, it is the questionDetail
controller It first instantiates certain scope properties, defaulting the
current question to the question fetched by that resolve in the state.
Defaulting a boolean voted to false, and the voteChoice to 0. It then defines
a vote method that loops through the possible choices until it reaches the one
that matches that voteChoice property we defined, increases its votes by 1 and
the total votes by 1, runs that choices update method to send that informtaion
to the back end, and sets the boolean to true.


Now these controllers interact with the templates defined with them on the
state. Templates are defined like this, script tags with ng-templates and an id
that will be the unique name that the state will call.

The quetion template uses the ng-repeat directive to iterate through all the
questions and add links to those questions. The ui-sref directive is ui-routers
way of mapping states to urls, here we call the questionDetail state and pass
in the current question.id, and then display the question text.

This brings us to the question detail template. The first part of the template
is the form, which has an ng-submit directive of vote(). Basically this means
on the submission of this form, call the vote function that we previously
defined on the scope. The ng-show directive means only display this form if
voted is still false. It then iterates through all of the choices, showing the
text and points to the ng-moel of $parent.voteChoice. The reason we call the
parent scope is whenever you do an ng-repeat it creates a scope particular to
just that loop, so we have to reach up to the parent ot access the controller
scope to set the vote choice. 

The second part of the questionDetail template is what is shown if voted
= true. Basically we want to display the results. So we basically iterate
through each choice, display the text and the votes associated with it and then
we have this div class that has a custom html attribute choice-percentage
attached to it. It also has the current votes set to the votes attribute and
total votes set to the total attribute. This is a custom directive. 

Basically we design this custom directive in directives.coffee called
choicePercentage. We restrict it to A which stands for attribute meaning any
attribute that matches choicePercentage will implement this directive. Other
possibilities here can be element, or class. The scope here means in the
directives scope, take the votes and total attributes and set them on the
directive scope as well. We then define the link method which allows us to
defin the logic behind the directive. Here we define an update method, which
sets the current elemtns css width percentage based on the percentage of total
votes that choice has. Then we have two scope watches which basically watch the
total and votes properties of the scope, and if they change, call the
previously defined update method. 


So here is a demo of it hopefully working.  

