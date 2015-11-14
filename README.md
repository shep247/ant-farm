# ant-farm

<h2>Overview</h2>
This is a simple ant farm simulator built to try out the thespian actor system in conjunction with pygame.  The object of the simulation is for red and black "ants" to emerge from their respective "ant hills" and move in a random pattern, searching for a crumb.  When an ant smells a crumb, it proceeds to the crumb.  When it gets to the crumb, it changes course and returns back to its ant hill.  When it gets back to the ant hill, it returns back to the crumb and repeats this pattern until the simulation is exited.
<h2>How To Install:</h2>
<h3>Requirements:</h3>
Python 3.4 <br>
PyGame <br>
Thespian <br>
> pip3 install hg+http://bitbucket.org/pygame/pygame <br>
> pip3 install thespian <br>
<b>NOTE: </b> <i>I have found that if pygame is installed in a virtual environment, the pygame screen will not focus, and you will not be able to add ants.  I have not found a viable workaround for this yet.</i>

<h2>How to execute:</h2>
After the requirements are installed, navigate to the folder with this code and run "python ants.py"
A screen with 2 ant hills and a text block with "ANTS!" will appear.
To add ants, press the b key for black ants, and the r key for red ants.
To add crumbs, click in the whitespace anywhere
To remove ants, click on the ants.

<h2>How It Works:</h2>
There are 4 actor types involved in this design: <br>
<b>1) DrawerActor:  </b>This actor keeps track of everything.  The pygame board lives in this actor, and cannot be separated out into other actors, as pygame must stay single threaded.  Upon wakeup message, this actor redraws the board, including all ants and crumbs it knows about. It then sends all ant locations to the CrumbSpriteActor.  When ants send their new locations to this actor, it updates its dictionary of actors and their locations with the new location.  When the notifier actor notifies this actor of the removal of another actor, that actor is removed from the dictionary. <br>
<b>2) AntSpriteActor: </b>(red and black).  These actors wake up, incriment their location based on their movement algorithm, then send the new location to the drawer actor, then set an alarm to wake up again in (?) miliseconds.  <br>
<b>3) CrumbSpriteActor:  </b>This actor keeps track of all ant locations.  If the ant location is in the crumb's circle of space, the CrumbSpriteActor will send a message to the ant that contains the crumb location so the ant can navigate to the crumb. <br>
<b>4) ClickNotifier: </b>The ClickNotifier receives click notifications from the drawer actor and determines if an ant or blank space was clicked.  If an ant was clicked, the click notifier will send an ActorExitRequest to the clicked ant to stop it. <br>
