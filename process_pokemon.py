import pandas as pd
import json
import os

def ensure_directories():
    directories = ['data', 'css', 'js', 'templates', 'pokemon_pages', 'categories']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def process_pokemon_data():
    # Read the CSV file
    df = pd.read_csv('data/pokemon.csv')
    
    # Clean the data by removing quotes and extra whitespace
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].str.strip().str.strip('"')
    
    # Convert to dictionary format for JSON
    pokemon_list = df.to_dict('records')
    
    # Save as JSON file for easier web usage
    with open('data/pokemon.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_list, f, ensure_ascii=False, indent=2)
    
    # Print some basic statistics
    print(f"Total number of Pokémon entries: {len(df)}")
    print("\nType distribution:")
    print(df['Primary Type'].value_counts())
    
    print("\nLegendary Pokémon count:")
    legendary_count = df['Legendary Type'].notna().sum()
    print(f"Number of Legendary Pokémon: {legendary_count}")
    
    print("\nStats Summary:")
    stats_columns = ['Health Stat', 'Attack Stat', 'Defense Stat', 
                    'Special Attack Stat', 'Special Defense Stat', 'Speed Stat']
    print(df[stats_columns].describe())

def get_pokemon_by_type(type_name):
    df = pd.read_csv('data/pokemon.csv')
    type_filter = (df['Primary Type'].str.contains(type_name, na=False) | 
                  df['Secondary Type'].str.contains(type_name, na=False))
    return df[type_filter]

def get_pokemon_by_name(name):
    df = pd.read_csv('data/pokemon.csv')
    return df[df['Pokemon Name'].str.contains(name, na=False, case=False)]

def get_strongest_pokemon(stat_type, n=10):
    df = pd.read_csv('data/pokemon.csv')
    return df.nlargest(n, stat_type)[['Pokemon Name', stat_type]]

if __name__ == "__main__":
    try:
        ensure_directories()
        process_pokemon_data()
        print("Data processing completed successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}") 