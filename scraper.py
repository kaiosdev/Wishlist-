import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import os

# Cabeçalhos para fingir ser um navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_product_details(url):
    try:
        print(f"🔍 Acessando: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"⚠️ Erro {response.status_code} em {url}")
            return None

        soup = BeautifulSoup(response.content, 'lxml')
        
        # 1. Dados Básicos (OpenGraph)
        og_title = soup.find("meta", property="og:title")
        og_image = soup.find("meta", property="og:image")
        
        title = og_title['content'] if og_title else soup.title.string
        image = og_image['content'] if og_image else "https://placehold.co/400?text=Sem+Imagem"
        
        # 2. Preço (Seletores Brasileiros)
        price = None
        price_selectors = [
            '.a-price-whole',           # Amazon
            '.andes-money-amount__fraction', # Mercado Livre
            '.finalPrice',              # Kabum
            '#blocoValores .preco_desconto', # Kabum 2
            '[data-testid="price-value"]',   # Magalu
            '.p-price strong',               # Magalu 2
            '.sales-price',             # Genérico
            '[itemprop="price"]'        # Genérico
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                raw = element.get_text(strip=True)
                clean = raw.replace('R$', '').replace('$', '').strip()
                if clean and len(clean) < 15:
                    price = f"R$ {clean}"
                    break
        
        if not price: price = "Ver no site"

        # Define a loja
        store = "Loja"
        if "amazon" in url: store = "Amazon"
        elif "mercadolivre" in url: store = "Mercado Livre"
        elif "kabum" in url: store = "Kabum"
        elif "magazineluiza" in url: store = "Magalu"
        elif "shopee" in url: store = "Shopee"

        return {
            "title": title.strip()[:60] + "...",
            "image": image,
            "price": price,
            "url": url,
            "store": store
        }
        
    except Exception as e:
        print(f"❌ Erro em {url}: {e}")
        return None

def main():
    # Carrega dados antigos (Cache)
    old_data = {}
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
                for prod in content.get('products', []):
                    old_data[prod['url']] = prod
        except: pass

    # Lê URLs do arquivo txt
    urls = []
    if os.path.exists('urls.txt'):
        with open('urls.txt', 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    
    if not urls:
        urls = list(old_data.keys())

    print(f"📋 Processando {len(urls)} produtos...")
    final_products = []
    
    for url in urls:
        details = get_product_details(url)
        if details:
            final_products.append(details)
        elif url in old_data:
            print(f"⚠️ Usando cache para: {url}")
            final_products.append(old_data[url])
        
        time.sleep(random.uniform(2, 5)) # Pausa anti-bloqueio

    # Salva
    output = {
        'last_updated': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'products': final_products
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()