from spotify_client import SpotifyClient
import os
from youtube_client import Playlist, YoutubeClient
from spotify_client import SpotifyClient

def run() :
    #1. Get a list of our playlists from Youtube
    youtube_client = YoutubeClient('./creds/client_secret.json')
    spotify_client = SpotifyClient('7bec4c7de6de4b96bf1268328bfd410e') 
    playlists = youtube_client.get_playlists()

    #2. Ask which playlist we want to get music video for
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")

    #3. For each video in playlist, get song info
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")

    #4. Search for the song on Spotify
    for song in songs: 
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id: 
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song: 
                print(f"Added Song {song.artist}")

    #5. If we found the song, add it to our Spotify Liked songs playlist
    

if __name__ == '__main__': 
    run()