'''
MoodTune: A Personal Music Mood Recommender

This is the main file of the program.
It controls the menu, user input, and what feature will run.

Other files:
- recommender.py: recommendation logic and CSV handling
- song.py: Song class
'''

from pathlib import Path

from recommender import MusicRecommender
from song import Song


class ReturnToMenu(Exception):
    '''Raised when the user wants to return to the main menu.'''


# File paths. This makes the program work even when it is run from another folder.
BASE_DIR = Path(__file__).resolve().parent
LIBRARY_FILE = BASE_DIR / 'song_library.csv'
LIKED_FILE = BASE_DIR / 'liked_songs.csv'
MENU_COMMAND = '/menu'

# These lists are used if the CSV file does not provide enough options.
DEFAULT_MOODS = ['chill', 'emotional', 'energetic', 'happy', 'hopeful', 'romantic', 'sad']
DEFAULT_GENRES = [
    'C-pop', 'Electronic', 'Hip-hop', 'Indie', 'J-pop', 'Jazz', 'K-pop',
    'Latin', 'Lo-fi', 'Pop', 'R&B', 'Rock', 'Soundtrack'
]
DEFAULT_ENERGIES = ['high', 'low', 'medium']
DEFAULT_LANGUAGES = ['Chinese', 'English', 'Japanese', 'Korean', 'Spanish']
DEFAULT_SCENES = ['study', 'walking', 'travel', 'workout', 'relaxing', 'party', 'sleep', 'commute']
DEFAULT_TEMPOS = ['fast', 'medium', 'slow']


def print_line(char='=', width=72):
    print(char * width)


def print_section(title):
    print()
    print_line()
    print(title)
    print_line()


def get_user_input(prompt):
    # This helper lets /menu work anywhere in the program.
    user_input = input(prompt).strip()

    if user_input.lower() == MENU_COMMAND:
        raise ReturnToMenu

    return user_input


def get_menu_choice():
    print_section('MoodTune: A Personal Music Mood Recommender')
    print('Find a soundtrack for your mood, scene, and energy in a few steps.')
    print(f"Type {MENU_COMMAND} anytime to return to the main menu.")
    print()
    print('1. Get a song recommendation')
    print('2. Generate a playlist')
    print('3. Take a music mood quiz')
    print('4. View library statistics')
    print('5. View liked songs')
    print('6. Add a new song to the library')
    print('7. Exit')
    print_line('-')

    return get_user_input('Choose an option (1-7): ')


def choose_from_options(title, options):
    # This function is reused for mood, genre, energy, quiz answers, etc.
    while True:
        print_section(title)
        print(f"Type {MENU_COMMAND} to return to the main menu.")

        for i, option in enumerate(options, start=1):
            print(f'{i}. {option}')

        choice = get_user_input(f'Choose an option (1-{len(options)}): ')

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]
            print('Please choose a number from the list.')
        except ValueError:
            print('Invalid input. Please enter a number.')


def choose_optional_from_options(title, options, skip_text='Skip this preference'):
    choice = choose_from_options(title, [skip_text] + options)

    if choice == skip_text:
        return ''

    return choice


def get_options(recommender, attribute, fallback_options):
    # Try to get real options from the CSV first.
    # If there is no data, use the default list above.
    options = recommender.get_available_values(attribute)

    if options:
        return options

    return list(fallback_options)


def format_reasons(reasons):
    if reasons:
        return ', '.join(reasons)

    return 'closest available match'


def show_preference_summary(preferences, title):
    print_section(title)
    print(f"Mood:      {preferences.get('mood') or 'Any'}")
    print(f"Genre:     {preferences.get('genre') or 'Any'}")
    print(f"Energy:    {preferences.get('energy') or 'Any'}")
    print(f"Language:  {preferences.get('language') or 'Any'}")
    print(f"Scene:     {preferences.get('scene') or 'Any'}")
    print(f"Tempo:     {preferences.get('tempo') or 'Any'}")


