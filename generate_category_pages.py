import json
from jinja2 import Environment, FileSystemLoader
import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_pokemon_data():
    with open('data/pokemon.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_category_pages():
    # Create categories directory
    create_directory('categories')
    
    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader('templates'))
    category_template = env.get_template('category_template.html')
    
    # Load Pokemon data
    pokemon_list = load_pokemon_data()
    
    # Define all Pokemon types to ensure all category pages are created
    all_types = [
        'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
        'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
        'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
    ]
    
    # Generate page for each type
    for type_name in all_types:
        # Filter Pokemon of this type
        type_pokemon = [
            p for p in pokemon_list 
            if p['Primary Type'] == type_name or 
            (p['Secondary Type'] and p['Secondary Type'] == type_name)
        ]
        
        # Generate HTML content
        html_content = category_template.render(
            type_name=type_name,
            pokemon_list=type_pokemon
        )
        
        # Write the file
        file_name = f"categories/{type_name.lower()}.html"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated category page for {type_name}-type Pokemon with {len(type_pokemon)} Pokemon")

if __name__ == "__main__":
    generate_category_pages() 