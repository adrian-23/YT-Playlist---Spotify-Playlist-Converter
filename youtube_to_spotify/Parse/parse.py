#https://www.youtube.com/watch?v=l_fXOgeTp4E&list=PLwYyk0NgX83PLPfzg6BPxtTIrkw7L2zHb&index=9
import re
from youtube_title_parse import get_artist_title
from youtube_to_spotify.config import Config
import sys

class Parse:

    """
        Description:
            parses the given youtube link 
        Parameters:
            url: the given URL of the user
        Return:
            returns a list of titles of songs 
    """
    cfg = Config()
    def parse_youtube_url(self,url:str):
        #if the gives a url that is only a video then playlist id can be null
        items = []
        # get established service
        yt = self.cfg.youtube
        
        #retrieve the playlist id from the given url
        id = re.search('list=', url)
        index = re.search('\&index=',url)
        if id is None:
            raise Exception('Playlist ID not found')
        elif index:
            id_start = id.span()[1]
            id_end = index.span()[0]
            playlistId= url[id_start:id_end]
        else:
            id_start = id.span()[1]
            playlistId = url[id_start:]
        request = yt.playlistItems().list(
        part="snippet,contentDetails,id,snippet,status",
        playlistId = playlistId,
        maxResults = 50
    )
        response = request.execute()
        print("-------------------------------------------------------------------")
        print("BEGINNING CONVERSION")
        print("-------------------------------------------------------------------")
        for item in response['items']:
            items.append(item['snippet']['title'])
            print(f'Converting {item["snippet"]["title"] }')
        
        return items

    """
        Description:
            Process the user's videos into a spotify playlist
        Parameters:
            user_option
                1 - create a new playlist then add all of the user's videos into that 
                playlist.
                
                2 - add all of the user's videos into an existing playlist

                3 - exit out of the program
            
            user_items
                the videos of the playlist that the user has given
        Return:
    """
    def convert_to_spotify_playlist(self,user_option, user_items):
        user_id = self.cfg.spotify.me()['id']
        
        if user_option == 1:
            #Create the playlist
            playlist = str(input('Enter Below the name of the playlist:\n'))
            playlist = self.cfg.spotify.user_playlist_create(user_id,playlist)
            self.search_and_add((user_id,user_items), playlist)
        elif user_option == 2:
            pass
        else:
            sys.exit(0)

    """
        Description:
            
        Parameters:
            user_info 
                A tuple that consists of the user's (id, playlist_items)
            
            playlist_name:
                name the user has given for that playlist
        Return:
    """
    def search_and_add(self, user_info, playlist):
        for song in user_info[1]:
            
            #Parse the song information then search if the song exists

            try:
                artist, title = get_artist_title(song)
            except TypeError:
                continue
            artist = artist.replace('& ', ',')
            title = self.remove_parenthesis(title)
            result = self.cfg.spotify.search(f'{title} {artist}')
            
            if result['tracks']['items']:
                
                print(f'{title} - {artist} found adding to playlist: {playlist["name"]}\n')
                #Grab the first item in the tracks
                track = result['tracks']['items'][0] 
                
                self.cfg.spotify.playlist_add_items(playlist['id'], [f'spotify:track:{track["id"]}'])
            else:
                print(f'{title} - {artist} ***NOT FOUND***. Unable to add to playlist: {playlist["name"]}\n')

    @staticmethod
    def remove_parenthesis(word):
        start = 0
        count = 0
        for i,letter in enumerate(word):
            if letter=='(':
                start = i
                word=word[0:start]
                count+=1
        return word


