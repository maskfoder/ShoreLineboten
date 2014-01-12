# -*- coding: utf-8 -*-
import tweepy, sys, random, time

consumer_token = ''
consumer_secret = ''
access_key = ''
access_secret = ''

#OAuth login
def OAuthLogin(consumer_token, consumer_secret):
    success = 1
    try:
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    except tweepy.TweepError:
        success = 0
    return success, auth

#Set access token
def SetAccessToken(auth, access_key, access_secret):
    success = 1
    try:
        auth.set_access_token(access_key, access_secret)  
    except tweepy.TweepError:
        success = 0
    return success, auth

#Get twitter api object
def GetAPIObject(auth):
    success = 1
    try:
        api = tweepy.API(auth)
    except tweepy.TweepError:
        success = 0
    return success, api

#Reads a random line from a text file and returns it.
def RandomLineFromFile(file_name):
    lyrics_lines = open(file_name).read().splitlines()    
    return random.choice(lyrics_lines)

#Create streamlistener class
class CustomStreamListener(tweepy.StreamListener):

    def __init__(self,api):
        self.api = api

    def on_status(self, status):
        try:
            #Mention
            if (self.api.me().screen_name in status.text) and (status.retweeted == False):
                print(time.strftime("%Y-%m-%d %H:%M:%S")+' Mention!')
                self.api.update_status('@'+status.user.screen_name+' '+RandomLineFromFile('shoreline.txt'), in_reply_to_status_id=status.id_str)                 
            #Retweet
            elif (status.user.id_str != self.api.me().id_str) and (status.retweeted == False):
                print(time.strftime("%Y-%m-%d %H:%M:%S")+' Retweet!')
                self.api.retweet(status.id)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

#main
def main():

    #Login using OAuth
    success, auth = OAuthLogin(consumer_token, consumer_secret)
    if (success != 1):
        print('Error logging in with OAuth')
        exit()

    #Set access key and secret
    success, auth = SetAccessToken(auth, access_key, access_secret)
    if (success != 1):
        print('Error setting access tokens')
        exit()
        
    #Get twitter API object
    success, api = GetAPIObject(auth)
    if (success != 1):
        print('Error getting Twitter API object')
        exit()

    # Create a streaming API and set a timeout value of 60 seconds.
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(api), timeout=60)
    streaming_api.filter(follow=None, track=['spela shoreline, spelar shoreline, @SPELA_SHORELINE']) 
        
if  __name__ =='__main__':
    main()
