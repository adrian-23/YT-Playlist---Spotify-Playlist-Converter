from youtube_to_spotify import cfg, parser

given_url = cfg.prompt_user()

#parse the given url and get a list of videos
video_items = parser.parse_youtube_url(given_url)

#send the list in the spotify api for processing
spotify_option = cfg.spotify_creds(video_items)
parser.convert_to_spotify_playlist(spotify_option, video_items)
