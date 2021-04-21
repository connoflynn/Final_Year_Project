import tweepy
import time
import json
import os
import requests
import shutil
from yolo_img_impl import run_create
from get_spaces import get_details

def create_api():
    APIKey = ""
    APISecretKey = ""
    #BearerToken = ""

    AccessToken = ""
    AccessTokenSecret= ""

    auth = tweepy.OAuthHandler(APIKey, APISecretKey)
    auth.set_access_token(AccessToken,AccessTokenSecret)
    api = tweepy.API(auth)
    return api

#a function to delete the temperary files created when performing algorithm
def delete_files():
    if os.path.exists("twitter.jpg"):
        os.remove("twitter.jpg")
    if os.path.exists("twitter.json"):
        os.remove("twitter.json")
    if os.path.exists("twitter_output.png"):
        os.remove("twitter_output.png")

#function to retrieve media from a mention if it is present
def get_media(mention):
    media = mention.entities.get('media',[])
    #if media is present
    if media:
        # use requests to download the image and save it to a file called twitter.jpg
        # large needs to be added to the end of the url to get the correct size photo
        url =media[0]["media_url"]+":large"
        filename = "twitter.jpg"
        r = requests.get(url, stream = True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
    
            # open a local file and write with binary
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print("Image could not be downloaded")
        #run algorithm on the downloaded image
        run_algorithm(filename)
        return True
    else:
        return False

def reply(api):
    # get 20 most recent mentions using twitter api
    mentions = api.mentions_timeline()

    #open replied_to json file
    with open('replied_to.json') as json_file:
        #retrieve already replied to tweets from json file
        replied_to = json.load(json_file)
        for mention in mentions:
            already_replied_to = False
            for replied in replied_to["mentions"]:
                if replied["id"] == mention.id:
                    already_replied_to = True
            if already_replied_to == False:
                #check if the mention contains media
                media_present = get_media(mention)
                print(str(mention.id) + ' - ' + mention.text, flush=True)
                #set media part of the tweet
                if media_present:
                    media = api.media_upload("twitter_output.png")
                    # get the details of the free spaces
                    num_free_spaces, free_spaces = get_details("twitter.json")
                    #set text part of the tweet
                    if num_free_spaces == 0:
                        text = '@' + mention.user.screen_name + ' ' + 'There are no free spaces available!'
                    elif num_free_spaces == 1:
                        text = '@' + mention.user.screen_name + ' ' + 'There is ' + str(num_free_spaces) + ' free space available!'
                        text += "\nThe space available is: " + str(free_spaces[0])
                    else:  
                        text = '@' + mention.user.screen_name + ' ' + 'There are ' + str(num_free_spaces) + ' free spaces available!'
                        text += "\nThe spaces available are: "
                        for space_id in free_spaces:
                            text += str(space_id) + " "
                    print("Replying to tweet: " + str(mention.id) + " with media!")
                    post_result = api.update_status(status=text, media_ids=[media.media_id], in_reply_to_status_id=mention.id)
                else:
                    text = '@' + mention.user.screen_name + ' ' + 'Hello!'
                    print("Replying to tweet: " + str(mention.id) + " without media!")
                    post_result = api.update_status(status=text, in_reply_to_status_id=mention.id)
                replied_to['mentions'].append({'id' : mention.id, 'text' : mention.text, 'date': str(mention.created_at), 'user': "@" + mention.user.screen_name})
                with open('replied_to.json', 'w') as outfile:
                    json.dump(replied_to, outfile, indent=2)

                #delete the temporary files
                delete_files()
    
def run_algorithm(image):
    json_file = "spaces_coordinates_UFPR05.json"

    yolo_settings = dict()
    yolo_settings["yolo"] = "yolo-coco"
    yolo_settings["image"] = image
    yolo_settings["confidence"] = 0.4
    yolo_settings["threshold"] = 0.3

    run_create(yolo_settings, json_file)

def main():
    api = create_api()
    reply(api)

main()
