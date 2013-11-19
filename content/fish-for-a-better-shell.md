Title: Fish for a better shell
Date: 2013-11-19 10:20
Category: Developer Tools
Tags: fish, shell, bash
Slug: fish-a-better-shell
Author: Matt Camilli
Description:Put some power into your shell and upgrade to fish. http://fishshell.com/

On any given day I'd say at least 60% of my time is spent in the shell doing this or that. 

A little while ago, I was doing a google search, and after typing the first word google did its
normal routine and auto completed my search. It was then I thought to myself, why doesn't that exist in my shell?

![brilliant](http://i1138.photobucket.com/albums/n527/The44thHour/DWBrilliant.gif)

Lucky for me, someone had already implemented that idea with a myriad of other shell improvements. 

[Fish](http://fishshell.com/) is a "smart and user-friendly command line shell for OS X, Linux and [unfortunately] Windows."

Right out of the box with fish you get:

- autosuggestsion ![autosuggestions](http://fishshell.com/assets/img/screenshots/autosuggestion.png)
- glorious colors ![colors](http://fishshell.com/assets/img/screenshots/colors.png)
- powerful scripting ![scripting](http://fishshell.com/assets/img/screenshots/scripting.png)

Installing it was as easy as going to their website downloading the .deb and clicking on it or you know, being a boss and using the shell.

	sudo apt-get install fish

If you are using linux which you should be, you can set this to be your default shell by typing this command

	chsh -s /usr/bin/fish

And then logging in and out

If at anytime you want to run a bash script you can just simply type

	~> bash somescript.sh

After I had installed it I immediately was loving it, the auto complete feature alone was saving me tons of time in my day.

HOWEVER, virtualenvwrapper doesnt work with fish, which for a python developer like me, was just unacceptable. 

Thankfully some really cool dude out there made [virtualfish](https://github.com/adambrenecki/virtualfish) which is basically
virtualenvwrapper for fish

To install virtualfish you'll want to save this [file](https://raw.github.com/adambrenecki/virtualfish/master/virtual.fish) to
	
	~/.config/fish/virtual.fish

and then edit your config.fish to path to it. Example config.fish:

	set -U VIRTUALFISH_HOME "/home/boos3y/Dev/.virtualenvs"
	. /home/username/.config/fish/virtual.fish
	### Added by the Heroku Toolbelt
	set -U PATH "/usr/local/heroku/bin:$PATH"

And voila! virtualfish will be installed.

Lastly you will want your shell to show that you actually are in the virtual environment, with an indicator looking like 
	
![this](http://i.imgur.com/65ZoFlp.png)

To do this type `funced fish_prompt` and add this line in

	if set -q VIRTUAL_ENV
    	echo -n -s (set_color -b blue white) "(" (basename "$VIRTUAL_ENV") ")" (set_color normal) " "
	end
and then type `funcsave fish_prompt` 
