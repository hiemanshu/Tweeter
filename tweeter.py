#!/usr/bin/env python

###
### Author : Hiemanshu Sharma <mail@theindiangeek.in>
###
###
### tweeter.py
###
### Python script to update twitter status
###
### TODO: Allow getting searches, add
### follow, unfollow, delete, list people you follow
###
###

import twitter, sys, ConfigParser, os.path

USAGE = '''Usage: tweeter.py command
    update <status>                 : Update your twitter status
    timeline                        : Get your user timeline
    replies                         : Get replies
    friends                         : Get list of friends
    follows                         : Get list of people that follow you
    direct                          : Get Direct messages sent to you
    senddirect <username> <text>    : Send Direct message to [username]
 '''

DOCUMENTATION = '''The Consumer Key and Secret Pair and Access Token Key and secret pair are stored in ~/.tweetrc
The format for the file is : 
    [Tweet]
    conskey: <Consumer Key>
    conssec: <Consumer Secret>
    accstkn: <Access Token Key>
    accssec: <Access Token Secret>
'''

check = os.path.isfile(os.path.expanduser('~/.tweetrc'))
if cmp(check,False) == 0:
    print DOCUMENTATION
    sys.exit(2)

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.tweetrc'))
conskey = config.get("Tweet", "conskey", raw=True)
conssec = config.get("Tweet", "conssec", raw=True)
accstkn = config.get("Tweet", "accstkn", raw=True)
accssec = config.get("Tweet", "accssec", raw=True)

api = twitter.Api(consumer_key=conskey, consumer_secret=conssec, access_token_key=accstkn, access_token_secret=accssec)
if len(sys.argv) == 1:
    print USAGE
    sys.exit(2);
if cmp(sys.argv[1],"-h") == 0:
    print USAGE 
    sys.exit(2);
if cmp(sys.argv[1],"update") == 0:
    api.PostUpdates(sys.argv[2])
if cmp(sys.argv[1],"timeline") == 0:
    statues = api.GetUserTimeline()
    for s in statues:
        print s.text
if cmp(sys.argv[1],"replies") == 0:
    replies = api.GetReplies()
    for l in replies:
        print "From : " + l.user.screen_name +  " \nMessage : %s\n" %l.text 
if cmp(sys.argv[1],"direct") == 0:
    directs = api.GetDirectMessages()
    for h in directs:
        print ("From : " + h.sender_screen_name + " Message : %s" %h.text)
if cmp(sys.argv[1],"friends") == 0:
    friends = api.GetFriends()
    for k in friends:
        if cmp(k.name,k.screen_name) == 0:
            print ("Screen Name : %s" %k.screen_name)
        else:
            print ("Real Name :" + k.name +"        Screen Name: %s" %k.screen_name)
if cmp(sys.argv[1],"follows") == 0:
    follows = api.GetFollowers()
    for k in follows:
        if cmp(k.name,k.screen_name) == 0:
            print ("Screen Name : %s" %k.screen_name)
        else:
            print ("Real Name :" + k.name +"        Screen Name: %s" %k.screen_name)
if cmp(sys.argv[1],"senddirect") == 0:
    dm = api.PostDirectMessage(sys.argv[2],sys.argv[3])
    print "Message sent to %s" %sys.argv[2]
