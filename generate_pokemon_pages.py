import json
import os
from jinja2 import Environment, FileSystemLoader
import shutil

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_pokemon_data():
    with open('data/pokemon.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def setup_directories():
    directories = ['pokemon_pages', 'css', 'js', 'categories']
    for directory in directories:
        create_directory(directory)

def get_unique_pokemon(pokemon_list):
    seen = set()
    unique_pokemon = []
    
    for pokemon in pokemon_list:
        pokedex_num = pokemon['Pokedex Number']
        if pokedex_num not in seen:
            seen.add(pokedex_num)
            # Find all forms of this Pokémon
            forms = [p for p in pokemon_list if p['Pokedex Number'] == pokedex_num]
            # Use the base form (one without alternate form name)
            base_form = next(
                (p for p in forms if not p['Alternate Form Name'] or str(p['Alternate Form Name']).lower() == 'nan'),
                forms[0]  # If no base form found, use the first form
            )
            unique_pokemon.append(base_form)
    
    return sorted(unique_pokemon, key=lambda x: int(str(x['Pokedex Number'])))

def get_pokemon_by_type(pokemon_list, type_name):
    type_pokemon = []
    seen = set()
    
    for pokemon in pokemon_list:
        pokedex_num = pokemon['Pokedex Number']
        primary_type = str(pokemon['Primary Type']).strip()
        secondary_type = str(pokemon['Secondary Type']).strip()
        
        is_type_match = (primary_type == type_name or 
                        (secondary_type and secondary_type != 'nan' and secondary_type == type_name))
        
        if is_type_match and pokedex_num not in seen:
            seen.add(pokedex_num)
            type_pokemon.append(pokemon)
    
    return sorted(type_pokemon, key=lambda x: int(str(x['Pokedex Number'])))

def get_base_url(template_type):
    """Get the correct base URL for different template types"""
    if template_type == 'index':
        return ''
    elif template_type in ['category', 'page', 'pokemon']:
        return '../'
    return ''

def get_site_url():
    """Get the site URL based on environment"""
    if os.environ.get('GITHUB_ACTIONS'):
        # If running in GitHub Actions, use the repository name as the base URL
        return '/pokedex'  # Replace 'pokedex' with your repository name
    return ''

def render_template(template_name, **kwargs):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    
    # Add site_url to kwargs
    site_url = get_site_url()
    kwargs['site_url'] = site_url
    
    # Update base_url to include site_url
    if 'base_url' not in kwargs:
        if template_name.startswith(('pages/', 'categories/', 'pokemon_pages/')):
            kwargs['base_url'] = f'{site_url}/../'
        else:
            kwargs['base_url'] = f'{site_url}/'
    
    # Add header and footer templates
    env.globals['header'] = env.get_template('header.html')
    env.globals['footer'] = env.get_template('footer.html')
    
    return template.render(**kwargs)

def clean_pokemon_data(pokemon):
    # Clean up type data
    if 'Secondary Type' in pokemon:
        if str(pokemon['Secondary Type']).lower() in ['nan', 'null', '', 'none']:
            pokemon['Secondary Type'] = None
    
    # Clean up numeric data
    stat_fields = ['Health Stat', 'Attack Stat', 'Defense Stat', 
                  'Special Attack Stat', 'Special Defense Stat', 'Speed Stat']
    for field in stat_fields:
        try:
            pokemon[field] = float(pokemon[field])
        except (ValueError, TypeError):
            pokemon[field] = 0
    
    return pokemon

def generate_pages():
    setup_directories()
    
    try:
        # Load and clean Pokemon data
        pokemon_list = load_pokemon_data()
        pokemon_list = [clean_pokemon_data(p) for p in pokemon_list]
        
        # Generate index page
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(render_template('index_template.html', 
                pokemon_list=pokemon_list,
                base_url=''
            ))
        
        # Generate category pages
        for type_name in get_all_types(pokemon_list):
            type_pokemon = get_pokemon_by_type(pokemon_list, type_name)
            with open(f'categories/{type_name.lower()}.html', 'w', encoding='utf-8') as f:
                f.write(render_template('category_template.html', 
                    pokemon_list=type_pokemon,
                    type_name=type_name,
                    base_url='../'
                ))
        
        # Generate Pokemon pages
        for pokemon in pokemon_list:
            clean_name = clean_pokemon_name(pokemon['Pokemon Name'])
            with open(f'pokemon_pages/{pokemon["Pokedex Number"]}_{clean_name}.html', 'w', encoding='utf-8') as f:
                f.write(render_template('pokemon_template.html',
                    pokemon=pokemon,
                    base_url='../'
                ))
        
        # Generate other pages
        for page in ['about', 'contact', 'disclaimer']:
            with open(f'pages/{page}.html', 'w', encoding='utf-8') as f:
                f.write(render_template(f'{page}.html', base_url='../'))
                
    except Exception as e:
        print(f"Error generating pages: {str(e)}")

if __name__ == "__main__":
    try:
        generate_pages()
        print("Successfully generated all pages!")
    except Exception as e:
        print(f"Error occurred: {str(e)}") 