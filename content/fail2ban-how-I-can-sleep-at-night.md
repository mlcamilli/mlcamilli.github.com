Title: Fail2ban: How I can sleep at night
Date: 2013-11-09 8:20
Category: DevOps
Tags: devops, fail2ban
Slug: fail2ban-how-I-can-sleep-at-night
Author: Matt Camilli

It was a casual day at the TrackMaven office when I just so happened to peruse through the logs
on our linode servers. To my dismay I saw a lot of this:
	
	reverse mapping checking getaddrinfo for xxx.xxx.xx.xxx failed - POSSIBLE BREAK-IN ATTEMPT!
	input_userauth_request: invalid user admin
	Received disconnect from xxx.xxx.xx.xxx: 11: Bye Bye
	Invalid user test1 from xxx.xxx.xx.xxx
	reverse mapping checking getaddrinfo for xxx.xxx.xx.xxx failed - POSSIBLE BREAK-IN ATTEMPT!
	input_userauth_request: invalid user super
	Received disconnect from xxx.xxx.xx.xxx: 11: Bye Bye
	Invalid user test from xxx.xxx.xx.xxx
	reverse mapping checking getaddrinfo for xxx.xxx.xx.xxx failed - POSSIBLE BREAK-IN ATTEMPT!
	input_userauth_request: invalid user test
	Received disconnect from xxx.xxx.xx.xxx: 11: Bye Bye

Wooo someone somewhere had a bot which was trying to gain access to our server; fun stuff.
While I had already secured our SSH via not allowing root login, using key authentication etc. (more instructions [here](#otherarticle))

So to stop this from happening I installed Fail2ban. Fail2ban is a tool that monitors logs and temporarily bans users based on
defined events, which in this case is brute forcing our SSH connection.

To install:

	sudo apt-get install fail2ban

The defaults will actually do a lot for you, but some further customization won't hurt either.

	sudo cp /etc/fail2ban/jail.{conf,local}

Run that command to have a customizable config file in which you can add ip's to whitelist (not get banned)
as well as which jails (rules) you want to enable. The rules are arrays of regex lines to look for in particular logs.
When found at a defined frequency, it will temporarily ban the offending IP address. 

While the default jail for SSH is great it unfortunately does not prevent preauth attempts (using a not allowed user)

So to fix this you'll need to

	sudo vim /etc/fail2ban/filter.d/sshd.conf

And add this line to the failregex = 

	^%(__prefix_line)sReceived disconnect from <HOST>: 11: Bye Bye \[preauth\]\s*$

Restart the server and you are good to go with fail2ban

	sudo service fail2ban restart

Now just type this command to see all the people you have banned!

	sudo iptables -L


