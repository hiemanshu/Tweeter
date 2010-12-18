#!/usr/bin/env python

###
###
### Author : Hiemanshu Sharma <mail@theindiangeek.in>
###
### tweeter.py
###
### Python script to update twitter status
###
###

import twitter, sys, ConfigParser, os.path, traceback

__author__ = "Hiemanshu Sharma <mail@theindiangeek.in>"
version = 0.1-3

USAGE = '''Usage: tweeter.py command
    update <status>                      : Update your twitter status
    timeline [username]                  : Get your timeline or of username if username is specified
    replies                              : Get replies
    friends                              : Get list of friends
    follows                              : Get list of people that follow you
    favs                                 : Get list of your favourited tweets
    direct                               : Get Direct messages sent to you
    senddirect <username> <text>         : Send Direct message to [username]
    search <text>                        : Search for [text] on twitter
    follow <username>                    : Follow [username]
    unfollow <username>                  : Stop following [username]
    createlist <name> [public/private]   : Create a list by the name given with public/private access (It is public by default)
    dellist <username> <listname>        : Delete listname by [username] if you have access if you want to delete your own list username should be your own id
    addtolist <username> <listname>      : Subscribe to the list by [username]
    delfromlist <username> <listname>    : Unsubscribe to the list [listname] by [username]
    getconvo <status id>         : Fetches the full tweet conversation
 '''

DOCUMENTATION = '''The Consumer Key and Secret Pair and Access Token Key and secret pair are stored in ~/.tweetrc
The format for the file is :
    [Tweet]
    conskey: <Consumer Key>
    conssec: <Consumer Secret>
    accstkn: <Access Token Key>
    accssec: <Access Token Secret>

To add the above keys use add-auth parameter in the format i.e.,
add-auth <Consumer Key> <Consumer Secret> <Access Token Key> <Access Token Secret>
You can get the above values by registering your app at http://dev.twitter.com
'''

def addAuth():
    if cmp(sys.argv[1],"add-auth" == 0) and len(sys.argv) != 6:
        print sys.argv[1]
        print DOCUMENTATION
        sys.exit(2)
    elif cmp(sys.argv[1],"add-auth" == 0) and len(sys.argv) == 6:
        config.set("Tweet","conskey",sys.argv[2])
        config.set("Tweet","conssec",sys.argv[3])
        config.set("Tweet","accstkn",sys.argv[4])
        config.set("Tweet","accssec",sys.argv[5])
        config.write(open(os.path.expanduser('~/.tweetrc'),'w'))
        print "Access keys saved!"

def updateStatus(status):
    api.PostUpdates(status)
    print "Your status has been succesfully update"

def lengthCheck(status):
    if len(status) > 140:
        choice = raw_input("Your status is greater than 140 words, and will be split into multiple tweets. Do you want to continue (yes/no)? ")
        if cmp(choice,"yes") == 0 :
            updateStatus(status)
        if cmp(choice,"no") == 0 :
            print "Your status has not been updated."

def timeline():
    statues = api.GetUserTimeline(sys.argv[2])
    for s in statues:
        print s.text

def replies():
    replies = api.GetReplies()
    for l in replies:
        print "From : " + l.user.screen_name +  " \nMessage : %s\n" %l.text

def friends():
    friends = api.GetFriends()
    for k in friends:
        if cmp(k.name,k.screen_name) == 0:
            print ("Screen Name : %s" %k.screen_name)
        else:
            print ("Real Name :" + k.name +"        Screen Name: %s" %k.screen_name)

def follows():
    follows = api.GetFollowers()
    for k in follows:
        if cmp(k.name,k.screen_name) == 0:
            print ("Screen Name : %s" %k.screen_name)
        else:
            print ("Real Name :" + k.name +"        Screen Name: %s" %k.screen_name)

def direct():
    directs = api.GetDirectMessages()
    for h in directs:
        print ("From : " + h.sender_screen_name + "\nMessage : %s\n" %h.text)

def favs():
    favs = api.GetFavorites()
    for f in favs:
        print ("Tweet : %s by: %s(@%s)\n" %(f.text, f.user.name, f.user.screen_name))

def sendDirect(user,message):
    dm = api.PostDirectMessage(user,message)
    print "Message sent to %s" %user

def search(text):
    search=api.GetSearch(text)
    for s in search:
        print "%s : %s" %(s.user.screen_name,s.text)

def follow(user):
    k = api.CreateFriendship(user)
    print "You are now following " + k.user.screen_name

