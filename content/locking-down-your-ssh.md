Title: Locking down your ssh
Date: 2010-12-03 10:20
Category: DevOps
Tags: devops, ssh
Slug: locking-down-your-ssh
Author: Matt Camilli
Description:So SSH is great, I use it just about everyday. I ssh into my linode as root like a baus and use password authentication because no one is gonna guess my password which is my last name twice, right?

So SSH is great, I use it just about everyday. I ssh into my linode as root like a baus
and use password authentication because no one is gonna guess my password which is my 
last name twice, right?

Okay that isn't what I do but it is so embarassingly close to what I used to do. Then after I
read a blog post about someone else's box getting hacked because their SSH wasn't secure, I quickly 
changed my tune. I can't risk having my linode hacked, WHAT WOULD HAPPEN TO MY MINECRAFT SERVER?!

So how do you go about doing just that? Well for starters you are going to want to use key
authentication because it is essentially better in every respect. 

If you don't have an ssh key on your computer, go [here](https://help.github.com/articles/generating-ssh-keys) and do that. (Thanks github for the step by step)

Then you will want to add that key toyour servers authorized key file by doing this

	mkdir ~/.ssh
	echo "yourpublickey" > ~/.ssh/authorized_keys

Next you will want to put these settings in your ssh config file : 

	PermitRootLogin no
	PermitEmptyPasswords no
	PasswordAuthentication no
	AllowUsers youruser

And then restart the ssh server

	sudo service ssh restart

Voila! Your server just became significantly harder to break into.