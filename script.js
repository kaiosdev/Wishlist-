/**
 * 🎯 WISHLIST - JavaScript Application
 * Gerencia a renderização de produtos e alternância de visualização
 */

// ========================================
// 🔧 CONFIGURAÇÕES E ESTADO
// ========================================

const STATE = {
    products: [],
    viewMode: 'grid', // 'grid' ou 'list'
    isLoading: true
};

// Elementos do DOM
const DOM = {
    productsContainer: document.getElementById('productsContainer'),
    viewToggle: document.getElementById('viewToggle'),
    productCount: document.getElementById('productCount'),
    lastUpdate: document.getElementById('lastUpdate'),
    loading: document.getElementById('loading'),
    emptyState: document.getElementById('emptyState'),
    toggleText: document.querySelector('.toggle-text'),
    gridIcon: document.querySelector('.grid-icon'),
    listIcon: document.querySelector('.list-icon')
};

// ========================================
// 🎨 FUNÇÕES DE RENDERIZAÇÃO
// ========================================

/**
 * Trunca texto para um número máximo de caracteres
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Extrai o nome da loja de forma mais amigável
 */
function formatStoreName(domain) {
    // Remove 'www.' e extensões comuns
    let name = domain.replace(/^www\./, '').split('.')[0];
    
    // Capitaliza primeira letra
    name = name.charAt(0).toUpperCase() + name.slice(1);
    
    // Nomes especiais conhecidos
    const storeNames = {
        'amazon': 'Amazon',
        'mercadolivre': 'Mercado Livre',
        'magazineluiza': 'Magalu',
        'kabum': 'KaBuM!',
        'shopee': 'Shopee',
        'aliexpress': 'AliExpress',
        'americanas': 'Americanas',
        'casasbahia': 'Casas Bahia'
    };
    
    return storeNames[name.toLowerCase()] || name;
}

/**
 * Formata data para exibição
 */
function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Hoje';
        if (diffDays === 1) return 'Ontem';
        if (diffDays < 7) return `${diffDays} dias atrás`;
        
        return date.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    } catch (e) {
        return 'Data desconhecida';
    }
}

/**
 * Cria o HTML de um card de produto
 */
function createProductCard(product) {
    const storeName = formatStoreName(product.store);
    const titleTruncated = truncateText(product.title, 80);
    
    return `
        <article class="product-card" role="listitem">
            <div class="product-image-container">
                <img 
                    src="${product.image}" 
                    alt="${product.title}"
                    class="product-image"
                    loading="lazy"
                    onerror="this.src='https://via.placeholder.com/400x400/1a1a2e/eee?text=Imagem+Indispon%C3%ADvel'"
                >
                <span class="product-store-badge">${storeName}</span>
            </div>
            
            <div class="product-content">
                <h2 class="product-title" title="${product.title}">
                    ${titleTruncated}
                </h2>
                
                <div class="product-price">
                    ${product.price}
                </div>
                
                <div class="product-actions">
                    <a 
                        href="${product.url}" 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        class="btn btn-primary"
                        aria-label="Ver produto em ${storeName}"
                    >
                        <span>🛒</span>
                        <span>Ver na Loja</span>
                    </a>
                </div>
            </div>
        </article>
    `;
}

/**
 * Renderiza todos os produtos na tela
 */
