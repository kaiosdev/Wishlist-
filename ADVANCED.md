# 🔍 GUIA DE DEBUGGING E CUSTOMIZAÇÃO AVANÇADA

## 🛠️ Como Adicionar Suporte para Novas Lojas

Se o scraper não está conseguindo extrair dados de uma loja específica, siga este guia:

### Passo 1: Identificar Seletores CSS

1. Abra o produto no navegador
2. Pressione F12 para abrir DevTools
3. Clique na ferramenta "Selecionar Elemento" (ícone de cursor)
4. Clique no preço do produto

**Exemplo - Amazon:**
```html
<span class="a-price-whole">299<span class="a-price-decimal">,</span>90</span>
```
✅ Seletor: `.a-price-whole`

**Exemplo - Mercado Livre:**
```html
<span class="andes-money-amount__fraction">1.299</span>
```
✅ Seletor: `.andes-money-amount__fraction`

### Passo 2: Adicionar ao Script

Edite `scraper.py` na linha ~145:

```python
price_selectors = [
    # Sua nova loja aqui
    '.seu-seletor-de-preco',
    '#id-do-elemento-preco',
    '[data-testid="price"]',
    
    # Amazon
    '.a-price-whole',
    # ...resto dos seletores
]
```

### Passo 3: Testar

```bash
# Execute localmente (requer Python instalado)
python scraper.py
```

---

## 🧪 Testar Localmente (Opcional)

### Setup Local

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/minha-wishlist.git
cd minha-wishlist

# 2. Crie ambiente virtual Python
python -m venv venv

# 3. Ative o ambiente
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Execute o scraper
python scraper.py
```

### Testar o Frontend Localmente

```bash
# Opção 1: Python Simple Server
python -m http.server 8000

# Opção 2: Node.js (se tiver instalado)
npx serve .

# Acesse: http://localhost:8000
```

---

## 🎯 Customizações Avançadas

### 1. Adicionar Filtro de Preço Máximo

Edite `scraper.py`, adicione após linha 231:

```python
def filter_by_max_price(products, max_price_brl):
    """Filtra produtos acima de um preço máximo"""
    filtered = []
    for product in products:
        price_str = product['price']
        # Extrai números do preço
        numbers = re.findall(r'\d+', price_str.replace('.', '').replace(',', '.'))
        if numbers:
            price_float = float('.'.join(numbers))
            if price_float <= max_price_brl:
                filtered.append(product)
    return filtered

# Use na função main():
# products = filter_by_max_price(products, 500.00)  # Apenas produtos até R$ 500
```

### 2. Adicionar Notificação de Queda de Preço

Edite `scraper.py`, adicione:

```python
def check_price_drop(old_products, new_products):
    """Detecta quedas de preço"""
    alerts = []
    for new_prod in new_products:
        for old_prod in old_products:
            if new_prod['url'] == old_prod['url']:
                old_price = extract_price_number(old_prod['price'])
                new_price = extract_price_number(new_prod['price'])
                if new_price and old_price and new_price < old_price:
                    drop = old_price - new_price
                    percent = (drop / old_price) * 100
                    alerts.append(f"🔥 {new_prod['title'][:50]} caiu de R$ {old_price:.2f} para R$ {new_price:.2f} (-{percent:.1f}%)")
    return alerts

def extract_price_number(price_str):
    """Converte string de preço em float"""
    numbers = re.findall(r'\d+[,.]?\d*', price_str.replace('.', '').replace(',', '.'))
    return float(numbers[0]) if numbers else None
```

### 3. Adicionar Campo de Categoria

Edite `data.json`:

```json
{
  "products": [
    {
      "url": "...",
      "category": "Eletrônicos",  // ← Novo campo
      "priority": "alta"           // ← Novo campo
    }
  ]
}
```

Edite `script.js` para filtrar por categoria:

```javascript
function filterByCategory(category) {
    const filtered = STATE.products.filter(p => p.category === category);
    renderProducts(filtered);
}

