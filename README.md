# MoodTune: A Personal Music Mood Recommender
==========================================

Project description
-------------------
MoodTune is a terminal-based Python music recommender designed for students and music lovers. It helps users pick songs based on mood, genre, energy level, language, listening scene, and optional tempo. The project runs fully offline, uses a local CSV song library, and is suitable for a short classroom demonstration.

Main features
-------------
1. Song recommendation
   - Recommends one song using a scoring system based on mood, genre, energy, language, scene, tempo, popularity, and liked artists.

2. Playlist generation
   - Creates a ranked playlist and presents the first five songs as a MoodTune playlist flow:
     warm-up track, main mood match, energy boost, popular pick, and calm ending.

3. Music mood quiz
   - Asks 4 quick questions and builds a suggested profile before recommending a song.

4. Library statistics
   - Shows total songs, number of genres, number of languages, most common mood, most common genre, high-energy song count, and scene counts.

5. Liked songs
   - Saves recommended songs to liked_songs.csv and gives bonus points to artists the user liked before.

6. Add a new song
   - Lets the user add a new song with scene, tempo, popularity, danceability, and valence values.

Advanced Python concepts used
-----------------------------
1. Object-oriented programming
   - The project uses a Song class and a MusicRecommender class.

2. CSV file handling
   - The program reads from song_library.csv and liked_songs.csv and writes updates back to CSV files.

3. Scoring and data processing
   - Each song is scored using multiple matching rules and readable reasons are stored for display.

4. Dictionaries and collections
   - The project uses dictionaries and Counter from the built-in collections module for quiz mapping and library statistics.

5. Input validation and exception handling
   - The program safely handles invalid menu choices, invalid numbers, missing files, and missing optional CSV columns.

How to run the program
----------------------
1. Keep all project files in the same folder.
2. Open a terminal in the project folder.
3. Run:

   python3 main.py

4. Follow the menu options in the terminal.

File structure
--------------
main.py
- Main program file.
- Handles menus, user input, quiz questions, and display formatting.

song.py
- Defines the Song class.
- Stores title, artist, genre, mood, energy, language, scene, popularity, tempo, danceability, and valence.

recommender.py
- Defines the MusicRecommender class.
- Handles CSV loading, scoring, recommendation, playlist generation, statistics, liked-song saving, and adding songs.

song_library.csv
- Local music library used by the program.
- The project does not need internet access or any external API.

liked_songs.csv
- Stores the user's saved songs.
- The file is updated when the user likes a recommendation.

Offline note
------------
MoodTune works fully offline. It does not use Spotify, Last.fm, or any other internet service. All recommendations come from the local CSV library.

Presentation idea
-----------------
A simple demo flow for a 3-minute presentation is:
1. Show the main menu.
2. Run a single recommendation with mood, genre, scene, and tempo.
3. Run the music mood quiz.
4. Show the playlist flow.
5. Open library statistics to show the 200-song dataset.