function renderProducts() {
    // Remove loading
    DOM.loading.style.display = 'none';
    
    // Verifica se há produtos
    if (STATE.products.length === 0) {
        DOM.emptyState.style.display = 'flex';
        DOM.productsContainer.innerHTML = '';
        return;
    }
    
    // Esconde empty state
    DOM.emptyState.style.display = 'none';
    
    // Renderiza produtos
    const productsHTML = STATE.products
        .map(product => createProductCard(product))
        .join('');
    
    DOM.productsContainer.innerHTML = productsHTML;
    
    // Adiciona animação com delay escalonado
    const cards = document.querySelectorAll('.product-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
}

/**
 * Atualiza estatísticas na tela
 */
function updateStats(lastUpdated) {
    DOM.productCount.textContent = STATE.products.length;
    DOM.lastUpdate.textContent = formatDate(lastUpdated);
}

// ========================================
// 🔄 ALTERNÂNCIA DE VISUALIZAÇÃO
// ========================================

/**
 * Alterna entre grid view e list view
 */
function toggleView() {
    // Alterna o modo
    STATE.viewMode = STATE.viewMode === 'grid' ? 'list' : 'grid';
    
    // Atualiza classe do container
    if (STATE.viewMode === 'list') {
        DOM.productsContainer.classList.remove('grid-view');
        DOM.productsContainer.classList.add('list-view');
        DOM.toggleText.textContent = 'Modo Grade';
        DOM.gridIcon.style.display = 'none';
        DOM.listIcon.style.display = 'inline';
    } else {
        DOM.productsContainer.classList.remove('list-view');
        DOM.productsContainer.classList.add('grid-view');
        DOM.toggleText.textContent = 'Modo Lista';
        DOM.gridIcon.style.display = 'inline';
        DOM.listIcon.style.display = 'none';
    }
    
    // Salva preferência no localStorage
    try {
        localStorage.setItem('wishlist-view-mode', STATE.viewMode);
    } catch (e) {
        console.warn('localStorage não disponível');
    }
    
    // Adiciona animação de transição
    DOM.productsContainer.style.opacity = '0.7';
    setTimeout(() => {
        DOM.productsContainer.style.opacity = '1';
    }, 150);
}

/**
 * Restaura preferência de visualização salva
 */
function restoreViewPreference() {
    try {
        const savedView = localStorage.getItem('wishlist-view-mode');
        if (savedView === 'list') {
            toggleView();
        }
    } catch (e) {
        // localStorage não disponível, mantém padrão
    }
}

// ========================================
// 📡 CARREGAMENTO DE DADOS
// ========================================

/**
 * Carrega dados do arquivo JSON
 */
async function loadData() {
    try {
        console.log('🔄 Carregando dados...');
        
        // Adiciona timestamp para evitar cache
        const timestamp = new Date().getTime();
        const response = await fetch(`data.json?t=${timestamp}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Atualiza estado
        STATE.products = data.products || [];
        STATE.isLoading = false;
        
        // Renderiza produtos
        renderProducts();
        
        // Atualiza estatísticas
        updateStats(data.last_updated);
        
        console.log(`✅ ${STATE.products.length} produtos carregados`);
        
    } catch (error) {
        console.error('❌ Erro ao carregar dados:', error);
        
        STATE.isLoading = false;
        DOM.loading.innerHTML = `
            <div style="text-align: center; color: var(--accent-danger);">
                <p>⚠️ Erro ao carregar produtos</p>
                <p style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.5rem;">
                    ${error.message}
                </p>
                <button 
                    onclick="location.reload()" 
                    class="btn btn-primary" 
                    style="margin-top: 1rem; max-width: 200px;"
                >
                    Tentar Novamente
                </button>
            </div>
        `;
    }
}

// ========================================
// 🚀 INICIALIZAÇÃO
// ========================================

/**
 * Inicializa a aplicação
 */
function init() {
    console.log('🎁 Iniciando Wishlist App...');
    
    // Event Listeners
    DOM.viewToggle.addEventListener('click', toggleView);
    
    // Restaura preferência de visualização
    restoreViewPreference();
    
    // Carrega dados
    loadData();
    
    // Auto-refresh a cada 5 minutos (se a página estiver ativa)
    setInterval(() => {
        if (document.visibilityState === 'visible') {
            console.log('🔄 Auto-refresh...');
            loadData();
        }
    }, 5 * 60 * 1000);
}

// ========================================
// 🎬 EXECUÇÃO
// ========================================

// Aguarda o DOM estar pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ========================================
// 🔍 FUNCIONALIDADES EXTRAS (OPCIONAL)
// ========================================

/**
 * Adiciona suporte para teclas de atalho
 */
document.addEventListener('keydown', (e) => {
    // Tecla 'V' para alternar visualização
    if (e.key === 'v' || e.key === 'V') {
        if (!e.ctrlKey && !e.metaKey && !e.altKey) {
            toggleView();
        }
    }
    
    // Tecla 'R' para recarregar dados
    if (e.key === 'r' || e.key === 'R') {
        if (!e.ctrlKey && !e.metaKey && !e.altKey) {
            loadData();
        }
    }
});

/**
 * Log de informações úteis no console
 */
console.log(`
╔═══════════════════════════════════════╗
║   🎁 WISHLIST SERVERLESS APP         ║
║   Desenvolvido com ❤️                 ║
╠═══════════════════════════════════════╣
║  Atalhos:                             ║
║  • V: Alternar Grid/Lista             ║
║  • R: Recarregar Dados                ║
╚═══════════════════════════════════════╝
`);
