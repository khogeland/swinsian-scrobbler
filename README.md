# setup

- save swinsian-scrobbler.py somewhere
- edit the python file with your username and password (and api keys if you want to change them)
- save com.kevinhogeland.swinsianscrobbler.plist to ~/Library/LaunchAgents/
- edit the plist file with the (absolute) path to the python file
- in terminal, run:
```launchctl load ~/Library/LaunchAgents/com.kevinhogeland.swinsianscrobbler.plist```
- that's it, just start listening :~)
- to remove it, either run the above command with "unload" instead or delete the plist/py files