def ask_user_preferences(recommender):
    # Get all possible choices from the current library.
    moods = get_options(recommender, 'mood', DEFAULT_MOODS)
    genres = get_options(recommender, 'genre', DEFAULT_GENRES)
    energies = get_options(recommender, 'energy', DEFAULT_ENERGIES)
    languages = get_options(recommender, 'language', DEFAULT_LANGUAGES)
    scenes = get_options(recommender, 'scene', DEFAULT_SCENES)
    tempos = get_options(recommender, 'tempo', DEFAULT_TEMPOS)

    mood = choose_from_options('How are you feeling today?', moods)
    genre = choose_from_options('What genre do you prefer?', genres)
    energy = choose_from_options('What energy level do you want?', energies)
    language = choose_from_options('What language do you prefer?', languages)
    scene = choose_from_options('What are you doing now?', scenes)
    tempo = choose_optional_from_options('Choose a tempo if you want one:', tempos)

    return {
        'mood': mood,
        'genre': genre,
        'energy': energy,
        'language': language,
        'scene': scene,
        'tempo': tempo,
    }


def display_recommendation(song, score, reasons, title='Recommended song'):
    print_section(title)
    print(f'Title:      {song.title}')
    print(f'Artist:     {song.artist}')
    print(f'Genre:      {song.genre}')
    print(f'Mood:       {song.mood}')
    print(f'Energy:     {song.energy}')
    print(f'Language:   {song.language}')
    print(f"Scene:      {song.scene or 'Unknown'}")
    print(f"Tempo:      {song.tempo or 'Unknown'}")
    print(f'Popularity: {song.popularity}')
    print(f'Score:      {score}')
    print(f'Reason:     {format_reasons(reasons)}')


def ask_yes_no(question):
    while True:
        answer = get_user_input(question).lower()

        if answer in ['yes', 'y']:
            return True
        if answer in ['no', 'n']:
            return False

        print('Please answer yes or no.')


def offer_to_save_song(recommender, song):
    if ask_yes_no('Do you want to save this song to liked songs? (yes/no): '):
        saved = recommender.save_liked_song(song)

        if saved:
            print('This song has been saved to liked_songs.csv.')
        else:
            print('This song is already in your liked songs.')


def get_song_recommendation(recommender):
    preferences = ask_user_preferences(recommender)
    show_preference_summary(preferences, 'Your MoodTune profile')

    song, score, reasons = recommender.recommend_song(**preferences)

    if song is None:
        print('No songs are available in the library.')
        return

    display_recommendation(song, score, reasons)
    offer_to_save_song(recommender, song)


def get_positive_number(prompt):
    while True:
        value = get_user_input(prompt)

        try:
            number = int(value)
            if number > 0:
                return number
            print('Please enter a number greater than 0.')
        except ValueError:
            print('Invalid input. Please enter a whole number.')


def display_playlist_flow(recommender, playlist):
    flow_items, extra_items = recommender.build_playlist_flow(playlist)

    print_section('Your MoodTune Playlist Flow')

    for i, item in enumerate(flow_items, start=1):
        label, song, score, reasons = item

        print(f'{i}. {label}')
        print(f'   Title:  {song.title}')
        print(f'   Artist: {song.artist}')
        print(f'   Genre:  {song.genre}')
        print(f'   Mood:   {song.mood}')
        print(f'   Score:  {score}')
        print(f'   Reason: {format_reasons(reasons)}')
        print_line('-')

    if extra_items:
        print('Extra recommendations:')

        for i, item in enumerate(extra_items, start=len(flow_items) + 1):
            song, score, reasons = item
            print(f'{i}. {song.title} - {song.artist} | {song.genre} | {song.mood}')
            print(f'   Score: {score} | Reason: {format_reasons(reasons)}')


def generate_playlist(recommender):
    preferences = ask_user_preferences(recommender)
    show_preference_summary(preferences, 'Playlist profile')

    playlist_size = get_positive_number('How many songs do you want in the playlist? ')
    playlist = recommender.generate_playlist(playlist_size=playlist_size, **preferences)

    if not playlist:
        print('No songs are available in the library.')
        return

    display_playlist_flow(recommender, playlist)


def view_liked_songs(recommender):
    liked_songs = recommender.get_liked_songs()

    print_section('Your liked songs')

    if not liked_songs:
        print('You have not saved any liked songs yet.')
        return

    for i, song in enumerate(liked_songs, start=1):
        print(f'{i}. {song.display()}')


def get_number_input(prompt, default, minimum=0, maximum=100):
    while True:
        value = get_user_input(prompt)

        # Pressing Enter means using the default value.
        if value == '':
            return default

        try:
            number = int(float(value))
            if minimum <= number <= maximum:
                return number
            print(f'Please enter a number from {minimum} to {maximum}.')
        except ValueError:
            print('Invalid input. Please enter a number.')


