#!/usr/bin/env python3
"""
Script de Web Scraping para Lista de Desejos
Extrai imagem, título e preço de URLs de produtos usando OpenGraph e fallbacks
"""

import json
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import time

# Headers realistas para evitar bloqueios (simula Chrome no Windows)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}


def extract_domain(url):
    """Extrai o domínio principal da URL (ex: amazon.com.br)"""
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remove 'www.' se existir
    domain = domain.replace('www.', '')
    return domain


def clean_price(price_text):
    """
    Limpa e normaliza texto de preço
    Procura por padrões como: R$ 299,90 ou $50.00
    """
    if not price_text:
        return None
    
    # Remove espaços extras e quebras de linha
    price_text = ' '.join(price_text.split())
    
    # Padrões comuns de preço
    patterns = [
        r'R\$\s*(\d+\.?\d*,\d{2})',  # R$ 1.299,90 ou R$ 299,90
        r'R\$\s*(\d+,\d{2})',         # R$ 299,90
        r'\$\s*(\d+\.\d{2})',         # $50.00
        r'(\d+\.?\d*,\d{2})',         # 1.299,90
    ]
    
    for pattern in patterns:
        match = re.search(pattern, price_text)
        if match:
            price = match.group(0)
            # Adiciona R$ se não tiver símbolo
            if not price.startswith(('R$', '$')):
                price = 'R$ ' + price
            return price
    
    return None


def scrape_product(url):
    """
    Função principal de scraping
    Retorna dicionário com: image, title, price, url, store
    """
    print(f"\n🔍 Processando: {url}")
    
    try:
        # Faz a requisição com timeout
        response = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extrai o domínio da loja
        store = extract_domain(url)
        
        # ===== EXTRAÇÃO DE IMAGEM =====
        image = None
        
        # 1. Tenta OpenGraph (og:image) - Padrão mais confiável
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image = og_image['content']
        
        # 2. Fallback: Twitter Card
        if not image:
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                image = twitter_image['content']
        
        # 3. Fallback: Link rel="image_src"
        if not image:
            link_image = soup.find('link', rel='image_src')
            if link_image and link_image.get('href'):
                image = link_image['href']
        
        # 4. Fallback específico para Amazon
        if not image and 'amazon' in store:
            amazon_img = soup.find('img', id='landingImage')
            if amazon_img and amazon_img.get('src'):
                image = amazon_img['src']
        
        # 5. Último recurso: primeira imagem grande do produto
        if not image:
            product_img = soup.find('img', class_=re.compile(r'product|main|zoom|gallery', re.I))
            if product_img and product_img.get('src'):
                image = product_img['src']
        
        # Se a imagem for relativa, converte para absoluta
        if image and not image.startswith('http'):
            from urllib.parse import urljoin
            image = urljoin(url, image)
        
        # ===== EXTRAÇÃO DE TÍTULO =====
        title = None
        
        # 1. Tenta OpenGraph (og:title)
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            title = og_title['content']
        
        # 2. Fallback: Tag <title>
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text()
        
        # 3. Fallback: h1 da página
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text()
        
        # Limpa o título
        if title:
            title = ' '.join(title.split()).strip()
            # Remove sufixos comuns de lojas
            title = re.sub(r'\s*[\|\-]\s*(Amazon|Mercado Livre|Shopee|Magalu|Kabum).*$', '', title, flags=re.I)
        
        # ===== EXTRAÇÃO DE PREÇO =====
        price = None
        
        # 1. Tenta OpenGraph (og:price:amount)
        og_price = soup.find('meta', property='og:price:amount')
        if og_price and og_price.get('content'):
            price = f"R$ {og_price['content']}"
        
        # 2. Fallback: Seletores comuns de preço (CUSTOMIZE AQUI POR LOJA!)
        if not price:
            # Lista de seletores CSS comuns para preço
            price_selectors = [
                # Amazon
                '.a-price-whole',
                '#priceblock_ourprice',
                '#priceblock_dealprice',
                'span.a-offscreen',
                
                # Mercado Livre
                '.andes-money-amount__fraction',
                '.price-tag-fraction',
                
                # Magalu
                '[data-testid="price-value"]',
                '.price-template__text',
                
                # Kabum
                '.finalPrice',
                '.priceCard',
                
                # Shopee
                '.item-price',
                
                # Genéricos (mais comuns)
                '.price',
                '.product-price',
                '.sale-price',
                '.special-price',
                '[itemprop="price"]',
                '.current-price',
                '.valor',
                '.preco',
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text()
                    cleaned = clean_price(price_text)
                    if cleaned:
                        price = cleaned
                        break
        
        # 3. Último recurso: busca por padrão de preço em texto
        if not price:
            # Procura por R$ seguido de números em todo o HTML
            text = soup.get_text()
            price_match = re.search(r'R\$\s*\d+\.?\d*,\d{2}', text)
            if price_match:
                price = price_match.group(0)
        
        # Se ainda não achou, marca como "Consultar"
        if not price:
            price = "Consultar no site"
            print(f"⚠️  Preço não encontrado automaticamente")
        
        # ===== VALIDAÇÃO FINAL =====
        if not image:
            print(f"⚠️  Imagem não encontrada")
            image = "https://via.placeholder.com/400x400/1a1a2e/eee?text=Sem+Imagem"
        
        if not title:
            print(f"⚠️  Título não encontrado")
            title = "Produto sem título"
        
        result = {
            "image": image,
            "title": title[:150],  # Limita título a 150 caracteres
            "price": price,
            "url": url,
            "store": store
        }
        
        print(f"✅ Extraído: {title[:50]}... | {price}")
        return result
        
    except requests.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return {
            "image": "https://via.placeholder.com/400x400/1a1a2e/eee?text=Erro",
            "title": "Erro ao carregar produto",
            "price": "Consultar no site",
            "url": url,
            "store": extract_domain(url)
        }
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None


def main():
    """
    Função principal: lê data.json, atualiza preços ou adiciona novas URLs
    """
    print("=" * 60)
    print("🚀 INICIANDO SCRAPER DE WISHLIST")
    print("=" * 60)
    
    # Tenta carregar o arquivo existente
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            products = data.get('products', [])
    except FileNotFoundError:
        print("ℹ️  data.json não encontrado, criando novo...")
        products = []
    
    # Aqui você pode adicionar lógica para ler novas URLs de um arquivo separado
    # Por exemplo, ler de 'urls.txt' e adicionar produtos novos:
    """
    try:
        with open('urls.txt', 'r', encoding='utf-8') as f:
            new_urls = [line.strip() for line in f if line.strip()]
        
        # Remove URLs que já estão no data.json
        existing_urls = {p['url'] for p in products}
        new_urls = [url for url in new_urls if url not in existing_urls]
        
        # Adiciona novos produtos
        for url in new_urls:
            product = scrape_product(url)
            if product:
                products.append(product)
            time.sleep(2)  # Delay entre requisições
    except FileNotFoundError:
        pass
    """
    
    # Atualiza preços dos produtos existentes
    print(f"\n📦 Atualizando {len(products)} produtos existentes...")
    for i, product in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}]", end=" ")
        updated = scrape_product(product['url'])
        if updated:
            # Atualiza apenas preço e imagem (mantém título original se preferir)
            product['price'] = updated['price']
            product['image'] = updated['image']
            # product['title'] = updated['title']  # Descomente para atualizar título também
        
        # Delay para não sobrecarregar o servidor
        if i < len(products):
            time.sleep(3)
    
    # Salva o arquivo atualizado
    output = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "products": products
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ CONCLUÍDO! {len(products)} produtos salvos em data.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
