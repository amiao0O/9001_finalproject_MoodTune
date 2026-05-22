"""
song.py
This file defines the Song class used by the MoodTune project.
Each Song object stores one song's information.
"""


class Song:
    """A class to represent one song in the MoodTune library."""

    def __init__(
        self,
        title,
        artist,
        genre,
        mood,
        energy,
        language,
        scene="",
        popularity=50,
        tempo="",
        danceability=50,
        valence=50,
    ):
        self.title = self._clean_text(title)
        self.artist = self._clean_text(artist)
        self.genre = self._clean_text(genre)
        self.mood = self._clean_text(mood)
        self.energy = self._clean_text(energy)
        self.language = self._clean_text(language)
        self.scene = self._clean_text(scene, "")
        self.popularity = self._clean_number(popularity, 50)
        self.tempo = self._clean_text(tempo, "")
        self.danceability = self._clean_number(danceability, 50)
        self.valence = self._clean_number(valence, 50)

    def _clean_text(self, value, default="Unknown"):
        """Return a safe text value."""
        if value is None:
            return default

        text = str(value).strip()
        if text == "":
            return default
        return text

    def _clean_number(self, value, default):
        """Return a safe integer value for optional numeric fields."""
        try:
            return int(float(str(value).strip()))
        except (TypeError, ValueError):
            return default

    def to_list(self):
        """Return the song information as a list for writing to CSV."""
        return [
            self.title,
            self.artist,
            self.genre,
            self.mood,
            self.energy,
            self.language,
            self.scene,
            self.popularity,
            self.tempo,
            self.danceability,
            self.valence,
        ]

    def to_dict(self):
        """Return the song information as a dictionary."""
        return {
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "mood": self.mood,
            "energy": self.energy,
            "language": self.language,
            "scene": self.scene,
            "popularity": self.popularity,
            "tempo": self.tempo,
            "danceability": self.danceability,
            "valence": self.valence,
        }

    def display(self):
        """Return a user-friendly string for displaying the song."""
        details = [self.genre, self.mood, self.energy, self.language]

        if self.scene:
            details.append(self.scene)

        return f"{self.title} by {self.artist} ({', '.join(details)})"