def add_new_song(recommender):
    print_section('Add a new song to the library')
    print(f"Type {MENU_COMMAND} anytime to return to the main menu.")

    title = get_user_input('Song title: ')
    artist = get_user_input('Artist: ')

    if not title or not artist:
        print('Title and artist cannot be empty.')
        return

    genre = choose_from_options('Choose the song genre:', get_options(recommender, 'genre', DEFAULT_GENRES))
    mood = choose_from_options('Choose the song mood:', get_options(recommender, 'mood', DEFAULT_MOODS))
    energy = choose_from_options('Choose the song energy level:', get_options(recommender, 'energy', DEFAULT_ENERGIES))
    language = choose_from_options('Choose the song language:', get_options(recommender, 'language', DEFAULT_LANGUAGES))
    scene = choose_from_options('Choose the listening scene:', get_options(recommender, 'scene', DEFAULT_SCENES))
    tempo = choose_from_options('Choose the tempo:', get_options(recommender, 'tempo', DEFAULT_TEMPOS))

    popularity = get_number_input('Popularity (0-100, press Enter for 50): ', 50)
    danceability = get_number_input('Danceability (0-100, press Enter for 50): ', 50)
    valence = get_number_input('Valence (0-100, press Enter for 50): ', 50)

    new_song = Song(
        title,
        artist,
        genre,
        mood,
        energy,
        language,
        scene,
        popularity,
        tempo,
        danceability,
        valence,
    )

    added = recommender.add_song_to_library(new_song)

    if added:
        print('The new song has been added to song_library.csv.')
    else:
        print('This song already exists in the library.')


def choose_best_option(score_table, ordered_options):
    # Return the option with the highest score.
    best_option = ordered_options[0]
    best_score = -1

    for option in ordered_options:
        score = score_table.get(option, 0)

        if score > best_score:
            best_option = option
            best_score = score

    return best_option


def build_quiz_profile(recommender, day_answer, goal_answer, scene_answer, pace_answer):
    # The quiz turns simple answers into mood, energy, scene and tempo.
    mood_options = get_options(recommender, 'mood', DEFAULT_MOODS)
    energy_options = get_options(recommender, 'energy', DEFAULT_ENERGIES)

    mood_scores = {mood: 0 for mood in mood_options}
    energy_scores = {energy: 0 for energy in energy_options}

    if day_answer == 'Busy':
        mood_scores['chill'] = mood_scores.get('chill', 0) + 2
        mood_scores['hopeful'] = mood_scores.get('hopeful', 0) + 1
        energy_scores['medium'] = energy_scores.get('medium', 0) + 2
    elif day_answer == 'Relaxed':
        mood_scores['chill'] = mood_scores.get('chill', 0) + 2
        mood_scores['romantic'] = mood_scores.get('romantic', 0) + 1
        energy_scores['low'] = energy_scores.get('low', 0) + 2
    elif day_answer == 'Emotional':
        mood_scores['emotional'] = mood_scores.get('emotional', 0) + 3
        mood_scores['sad'] = mood_scores.get('sad', 0) + 1
        energy_scores['low'] = energy_scores.get('low', 0) + 1
    elif day_answer == 'Exciting':
        mood_scores['energetic'] = mood_scores.get('energetic', 0) + 2
        mood_scores['happy'] = mood_scores.get('happy', 0) + 1
        energy_scores['high'] = energy_scores.get('high', 0) + 2

    if goal_answer == 'Help me focus':
        mood_scores['chill'] = mood_scores.get('chill', 0) + 2
        mood_scores['hopeful'] = mood_scores.get('hopeful', 0) + 1
        energy_scores['low'] = energy_scores.get('low', 0) + 1
        energy_scores['medium'] = energy_scores.get('medium', 0) + 1
    elif goal_answer == 'Cheer me up':
        mood_scores['happy'] = mood_scores.get('happy', 0) + 3
        mood_scores['hopeful'] = mood_scores.get('hopeful', 0) + 1
        energy_scores['medium'] = energy_scores.get('medium', 0) + 1
        energy_scores['high'] = energy_scores.get('high', 0) + 1
    elif goal_answer == 'Calm me down':
        mood_scores['chill'] = mood_scores.get('chill', 0) + 2
        mood_scores['emotional'] = mood_scores.get('emotional', 0) + 1
        energy_scores['low'] = energy_scores.get('low', 0) + 2
    elif goal_answer == 'Give me energy':
        mood_scores['energetic'] = mood_scores.get('energetic', 0) + 3
        mood_scores['happy'] = mood_scores.get('happy', 0) + 1
        energy_scores['high'] = energy_scores.get('high', 0) + 2

    scene_map = {
        'Studying': 'study',
        'Walking': 'walking',
        'Travelling': 'travel',
        'Working out': 'workout',
        'Relaxing': 'relaxing',
    }
    scene = scene_map[scene_answer]

    if scene == 'study':
        mood_scores['chill'] = mood_scores.get('chill', 0) + 1
    elif scene == 'walking':
        mood_scores['happy'] = mood_scores.get('happy', 0) + 1
    elif scene == 'travel':
        mood_scores['hopeful'] = mood_scores.get('hopeful', 0) + 1
    elif scene == 'workout':
        mood_scores['energetic'] = mood_scores.get('energetic', 0) + 1
        energy_scores['high'] = energy_scores.get('high', 0) + 1
    elif scene == 'relaxing':
        mood_scores['chill'] = mood_scores.get('chill', 0) + 1
        energy_scores['low'] = energy_scores.get('low', 0) + 1

    tempo_map = {
        'Slow and steady': 'slow',
        'Balanced': 'medium',
        'Fully pumped': 'fast',
    }
    tempo = tempo_map[pace_answer]

    if tempo == 'slow':
        energy_scores['low'] = energy_scores.get('low', 0) + 1
    elif tempo == 'medium':
        energy_scores['medium'] = energy_scores.get('medium', 0) + 1
    elif tempo == 'fast':
        energy_scores['high'] = energy_scores.get('high', 0) + 1

    mood = choose_best_option(mood_scores, mood_options)
    energy = choose_best_option(energy_scores, energy_options)

    return {
        'mood': mood,
        'genre': '',
        'energy': energy,
        'language': '',
        'scene': scene,
        'tempo': tempo,
    }


