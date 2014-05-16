Title: The Glory of Redis Pipelines 
Date: 2014-01-23 5:20
Category: Python
Tags: python, redis, pipeline
Slug: glory-of-redis-pipelines
Author: Matt Camilli
Description: Save yourself and your app a lot of overhead and connection time by using pipelines to drastically increase performance.

    :::py
    import test

Like most python developers, and developers in general, I use Redis for pretty much everything. It is the developer's
swiss army knife and boy does it get the job done. 

Not too long ago we implemented a new feature at TrackMaven that heavily depended on reading and writing a lot to redis. What we noticed
almost instantly was the performance hit we were taking in just redis connections. 

A basic redis implementation may look something like this

    :::python

	import redis

	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	value = r.get('somekey')

Or in our case, we had to get a bunch of specific keys out of a HashSet

	:::py
	keys = ['01102014', '01112014', '01122014', '01132014', '01142014', '01152014', '01162014']
	values = []
	for key in keys:
		values.append(r.hget('somekey', key))

And while this worked, we were seeing a lot of overhead in redis connections. This is because every time
that hget is called it opens a connection to redis. 

We were fortunately able dramatically reduce this overhead by using redis pipelines. 
A pipeline is basically a subclass of the redis instance that allows support for buffering multiple commands
to the redis server in a single request. 

So taking our previous example we refactored to make it look like this

    :::python
	keys = ['01102014', '01112014', '01122014', '01132014', '01142014', '01152014', '01162014']
	pipe = r.pipeline()
	for key in keys:
		pipe.hget('somekey', key)
	values = pipe.execute()

The execute command sends the request, and returns the response which is an array of the return values
of each command, in order. 

So save yourself some time and your redis some connections and use pipelines. 


	

