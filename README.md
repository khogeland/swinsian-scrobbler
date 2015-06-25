# setup

- save swinsian-scrobbler.py somewhere
- edit the python file with your username and password (and api keys if you want to change them)
- save com.kevinhogeland.swinsianscrobbler.plist to ~/Library/LaunchAgents/
- edit the plist file with the (absolute) path to the python file
- in terminal, run:
```
    sudo pip install pylast
    launchctl load ~/Library/LaunchAgents/com.kevinhogeland.swinsianscrobbler.plist
```
- that's it, just start listening :~)
- to remove it, either run the above command with "unload" instead or delete the plist/py files

scrobbling (but not "now listening") songs with unicode characters seems to be broken using python 2.7 - maybe try 3.x