def take_music_mood_quiz(recommender):
    print_section('MoodTune music mood quiz')

    day_answer = choose_from_options(
        'Q1. How was your day?',
        ['Busy', 'Relaxed', 'Emotional', 'Exciting'],
    )
    goal_answer = choose_from_options(
        'Q2. What do you want music to do for you?',
        ['Help me focus', 'Cheer me up', 'Calm me down', 'Give me energy'],
    )
    scene_answer = choose_from_options(
        'Q3. Where are you listening?',
        ['Studying', 'Walking', 'Travelling', 'Working out', 'Relaxing'],
    )
    pace_answer = choose_from_options(
        'Q4. Pick your music pace:',
        ['Slow and steady', 'Balanced', 'Fully pumped'],
    )

    quiz_profile = build_quiz_profile(recommender, day_answer, goal_answer, scene_answer, pace_answer)
    show_preference_summary(quiz_profile, 'Your quiz profile')

    song, score, reasons = recommender.recommend_song(**quiz_profile)

    if song is None:
        print('No songs are available in the library.')
        return

    display_recommendation(song, score, reasons, 'Quiz recommendation')
    offer_to_save_song(recommender, song)


def view_library_statistics(recommender):
    stats = recommender.get_library_statistics()

    print_section('Library statistics')
    print(f"Total number of songs: {stats['total_songs']}")
    print(f"Number of genres:      {stats['genre_count']}")
    print(f"Number of languages:   {stats['language_count']}")
    print(f"Most common mood:      {stats['most_common_mood']}")
    print(f"Most common genre:     {stats['most_common_genre']}")
    print(f"High energy songs:     {stats['high_energy_songs']}")
    print()
    print('Songs by scene:')

    if not stats['scene_counts']:
        print('No scene data is available.')
        return

    for scene, count in stats['scene_counts'].items():
        print(f'- {scene}: {count}')


def main():
    recommender = MusicRecommender(LIBRARY_FILE, LIKED_FILE)

    while True:
        try:
            choice = get_menu_choice()
        except ReturnToMenu:
            continue

        try:
            if choice == '1':
                get_song_recommendation(recommender)
            elif choice == '2':
                generate_playlist(recommender)
            elif choice == '3':
                take_music_mood_quiz(recommender)
            elif choice == '4':
                view_library_statistics(recommender)
            elif choice == '5':
                view_liked_songs(recommender)
            elif choice == '6':
                add_new_song(recommender)
            elif choice == '7':
                print('Thank you for using MoodTune. Goodbye!')
                break
            else:
                print('Invalid choice. Please choose a number from 1 to 7.')
        except ReturnToMenu:
            print('Returning to main menu...')


if __name__ == '__main__':
    main()
