import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = '11ba8913b3694bfb89738b369efccb15'
SPOTIPY_CLIENT_SECRET = 'ccd77e9746ff46fab0b0a6db9a330f09'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                                         client_secret=SPOTIPY_CLIENT_SECRET))
START_DATE_SONGS = '2019-03-08'
END_DATE_SONGS = '2021-03-03'

spotify_dates = []
galgalatz_dates = ['2019-02-21','2019-02-28','2019-03-07','2019-03-14','2019-03-21','2019-03-28','2019-04-04','2019-04-11','2019-04-18','2019-05-16','2019-05-23','2019-05-30','2019-06-06','2019-06-13','2019-06-20','2019-06-27','2019-07-04','2019-07-11','2019-07-18','2019-07-25','2019-08-01','2019-08-08','2019-08-15','2019-08-22','2019-08-29','2019-09-05','2019-09-12','2019-09-19','2019-10-03','2019-10-10','2019-10-17','2019-10-24','2019-11-07','2019-11-14','2019-11-21','2019-11-28','2019-12-05','2019-12-12','2019-12-19','2020-01-02','2020-01-09','2020-01-16','2020-01-23','2020-01-30','2020-02-06','2020-02-13','2020-02-20','2020-02-27','2020-03-05','2020-03-12','2020-03-19','2020-03-26','2020-04-02','2020-04-16','2020-04-23','2020-04-30','2020-05-07','2020-05-14','2020-05-21','2020-06-04','2020-06-11','2020-06-18','2020-06-28','2020-07-09','2020-07-16','2020-07-23','2020-08-20','2020-08-27','2020-09-03','2020-09-24','2020-10-01','2020-10-08','2020-10-22','2020-11-05','2020-11-19','2020-11-26','2020-12-03','2020-12-17','2020-12-24','2021-01-07','2021-01-14','2021-01-21','2021-01-28','2021-02-11','2021-02-18','2021-02-25']

START_COVID19 = '2020-03-01'
START_LOCKDOWN1 = '2020-03-25'
END_LOCKDOWN1 = '2020-04-24'
START_LOCKDOWN2 = '2020-09-18'
END_LOCKDOWN2 = '2020-10-10'
START_LOCKDOWN3 = '2020-12-27'
END_LOCKDOWN3 = '2021-02-07'


class Song:
    def __init__(self, name, artist, track_id):
        self.name = name
        self.artist = artist
        self.weeks_list = []
        self.track_id = track_id


def get_top_songs_audio_features(list_of_dict_of_songs):
    track_ids = [songs['track_id'] for songs in list_of_dict_of_songs if songs['track_id'] is not None]
    hundred_track_ids = track_ids[:100]
    track_ids = track_ids[100:]
    audio_features_list = sp.audio_features(hundred_track_ids)
    while len(track_ids) > 0:
        hundred_track_ids = track_ids[:100]
        track_ids = track_ids[100:]
        audio_features = sp.audio_features(hundred_track_ids)
        audio_features_list.extend(audio_features)

    i = 0
    for audio_features in audio_features_list:
        song = list_of_dict_of_songs[i]
        result = sp.search(song['song_artist'])
        if len(result['tracks']['items']) > 0:
            track = result['tracks']['items'][0]
            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
            song['genre'] = artist["genres"]
        else:
            song['genre'] = None
        if audio_features is None:
            list_of_dict_of_songs.remove(song)
            continue
        song['danceability'] = audio_features['danceability']
        song['energy'] = audio_features['energy']
        song['key'] = audio_features['key']
        song['loudness'] = audio_features['loudness']
        song['mode'] = audio_features['mode']
        song['speechiness'] = audio_features['speechiness']
        song['acousticness'] = audio_features['acousticness']
        song['instrumentalness'] = audio_features['instrumentalness']
        song['liveness'] = audio_features['liveness']
        song['valence'] = audio_features['valence']
        song['tempo'] = audio_features['tempo']
        list_of_dict_of_songs[i] = song
        i += 1
    return list_of_dict_of_songs


