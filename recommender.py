"""
recommender.py - MoodTune recommender module

This file keeps the main recommendation logic.
It reads songs from csv files, scores songs, makes playlists,
and saves liked songs.
"""

import csv
import random
from collections import Counter
from pathlib import Path

from song import Song


class MusicRecommender:
    # These fields are the standard format used by both csv files.
    STANDARD_FIELDS = [
        'title',
        'artist',
        'genre',
        'mood',
        'energy',
        'language',
        'scene',
        'popularity',
        'tempo',
        'danceability',
        'valence',
    ]

    # These fields are the minimum information needed to make a song useful.
    REQUIRED_FIELDS = ['title', 'artist', 'genre', 'mood', 'energy', 'language']

    def __init__(self, library_file='song_library.csv', liked_file='liked_songs.csv'):
        self.library_file = Path(library_file)
        self.liked_file = Path(liked_file)

        self.songs = []
        self.liked_songs = []

        self.load_songs()
        self.load_liked_songs()

    def load_songs(self):
        self.songs = self.load_song_file(self.library_file)
        self.normalise_song_file(self.library_file, self.songs)

    def load_liked_songs(self):
        if not self.liked_file.exists():
            self.create_empty_song_file(self.liked_file)

        self.liked_songs = self.load_song_file(self.liked_file)
        self.normalise_song_file(self.liked_file, self.liked_songs)

    def create_empty_song_file(self, file_path):
        # Create a csv file with only the header row.
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.STANDARD_FIELDS)

    def file_needs_normalising(self, file_path):
        # This checks if the csv header is old or incomplete.
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader, [])
        except FileNotFoundError:
            return False
        except csv.Error:
            return False

        header = [item.strip() for item in header]

        if not header:
            return True

        for field in self.REQUIRED_FIELDS:
            if field not in header:
                return True

        return header != self.STANDARD_FIELDS

    def normalise_song_file(self, file_path, songs):
        # If the file uses an old header, rewrite it with the new 11-column format.
        if self.file_needs_normalising(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.STANDARD_FIELDS)

                for song in songs:
                    writer.writerow(song.to_list())

    def load_song_file(self, file_path):
        songs = []

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    self.create_empty_song_file(file_path)
                    return []

                for row in reader:
                    title = (row.get('title') or '').strip()
                    artist = (row.get('artist') or '').strip()

                    # Skip empty rows, because they cannot be recommended.
                    if not title or not artist:
                        continue

                    song = Song(
                        title,
                        artist,
                        row.get('genre', 'Unknown'),
                        row.get('mood', 'Unknown'),
                        row.get('energy', 'Unknown'),
                        row.get('language', 'Unknown'),
                        row.get('scene', ''),
                        row.get('popularity', 50),
                        row.get('tempo', ''),
                        row.get('danceability', 50),
                        row.get('valence', 50),
                    )
                    songs.append(song)

        except FileNotFoundError:
            print(f'Warning: {file_path} was not found. An empty file has been created.')
            self.create_empty_song_file(file_path)
        except csv.Error:
            print(f'Warning: {file_path} could not be read correctly.')

        return songs

    def get_available_values(self, attribute):
        # Used by main.py to build the option lists from the csv data.
        values = set()

        for song in self.songs:
            value = getattr(song, attribute, '')

            if value and str(value).lower() != 'unknown':
                values.add(value)

        return sorted(values)

    def matches(self, song_value, user_value):
        if not user_value:
            return False

        return str(song_value).lower() == str(user_value).lower()

    def get_scene_reason(self, scene):
        # Make the scene reason easier to read in the output.
        scene_reasons = {
            'study': 'good for studying',
            'walking': 'good for walking',
            'travel': 'good for travelling',
            'workout': 'good for working out',
            'relaxing': 'good for relaxing',
            'party': 'good for a party',
            'sleep': 'good for sleeping',
            'commute': 'good for commuting',
        }

        return scene_reasons.get(scene.lower(), f'good for {scene}')

    def score_song(self, song, mood='', genre='', energy='', language='', scene='', tempo=''):
        score = 0
        reasons = []

        liked_artists = set()
        for liked_song in self.liked_songs:
            liked_artists.add(liked_song.artist.lower())

        # The weights below decide how important each preference is.
        if self.matches(song.mood, mood):
            score += 4
            reasons.append('mood matched')

        if self.matches(song.genre, genre):
            score += 3
            reasons.append('genre matched')

        if self.matches(song.energy, energy):
            score += 2
            reasons.append('energy matched')

        if self.matches(song.language, language):
            score += 1
            reasons.append('language matched')

        if self.matches(song.scene, scene):
            score += 2
            reasons.append(self.get_scene_reason(song.scene))

        if self.matches(song.tempo, tempo):
            score += 1
            reasons.append('tempo matched')

        if song.popularity >= 80:
            score += 1
            reasons.append('high popularity')

        if song.artist.lower() in liked_artists:
            score += 2
            reasons.append('you liked this artist before')

        return score, reasons

    def score_all_songs(self, mood='', genre='', energy='', language='', scene='', tempo=''):
        scored_songs = []

        for song in self.songs:
            score, reasons = self.score_song(song, mood, genre, energy, language, scene, tempo)
            scored_songs.append((song, score, reasons))

        # Shuffle first so songs with the same score do not always appear in the same order.
        random.shuffle(scored_songs)

        scored_songs.sort(
            key=lambda item: (
                item[1],
                item[0].popularity,
                item[0].danceability,
                item[0].valence,
            ),
            reverse=True,
        )

        return scored_songs

    def recommend_song(self, mood='', genre='', energy='', language='', scene='', tempo=''):
        if not self.songs:
            return None, 0, ['song library is empty']

        scored_songs = self.score_all_songs(mood, genre, energy, language, scene, tempo)
        return scored_songs[0]

    def generate_playlist(self, mood='', genre='', energy='', language='', scene='', tempo='', playlist_size=5):
        if not self.songs:
            return []

        scored_songs = self.score_all_songs(mood, genre, energy, language, scene, tempo)
        return scored_songs[:playlist_size]

    def get_song_key(self, song):
        # I use title + artist to check if two songs are the same.
        return song.title.lower(), song.artist.lower()

    def pick_playlist_item(self, playlist, used_keys, rule):
        # First try to find a song that fits the playlist role.
        for item in playlist:
            song = item[0]

            if self.get_song_key(song) not in used_keys and rule(item):
                return item

        # If no song fits that role, just take the next unused song.
        for item in playlist:
            song = item[0]

            if self.get_song_key(song) not in used_keys:
                return item

        return None

    def build_playlist_flow(self, playlist):
        if not playlist:
            return [], []

        # These labels make the playlist look more like a real listening flow.
        flow_rules = [
            ('Warm-up track', lambda item: item[0].energy.lower() in ['low', 'medium']),
            ('Main mood match', lambda item: 'mood matched' in item[2]),
            ('Energy boost', lambda item: item[0].energy.lower() == 'high'),
            ('Popular pick', lambda item: item[0].popularity >= 80),
            (
                'Calm ending',
                lambda item: item[0].energy.lower() == 'low'
                or item[0].scene.lower() in ['relaxing', 'sleep'],
            ),
        ]

        flow_count = min(5, len(playlist))
        used_keys = set()
        flow_items = []

        for label, rule in flow_rules[:flow_count]:
            selected = self.pick_playlist_item(playlist, used_keys, rule)

            if selected is None:
                break

            song = selected[0]
            used_keys.add(self.get_song_key(song))
            flow_items.append((label, selected[0], selected[1], selected[2]))

        extra_items = []

        for song, score, reasons in playlist:
            if self.get_song_key(song) not in used_keys:
                extra_items.append((song, score, reasons))

        return flow_items, extra_items

    def get_library_statistics(self):
        mood_counter = Counter()
        genre_counter = Counter()
        scene_counter = Counter()
        language_counter = Counter()
        high_energy_songs = 0

        for song in self.songs:
            if song.mood and song.mood.lower() != 'unknown':
                mood_counter[song.mood] += 1

            if song.genre and song.genre.lower() != 'unknown':
                genre_counter[song.genre] += 1

            if song.language and song.language.lower() != 'unknown':
                language_counter[song.language] += 1

            if song.scene:
                scene_counter[song.scene] += 1

            if song.energy.lower() == 'high':
                high_energy_songs += 1

        most_common_mood = 'N/A'
        if mood_counter:
            most_common_mood = mood_counter.most_common(1)[0][0]

        most_common_genre = 'N/A'
        if genre_counter:
            most_common_genre = genre_counter.most_common(1)[0][0]

        scene_counts = {}
        for scene in sorted(scene_counter):
            scene_counts[scene] = scene_counter[scene]

        return {
            'total_songs': len(self.songs),
            'genre_count': len(genre_counter),
            'language_count': len(language_counter),
            'most_common_mood': most_common_mood,
            'most_common_genre': most_common_genre,
            'high_energy_songs': high_energy_songs,
            'scene_counts': scene_counts,
        }

    def save_liked_song(self, song):
        self.load_liked_songs()

        for liked_song in self.liked_songs:
            same_title = liked_song.title.lower() == song.title.lower()
            same_artist = liked_song.artist.lower() == song.artist.lower()

            if same_title and same_artist:
                return False

        with open(self.liked_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(song.to_list())

        self.load_liked_songs()
        return True

    def add_song_to_library(self, song):
        for old_song in self.songs:
            same_title = old_song.title.lower() == song.title.lower()
            same_artist = old_song.artist.lower() == song.artist.lower()

            if same_title and same_artist:
                return False

        with open(self.library_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(song.to_list())

        self.load_songs()
        return True

    def get_liked_songs(self):
        self.load_liked_songs()
        return self.liked_songs
