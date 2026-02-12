const API_URL = 'http://localhost:8000/products/search/';

// Allow search on Enter key press
document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchProducts();
    }
});

async function searchProducts() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) return;

    const resultsContainer = document.getElementById('results');
    const loadingIndicator = document.getElementById('loading');

    // Clear previous state
    resultsContainer.innerHTML = '';
    loadingIndicator.classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}?q=${encodeURIComponent(query)}`);
        const products = await response.json();

        loadingIndicator.classList.add('hidden');

        if (products.length === 0) {
            resultsContainer.innerHTML = `
                <div class="col-span-full text-center text-gray-500 py-8">
                    No similar products found. Try a different description.
                </div>`;
            return;
        }

        products.forEach(product => {
            resultsContainer.appendChild(createProductCard(product));
        });

    } catch (error) {
        console.error('Error:', error);
        loadingIndicator.classList.add('hidden');
        resultsContainer.innerHTML = `<div class="text-red-500 text-center col-span-full">Error connecting to the API. Verify the server is running and CORS is configured.</div>`;
    }
}

function createProductCard(product) {
    // Calculate similarity (assuming distance comes from CosineDistance where 0 is identical)
    // Convert distance to approximate similarity percentage
    const similarity = product.distance !== undefined 
        ? Math.max(0, (1 - product.distance) * 100).toFixed(1) 
        : null;

    const card = document.createElement('div');
    card.className = 'bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden border border-gray-100 flex flex-col';
    
    card.innerHTML = `
        <div class="p-6 flex-1">
            <div class="flex justify-between items-start mb-2">
                <span class="text-xs font-bold uppercase tracking-wider text-indigo-500">${product.category || 'General'}</span>
                ${similarity ? `<span class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">Match: ${similarity}%</span>` : ''}
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2 leading-tight">${product.title}</h3>
            <p class="text-gray-600 text-sm mb-4 line-clamp-3">${product.description || 'No description available.'}</p>
        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
            <span class="text-2xl font-bold text-gray-800">$${product.price ? product.price.toFixed(2) : 'N/A'}</span>
            <button class="text-indigo-600 hover:text-indigo-800 font-medium text-sm">View details &rarr;</button>
        </div>
    `;

    return card;
}