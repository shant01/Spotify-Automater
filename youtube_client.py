import os
from google.auth.transport import Request
import google_auth_oauthlib
import googleapiclient
import youtube_dl

class Song(object): 
    def __init__(self, artist, track): 
        self.artist = artist
        self.track = track

class YoutubeClient(object): 
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        flow = google_auth_oauthlib.flow.InstallAppFlow.from_client_secrets_file(
            credentials_location, scopes
        )
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )

        self.youtube_client = youtube_client
        

    def get_playlists(self): 
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=50,
            mine=True
        )
        response= request.execute()

        playlists = [playlist for playlist in response['items']]
        return playlists

    def get_videos_from_playlist(self,playlist_id): 
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId = playlist_id,
            part = "id, snippet"
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist, track = self.get_artist_and_track_from_video(video_id)
            if artist and track: 
                songs.append(Song(artist, track))

        return songs


    def get_artist_and_track_from_video(self,video_id): 
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download = False
        )

