document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const pokemonGrid = document.getElementById('pokemonGrid');
    
    if (searchInput && pokemonGrid) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const pokemonCards = pokemonGrid.querySelectorAll('.pokemon-card');

            pokemonCards.forEach(card => {
                const pokemonName = card.querySelector('.pokemon-name').textContent.toLowerCase();
                const pokemonNumber = card.querySelector('.pokemon-number').textContent.toLowerCase();
                const types = Array.from(card.querySelectorAll('.type-badge'))
                    .map(badge => badge.textContent.toLowerCase())
                    .filter(type => type !== 'nan');

                const matches = pokemonName.includes(searchTerm) || 
                              pokemonNumber.includes(searchTerm) ||
                              types.some(type => type.includes(searchTerm));

                card.style.display = matches ? 'block' : 'none';
            });
        });
    }
}); 