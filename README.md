# MoodTune: A Personal Music Mood Recommender

MoodTune is a terminal-based Python program created for the COMP9001 Python Project Challenge. It recommends songs based on the user's mood, preferred genre, energy level, language, listening scene, and tempo preference.

## Project Description

Many students listen to music while studying, relaxing, walking, travelling, or working out, but sometimes it is hard to decide what to play. MoodTune helps users find songs that match their current mood and situation.

Instead of choosing songs randomly, the program uses a simple scoring system. It compares the user's preferences with each song's metadata and gives readable reasons for each recommendation.

The song library is stored in a local CSV file with 200 songs, so the program can run without internet connection or external APIs.

## Main Features

- Recommend songs based on mood, genre, energy, language, scene, and tempo
- Show a recommendation score and readable reasons
- Generate a playlist flow
- Take a short music mood quiz
- Save liked songs
- View liked songs
- Add new songs to the song library
- View library statistics
- Return to the main menu during input by typing `/menu`

## Python Concepts Used

This project uses several Python concepts from COMP9001:

- Functions
- Lists and dictionaries
- Object-oriented programming
- CSV file handling
- Exception handling
- Menu-based user interaction

## How to Run

Keep all project files in the same folder, then run:

```bash
python3 main.py
