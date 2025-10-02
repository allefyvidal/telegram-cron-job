"""
🔍 EXPLORADOR FRED - Busca Séries Brasileiras Relevantes
"""

import requests
import os

class FredExplorer:
    def __init__(self):
        self.api_key = os.getenv('FRED_API_KEY')
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def buscar_series_por_palavra_chave(self, keyword: str):
        """Busca séries por palavra-chave"""
        print(f"🔍 Buscando séries com: '{keyword}'...")
        
        if not self.api_key:
            print("❌ FRED_API_KEY não configurada!")
            return []
        
        endpoint = "series/search"
        params = {
            'api_key': self.api_key,
            'file_type': 'json',
            'search_text': keyword,
            'limit': 10
        }
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                series = data.get('seriess', [])
                
                print(f"✅ {len(series)} séries encontradas para '{keyword}':")
                print("=" * 60)
                
                series_filtradas = []
                for serie in series:
                    # Filtra só séries relevantes (não descontinuadas)
                    if not serie.get('title', '').upper().startswith('DISCONTINUED'):
                        info = {
                            'id': serie['id'],
                            'title': serie['title'],
                            'frequency': serie.get('frequency', 'N/A'),
                            'units': serie.get('units', 'N/A')
                        }
                        series_filtradas.append(info)
                        
                        print(f"📊 {serie['id']}")
                        print(f"   📝 {serie['title']}")
                        print(f"   🕐 {serie.get('frequency', 'N/A')} | 📏 {serie.get('units', 'N/A')}")
                        print()
                
                return series_filtradas
            else:
                print(f"❌ Erro API: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"💥 Erro: {e}")
            return []
    
    def explorar_series_brasileiras(self):
        """Busca séries brasileiras relevantes"""
        print("🇧🇷 EXPLORANDO SÉRIES BRASILEIRAS RELEVANTES...")
        
        keywords = [
            "Brazil exchange rate",
            "Brazil interest rate", 
            "Brazil inflation",
            "Brazil GDP",
            "Brazil unemployment",
            "Brazil industrial production",
            "Brazil consumer price",
            "Bovespa",
            "Brazil currency",
            "Brazil central bank"
        ]
        
        todas_series = []
        
        for keyword in keywords:
            series = self.buscar_series_por_palavra_chave(keyword)
            todas_series.extend(series)
            print()  # Linha em branco entre buscas
        
        # Remove duplicatas
        series_unicas = []
        ids_vistos = set()
        
        for serie in todas_series:
            if serie['id'] not in ids_vistos:
                series_unicas.append(serie)
                ids_vistos.add(serie['id'])
        
        print(f"🎯 TOTAL DE {len(series_unicas)} SÉRIES BRASILEIRAS ÚNICAS ENCONTRADAS!")
        return series_unicas

def main():
    print("🚀 EXPLORADOR FRED AVANÇADO - INICIANDO...")
    explorer = FredExplorer()
    explorer.explorar_series_brasileiras()
    print("🎯 EXPLORAÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()