def get_spotify_top_songs_of_month(country, start_month, end_month):
    start_curr_week = datetime.strptime(start_month, '%Y-%m-%d')
    end_curr_week = (start_curr_week + timedelta(days=7)).strftime('%Y-%m-%d')
    start_curr_week = start_curr_week.strftime('%Y-%m-%d')
    list_of_songs = []
    while (start_curr_week < end_month):
        print(start_curr_week, end_curr_week)
        week_songs = get_spotify_top_song_by_dates(country, start_curr_week, end_curr_week)
        list_of_songs.extend(week_songs)
        start_curr_week = datetime.strptime(end_curr_week, '%Y-%m-%d')
        end_curr_week = (start_curr_week + timedelta(days=7)).strftime('%Y-%m-%d')
        start_curr_week = start_curr_week.strftime('%Y-%m-%d')
    return list_of_songs


def get_spotify_top_song_by_dates(country, start_date, end_date):
    url = f"https://spotifycharts.com/regional/{country}/weekly/{start_date}--{end_date}"
    response = requests.request("GET", url)
    html_file = BeautifulSoup(response.text, "html.parser")
    songs_list_html = html_file.find_all('td', attrs={'class': 'chart-table-track'})

    list_songs_by_country_and_time = []
    print(len(songs_list_html))
    for i in range(0, len(songs_list_html)):
        dict = {}
        song_name_html = str(songs_list_html[i].find('strong'))
        song_name_html = re.sub('</strong>', '', song_name_html)
        song_name = re.sub('<strong>', '', song_name_html)
        dict['song_name'] = song_name
        song_artist_html = str(songs_list_html[i].find('span'))
        song_artist_html = re.sub('</span>', '', song_artist_html)
        song_artist = re.sub('<span>', '', song_artist_html)
        song_artist = re.sub('by ', '', song_artist)
        dict['song_artist'] = song_artist
        dict['start date'] = start_date
        if start_date not in spotify_dates:
            spotify_dates.append(dict['start date'])
        track_id = sp.search(q='artist:' + song_artist + ' track:' + song_name, type='track')
        if len(track_id['tracks']['items']) == 0:
            continue
        else:
            trackId = track_id['tracks']['items'][0]['id']
            dict['track_id'] = trackId
            list_songs_by_country_and_time.append(dict)
    return list_songs_by_country_and_time


def get_list_of_spotify_charts_songs(country):
    start_date_curr = datetime.strptime(START_DATE_SONGS, '%Y-%m-%d')
    end_date_curr = (start_date_curr + timedelta(days=28)).strftime('%Y-%m-%d')
    end_date = datetime.strptime(END_DATE_SONGS, '%Y-%m-%d')
    months_list = []
    while (start_date_curr < end_date):
        start_date_curr = start_date_curr.strftime('%Y-%m-%d')
        month_songs = get_spotify_top_songs_of_month(country, start_date_curr, end_date_curr)
        months_list.append(month_songs)
        start_date_curr = datetime.strptime(end_date_curr, '%Y-%m-%d')
        end_date_curr = (start_date_curr + timedelta(days=28)).strftime('%Y-%m-%d')

    songs_obj_list = []
    mapNameToSong = {}
    for month_songs in months_list:
        for song in month_songs:
            songsListName = [s.name for s in songs_obj_list]
            if not song['song_name'] in songsListName:
                songObj = Song(song['song_name'], song['song_artist'], song['track_id'])
                mapNameToSong[song['song_name']] = songObj
                songs_obj_list.append(songObj)
            songObj = mapNameToSong[song['song_name']]
            songObj.weeks_list.append(song['start date'])

    songs_list = []
    for songObj in songs_obj_list:
        song_dict = {}
        song_dict['song_name'] = songObj.name
        song_dict['song_artist'] = songObj.artist
        song_dict['track_id'] = songObj.track_id
        song_dict['weeks'] = songObj.weeks_list
        songs_list.append(song_dict)

    return songs_list


