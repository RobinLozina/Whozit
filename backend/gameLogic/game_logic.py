import os
import random
from .models import Game, Character
from django.conf import settings

def initialize_game(room_code, selected_folder):
    """
    Initialize the game with characters from the selected folder.
    Ensures that there are always 24 distinct characters.
    """
    character_path = os.path.join(settings.MEDIA_ROOT, 'characters', selected_folder)
    
    # Fetch character images from the selected folder
    character_files = [
        f for f in os.listdir(character_path)
        if os.path.isfile(os.path.join(character_path, f))
    ]

    # If there are fewer than 24 images, generate placeholder characters
    if len(character_files) < 24:
        existing_count = len(character_files)
        for i in range(existing_count, 24):
            # Generate unique placeholder names
            placeholder_name = f'Placeholder_{i + 1}'
            character_files.append(placeholder_name)
    
    # Shuffle to add randomness in case we have placeholders mixed in
    random.shuffle(character_files)
    character_files = character_files[:24]  # Ensure there are exactly 24 characters

    # Get or create the Game instance
    game, created = Game.objects.get_or_create(room_code=room_code, defaults={'selected_folder': selected_folder})
    
    # Clear any existing characters for this game and create new ones
    Character.objects.filter(game=game).delete()
    characters = []

    for file_name in character_files:
        if file_name.startswith('Placeholder_'):
            # Create a placeholder character object
            character_name = file_name
            character_image = None  # Placeholder doesn't have an image
            image_url = 'https://via.placeholder.com/100'  # Placeholder image (default URL or generated)
        else:
            # Create a character from the actual files
            character_name = os.path.splitext(file_name)[0]
            character_image = f'characters/{selected_folder}/{file_name}'
            image_url = f'http://127.0.0.1:8000{settings.MEDIA_URL}characters/{selected_folder}/{file_name}'

        # Create the Character instance in the database
        Character.objects.create(
            game=game,
            name=character_name,
            image=character_image if character_image else ""
        )

        # Append character data to the characters list
        characters.append({
            'name': character_name,
            'image_url': image_url
        })

    return {
        'room_code': room_code,
        'characters': characters
    }
