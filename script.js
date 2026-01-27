async function loadProducts() {
    try {
        // Adiciona timestamp para evitar cache do navegador
        const response = await fetch(`data.json?t=${new Date().getTime()}`);
        if (!response.ok) throw new Error("JSON não encontrado");
        
        const data = await response.json();
        document.getElementById('last-updated').textContent = `Atualizado: ${data.last_updated}`;
        
        const container = document.getElementById('products-container');
        if (data.products.length === 0) {
            container.innerHTML = '<p style="text-align:center; width:100%; color:#888;">Nenhum produto na lista ainda.</p>';
            return;
        }

        container.innerHTML = data.products.map(product => `
            <div class="card">
                <a href="${product.url}" target="_blank" class="card-link">
                    <img src="${product.image}" alt="${product.title}" loading="lazy" onerror="this.src='https://placehold.co/400?text=Sem+Imagem'">
                    <div class="info">
                        <span class="store-tag">${product.store}</span>
                        <h3>${product.title}</h3>
                        <span class="price">${product.price}</span>
                    </div>
                </a>
            </div>
        `).join('');
    } catch (error) {
        console.log("Erro:", error);
    }
}

function toggleView() {
    const container = document.getElementById('products-container');
    const icon = document.querySelector('#view-toggle i');
    container.classList.toggle('list-view');
    container.classList.toggle('grid-view');
    
    if (container.classList.contains('list-view')) {
        icon.className = 'fas fa-list';
    } else {
        icon.className = 'fas fa-th-large';
    }
}

function addProduct() {
    const url = document.getElementById('new-url').value.trim();
    if (!url) return alert("Cole um link primeiro!");

    // SEUS DADOS AQUI
    const user = "kaiosdev";
    const repo = "Wishlist-"; // Com o traço
    
    // Abre a issue automaticamente
    const link = `https://github.com/${user}/${repo}/issues/new?title=ADD_URL&body=${encodeURIComponent(url)}`;
    window.open(link, '_blank');
    document.getElementById('new-url').value = "";
}

loadProducts();