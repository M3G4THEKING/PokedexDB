import os
import json

def check_setup():
    required_files = [
        'index.html',
        'css/styles.css',
        'js/search.js',
        'data/pokemon.json',
        'data/pokemon.csv'
    ]
    
    required_dirs = [
        'css',
        'js',
        'data',
        'templates',
        'pokemon_pages',
        'categories'
    ]
    
    print("Checking directory structure...")
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Found directory: {directory}")
        else:
            print(f"✗ Missing directory: {directory}")
            
    print("\nChecking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ Found file: {file}")
        else:
            print(f"✗ Missing file: {file}")
    
    if os.path.exists('data/pokemon.json'):
        try:
            with open('data/pokemon.json', 'r') as f:
                data = json.load(f)
                print(f"\n✓ Pokemon data loaded successfully with {len(data)} entries")
        except json.JSONDecodeError:
            print("\n✗ Error reading pokemon.json file")

if __name__ == "__main__":
    check_setup() 