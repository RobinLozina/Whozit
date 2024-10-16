# game_logic.py
from .models import Game, Character
import os
from django.conf import settings

def initialize_game(room_code, selected_folder):
    """
    Initialize the game with characters from the selected folder.
    """
    character_path = os.path.join(settings.MEDIA_ROOT, 'characters', selected_folder)
    
    # Fetch character images from the selected folder
    character_files = [
        f for f in os.listdir(character_path)
        if os.path.isfile(os.path.join(character_path, f))
    ]

    # Get or create the Game instance
    game, created = Game.objects.get_or_create(room_code=room_code, defaults={'selected_folder': selected_folder})
    
    # Create Character instances for each character in the folder
    Character.objects.filter(game=game).delete()  # Clear any existing characters for this game
    for file_name in character_files:
        Character.objects.create(
            game=game,  # Associate each character with the game
            name=os.path.splitext(file_name)[0],
            image=f'characters/{selected_folder}/{file_name}'
        )

    # Return the game data, including the list of characters
    characters = [
        {'name': os.path.splitext(f)[0], 'image_url': f'/media/characters/{selected_folder}/{f}'}
        for f in character_files
    ]

    return {
        'room_code': room_code,
        'characters': characters
    }