def get_list_of_galgalatz_songs(country):
    songs_obj_list = []
    mapNameToSong = {}

    with open('songs_utf8.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            track_id = sp.search(q=' track:' + row['song_name'],
                                 type='track', market='il')
            if len(track_id['tracks']['items']) == 0:
                continue
            track_id_val = track_id['tracks']['items'][0]['id']
            songsListName = [s.name for s in songs_obj_list]
            if not row['song_name'] in songsListName:
                songObj = Song(row['song_name'], row['song_artist'], track_id_val)
                mapNameToSong[row['song_name']] = songObj
                songs_obj_list.append(songObj)
            songObj = mapNameToSong[row['song_name']]
            songObj.weeks_list.append(row['week'])

    songs_list = []
    for songObj in songs_obj_list:
        song_dict = {}
        song_dict['song_name'] = songObj.name
        song_dict['song_artist'] = songObj.artist
        song_dict['track_id'] = songObj.track_id
        song_dict['weeks'] = songObj.weeks_list
        songs_list.append(song_dict)

    return songs_list


def create_analyzed_songs_csv(songs_list, name_of_source):
    get_top_songs_audio_features(songs_list)

    with open(f'{name_of_source}_songs.csv', 'w', encoding='utf8',
              newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=songs_list[0].keys(), )
        fc.writeheader()
        fc.writerows(songs_list)

    return songs_list


def create_lockdown_dict(dates_list):
    date_format = "%Y-%m-%d"
    covid_start = datetime.strptime(START_COVID19, date_format)
    l1_start = datetime.strptime(START_LOCKDOWN1, date_format)
    l1_end = datetime.strptime(END_LOCKDOWN1, date_format)
    l2_start = datetime.strptime(START_LOCKDOWN2, date_format)
    l2_end = datetime.strptime(END_LOCKDOWN2, date_format)
    l3_start = datetime.strptime(START_LOCKDOWN3, date_format)
    l3_end = datetime.strptime(END_LOCKDOWN3, date_format)
    dates_lockdown = []
    for date in dates_list:
        date_dict = {}
        date_dict['weeks_cols'] = date
        cur_date = datetime.strptime(date, date_format)
        if l1_start-timedelta(days=4) <= cur_date < l1_end-timedelta(days=3):
            date_dict['lockdown'] = 1
        elif l2_start-timedelta(days=4) <= cur_date < l2_end-timedelta(days=3):
            date_dict['lockdown'] = 2
        elif l3_start-timedelta(days=4) <= cur_date < l3_end-timedelta(days=3):
            date_dict['lockdown'] = 3
        else:
            date_dict['lockdown'] = 0
        if cur_date >= covid_start:
            date_dict['is_covid19'] = 1
        else:
            date_dict['is_covid19'] = 0
        dates_lockdown.append(date_dict)
    return dates_lockdown


def create_lockdown_csv(dates_list, name_of_source):
    dates_lockdown = create_lockdown_dict(dates_list)
    dates_lockdown = sorted(dates_lockdown, key=lambda row: datetime.strptime(row['weeks_cols'], "%Y-%m-%d"))

    with open(f'{name_of_source}_weeks_to_lockdown.csv', 'w', encoding='utf8',
              newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=dates_lockdown[0].keys(), )
        fc.writeheader()
        fc.writerows(dates_lockdown)

    return dates_lockdown


def create_csv(songs_list, name_of_source):
    with open(f'{name_of_source}_songs_before_analyze.csv', 'w', encoding='utf8',
              newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=songs_list[0].keys(), )
        fc.writeheader()
        fc.writerows(songs_list)


def import_csv(csv_name):
    list = []
    with open(csv_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            list.append(row)
    return list


def fill_spotify_dates(spotify_songs_list):
    for song in spotify_songs_list:
        text = song['weeks'][1:][:-1]
        weeks_list = list(text.split(", "))
        for week in weeks_list:
            week = week[1:][:-1]
            print(f"week={week}")
            if week not in spotify_dates:
                spotify_dates.append(week)


if __name__ == '__main__':
    country = 'il'
    # Spotify:
    spotify_songs_list = get_list_of_spotify_charts_songs(country)
    spotify_songs_list = create_analyzed_songs_csv(spotify_songs_list, "spotify_charts")
    spotify_dates_lockdown = create_lockdown_csv(spotify_dates, "spotify_charts")
    # Galgalaz:
    galgalatz_songs_list = get_list_of_galgalatz_songs(country)
    galgalatz_songs_list = create_analyzed_songs_csv(galgalatz_songs_list, "galgalatz")
    galgalatz_dates_lockdown = create_lockdown_csv(galgalatz_dates, "galgalatz")