def unfollow(user):
    u = api.DestroyFriendship(user)
    print "You are not following %s anymore" % k.user.screen_name

def createList1(name,mode):
    l = api.CreateList('user',name,mode)
    print "List by the name %s has been created" %name

def createList2(name):
    l = api.CreateList('user',name)
    print "List by the name %s has been created" %name

def deleteList(user,list):
    api.DestroyList(user,list)
    print "List by the name %s has been deleted" %list

def addToList(user,list):
    api.CreateSubscription(user,list)
    print "You are now following the list %s by %s" %(user,list)

def delFromList(user,list):
    api.DestroySubscription(user,list)
    print "You are no longer following the list %s by %s" %(user,list)

def get_conversation(status_id):
    flag = 1
    tweet_count = 1
    while flag == 1:
        status = api.GetStatus(status_id)
        print ("%s%s")%(tweet_count*"-",status.text)
        if status.in_reply_to_status_id == None:
            break
        else:
            tweet_count = tweet_count + 1
            status_id = status.in_reply_to_status_id

def validate_parameters(num):
    if len(sys.argv) < num:
        print USAGE
        sys.exit(2)

### Check if config file has the section Tweet, if not add it
config = ConfigParser.ConfigParser()
if not config.has_section("Tweet"):
    config.add_section("Tweet")

### Print Usage if no arguments have been supplied or if -h / --help is an argument

if len(sys.argv) == 1 or sys.argv[1] in ("-h","--help"):
    print USAGE
    sys.exit(2)

### Check if file exists, if it doesn't exist and if user wants to add the keys
### If user doesn't want to add keys, show Documentation

check = os.path.isfile(os.path.expanduser('~/.tweetrc'))
if cmp(check,False) == 0:
    addAuth()

### Read Keys from file

config.read(os.path.expanduser('~/.tweetrc'))
conskey = config.get("Tweet", "conskey", raw=True)
conssec = config.get("Tweet", "conssec", raw=True)
accstkn = config.get("Tweet", "accstkn", raw=True)
accssec = config.get("Tweet", "accssec", raw=True)

### Create api object to be used

api = twitter.Api(consumer_key=conskey, consumer_secret=conssec, access_token_key=accstkn, access_token_secret=accssec)

### Different checks to see what the user wants to do

try :
    if cmp(sys.argv[1],"update") == 0:
        validate_parameters(3)
        status=' '.join(sys.argv[2:])
        lengthCheck(status)

    if cmp(sys.argv[1],"timeline") == 0:
        timeline()

    if cmp(sys.argv[1],"replies") == 0:
        replies()

    if cmp(sys.argv[1],"direct") == 0:
        direct()

    if cmp(sys.argv[1],"favs") == 0:
        favs()

    if cmp(sys.argv[1],"friends") == 0:
        friends()

    if cmp(sys.argv[1],"follows") == 0:
        follows()

    if cmp(sys.argv[1],"senddirect") == 0:
        validate_parameters(3)
        msg = ' '.join(sys.argv[3:])
        sendDirect(sys.argv[2],msg)

    if cmp(sys.argv[1],"search") == 0:
        validate_parameters(3)
        search(sys.argv[2])

    if cmp(sys.argv[1],"follow") == 0:
        validate_parameters(3)
        follow(sys.argv[2])

    if cmp(sys.argv[1],"unfollow") == 0:
        validate_parameters(3)
        unfollow(sys.arg[2])

    if cmp(sys.argv[1],"createlist") == 0:
        vaildate_parameters(3) 
        if len(sys.argv) == 4:
            createList1(sys.argv[2],sys.argv[3])
        if len(sys.argv) == 3:
            createList2(sys.argv[2])

    if cmp(sys.argv[1],"dellist") == 0:
        validate_parameters(4)
        deleteList(sys.argv[2],sys.argv[3])

    if cmp(sys.argv[1],"addtolist") == 0:
        validate_parameters(4)
        addToList(sys.argv[2],sys.argv[3])

    if cmp(sys.argv[1],"delfromlist") == 0:
        validate_parameters(4)
        delFromList(sys.argv[2],sys.argv[3])

    if cmp(sys.argv[1],"getconvo") == 0:
        validate_parameters(3)
        get_conversation(sys.argv[2])


except :
    print "Looks like something has gone wrong. Please check your internet connection and try again, or please email me at %s with the tweeter.log file as an attachment" % __author__
    traceback.print_exc(file=open("tweeter.log","a"))
