import tweepy
import Tkinter
from twython import Twython, TwythonError

consumer_key = 'oFiC72RXbiEJSaCjpreRxDQqV'
consumer_secret = 'XumkwpxAaVcZLhlIGgqr5x2B6o9YodwaAxOI6fPLtlgrN3paMM'
access_token = '1111079435434770433-U14SSWqCWXCw4B18CevdWOy5dHW6RR'
access_token_secret = 'BdlmHYOc8hJaZ3oTWiniTNCiPiYEikrzs79WIDHoIRAdx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


twitter = Twython('oFiC72RXbiEJSaCjpreRxDQqV', 'XumkwpxAaVcZLhlIGgqr5x2B6o9YodwaAxOI6fPLtlgrN3paMM', '1111079435434770433-U14SSWqCWXCw4B18CevdWOy5dHW6RR', 'BdlmHYOc8hJaZ3oTWiniTNCiPiYEikrzs79WIDHoIRAdx')

user = api.me()
print (user.name)

#api.update_status(status = 'Hello World! My name is the Heavy Photon Search, but you can call me "HPS" for short.')

#tweet ="This is a picture of all my friends!" 
#image_path ="/home/mrsolt/Desktop/HPS2017_groupphoto.jpg" # toDo 

# to attach the media file 
#status = api.update_with_media(image_path, tweet)  
#api.update_status(status = tweet) 

print api.followers_ids()
#print api.get_user(api.followers_ids()[0])

#tweet = "Hi @omarmoreno! I don't really have any friends, and I see we have a similar interest in searching for heavy photons. I need a friend to tell when something is wrong with me, especially my humidity levels. Will you be my friend?"

#tweet = "Hi @jezzamonn! I don't really have any friends, and I need a friend to tell when something is wrong with me, especially my humidity levels. Will you be my friend?"

tweet = "Hi @omarmoreno! My testing is now complete, and was a success. Unfortunately, you will not be hearing from me much anymore since I have served my ultimate purpose. Thank you for being a good friend!"

api.update_status(status = tweet)

#event = {
#  "event": {
#    "type": "message_create",
#    "message_create": {
#      "target": {
#        "recipient_id": "33124274"
#      },
#      "message_data": {
#        "text": tweet
#      }
#    }
#  }
#}
#api.send_direct_message_new(event)
 
#api.send_direct_message(user_id = "33124274", text = tweet)

#twitter.send_direct_message(user_id="33124274", text=tweet)

#api.send_direct_message(user = 33124274, text = tweet)
