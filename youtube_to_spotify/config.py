from typing import List
import os
from googleapiclient.discovery import build
import google_auth_oauthlib.flow 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import argparse



class Config(object):
    api_key= os.environ.get('youtube_key')
    client_secret = os.path.realpath('client_secret.json')
    
    scopes = ["https://www.googleapis.com/auth/youtube"]

    print(f'client_secret type: {type(client_secret)}')
    
    #create services

    #Youtube
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret, scopes)
    
    credentials = flow.run_console()
    youtube = build('youtube','v3', developerKey = api_key, credentials= credentials)
    
    #Spotify
    
    scope='playlist-modify-public'
    auth_manager = SpotifyOAuth(scope=scope)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    
    
    # spotify.user_playlist_create(user_id, args.playlist)
    #retrieve youtube api data (Parse takes care of this)
    
    #send data to spotify
    
    
    def prompt_user(self) -> str :
        user_url = str(input('Please input Youtube URL here\n'))

        return user_url


    def spotify_creds(self, playlist_items:List):
        
        print("-------------------------------------------------------------------")
        print("OPTIONS SELECTION")
        print("-------------------------------------------------------------------")
        options = ['create new playlist', 'add to existing playlist', 'exit']
        for i,option in enumerate(options):
            print(f'{i+1} - {option}')

        print("-------------------------------------------------------------------")
        print("OPTIONS SELECTION")
        print("-------------------------------------------------------------------")
        
        while(True):
            
            try:
                user_option = int(input('Put Selected Option here:\n'))
            except ValueError:
                print('Please type in a number. Try Again\n')
            else:
                if 0 < user_option <= len(options):
                    return user_option
                    
                else:
                    print('Invalid option. Try Again.\n')