#!/usr/bin/env python
from __future__ import unicode_literals
import Foundation
import subprocess
import threading
import pylast
import time
from AppKit import *
from PyObjCTools import AppHelper

API_KEY = "ee6d965488421f5edc8021b2a8440797"     #replace these with your own api keys if you want to change the scrobbler name
API_SECRET = "f1feb09f42718ab70fc0ad141b19b90f"  #these ones will show up as "scrobbling from a faraway land"
username = "YOUR USERNAME HERE"
password_hash = pylast.md5("YOUR PASSWORD HERE")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)

playing = False

def asrun(ascript):
  "Run the given AppleScript and return the standard output and error."

  osa = subprocess.Popen(['osascript', '-'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
  return osa.communicate(ascript)[0]

def asquote(astr):
  "Return the AppleScript equivalent of the given string."
  
  astr = astr.replace('"', '" & quote & "')
  return '"{}"'.format(astr)

class Paused(NSObject):
    def paused_(self, song):
        global playing
        playing = False

class GetSongs(NSObject):
    def getMySongs_(self, song):
        global playing
        playing = True
        song_details = {}
        ui = song.userInfo()
        song_details = dict(zip(ui.keys(), ui.values()))
        timestamp = int(time.time())
        network.update_now_playing(song_details['artist'],song_details['title'],song_details['album'])
        if song_details['currentTime'] == 0.0:
        	observer = ObserveSong(song_details, timestamp)
        	observer.start()

class ObserveSong(threading.Thread):
    def __init__(self, song_details_arg, timestamp_arg):
        threading.Thread.__init__(self)
        self.song_details = song_details_arg
        self.timestamp = timestamp_arg
    def run(self):
        half_length = self.song_details['length']/2
        loops = 0
        while asrun('tell application "Swinsian"\nset thetrack to current track\nset trackname to name of thetrack\nend tell').strip() == self.song_details['title']:
            if playing:
                if loops * 5 > half_length:
                    network.scrobble(self.song_details['artist'],self.song_details['title'],self.timestamp,self.song_details['album'])
                    break
                loops += 1
            time.sleep(5)

nc = Foundation.NSDistributedNotificationCenter.defaultCenter()
Paused = Paused.new()
GetSongs = GetSongs.new()
nc.addObserver_selector_name_object_(GetSongs, 'getMySongs:', 'com.swinsian.Swinsian-Track-Playing',None)
nc.addObserver_selector_name_object_(Paused, 'paused:', 'com.swinsian.Swinsian-Track-Paused',None)
NSLog("Observers ready")
AppHelper.runConsoleEventLoop()