// Adicione botões de filtro no HTML
```

### 4. Modo Light Theme

Adicione no final de `style.css`:

```css
/* Light Mode */
@media (prefers-color-scheme: light) {
    :root {
        --bg-primary: #f5f5f5;
        --bg-secondary: #ffffff;
        --bg-tertiary: #e8e8e8;
        --bg-card: #ffffff;
        --text-primary: #1a1a1a;
        --text-secondary: #4a4a4a;
    }
}
```

---

## 📊 Monitoramento de Logs

### Ver Logs Detalhados no GitHub Actions

1. Vá em **Actions**
2. Clique na última execução
3. Expanda cada step:
   - **Run scraper**: Veja URLs processadas
   - **Check for changes**: Veja se houve alterações
   - **Summary**: Resumo da execução

### Adicionar Mais Logs

Edite `scraper.py`, adicione print statements:

```python
print(f"🔍 Processando: {url}")
print(f"✅ Título: {title}")
print(f"💰 Preço: {price}")
print(f"🖼️ Imagem: {image[:50]}...")
```

---

## 🚨 Solução de Problemas Avançados

### Erro: `ModuleNotFoundError: No module named 'bs4'`

**Causa**: Dependências não instaladas  
**Solução**: Verifique se `requirements.txt` existe e tem:
```
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
```

### Erro: `403 Forbidden`

**Causa**: Site bloqueou o IP do GitHub  
**Soluções**:

1. Adicione delays maiores:
```python
time.sleep(5)  # Aumentar de 2 para 5 segundos
```

2. Use proxies rotativos (avançado):
```python
PROXIES = {
    'http': 'http://seu-proxy.com:8080',
    'https': 'http://seu-proxy.com:8080',
}
response = requests.get(url, headers=HEADERS, proxies=PROXIES)
```

### Erro: `JSONDecodeError`

**Causa**: `data.json` mal formatado  
**Solução**: Use um validador JSON online:
- https://jsonlint.com/
- Cole seu JSON
- Corrija erros apontados

### Imagens Não Carregam (Hotlink Protection)

**Causa**: Site bloqueia referrers externos  
**Solução**: Baixe e hospede imagens localmente:

```python
def download_image(url, filename):
    response = requests.get(url, headers=HEADERS)
    with open(f'images/{filename}', 'wb') as f:
        f.write(response.content)
    return f'images/{filename}'
```

---

## 🔐 Segurança e Boas Práticas

### ❌ Nunca Faça:

- Não adicione senhas ou tokens no código
- Não faça scraping agressivo (respeite rate limits)
- Não ignore robots.txt

### ✅ Sempre Faça:

- Use delays entre requisições
- Verifique Terms of Service dos sites
- Use User-Agent realista
- Trate erros graciosamente

---

## 📈 Otimizações de Performance

### 1. Cache de Imagens

```python
# Salvar hash das imagens para evitar re-download
import hashlib

def image_hash(url):
    return hashlib.md5(url.encode()).hexdigest()[:8]
```

### 2. Paralelização (Cuidado!)

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(scrape_product, urls)
```

⚠️ **Atenção**: Pode causar banimento se muitas requisições simultâneas!

### 3. Lazy Loading no Frontend

Já implementado! As imagens usam `loading="lazy"`.

---

## 🎨 Customizações de Interface

### Adicionar Contador de Desconto

```javascript
// Em script.js
function calculateDiscount(originalPrice, currentPrice) {
    const discount = ((originalPrice - currentPrice) / originalPrice) * 100;
    return discount.toFixed(0);
}

// Adicione um badge de desconto no HTML
```

### Adicionar Wishlist Compartilhável

```javascript
function shareWishlist() {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    alert('Link copiado! 🎉');
}
```

### Adicionar Modo Escuro/Claro Manual

```html
<!-- Adicione no header -->
<button onclick="toggleTheme()">🌙/☀️</button>
```

```javascript
function toggleTheme() {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
}
```

---

## 📚 Recursos Úteis

- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.asp)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## 🤝 Contribuindo com Melhorias

Tem uma ideia? Abra uma issue no GitHub com:
1. **Descrição** da funcionalidade
2. **Caso de uso** (por que seria útil)
3. **Exemplo** de código (se possível)

---

**🚀 Happy Scraping!**
