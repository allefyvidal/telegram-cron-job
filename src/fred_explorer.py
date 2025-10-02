"""
🔍 EXPLORADOR FRED - Versão Simplificada
"""

import requests
import os

class FredExplorer:  # ← ESTA é a única declaração da classe
    def __init__(self):
        self.api_key = os.getenv('FRED_API_KEY')  # Direto da environment variable
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def buscar_series_brasil(self):
        """Busca especificamente séries brasileiras"""
        print("🇧🇷 Buscando séries do Brasil...")
        
        if not self.api_key:
            print("❌ FRED_API_KEY não configurada!")
            return []
        
        endpoint = "category/series"
        params = {
            'api_key': self.api_key,
            'file_type': 'json',
            'category_id': 32351,  # Categoria Brasil
            'limit': 20
        }
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                series = data.get('seriess', [])
                
                print(f"✅ {len(series)} séries brasileiras encontradas:")
                print("=" * 60)
                
                for serie in series:
                    print(f"📊 {serie['id']}")
                    print(f"   📝 {serie['title']}")
                    print(f"   🕐 {serie.get('frequency', 'N/A')}")
                    print(f"   📏 {serie.get('units', 'N/A')}")
                    print()
                
                return series
            else:
                print(f"❌ Erro API: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"💥 Erro: {e}")
            return []

def main():
    print("🚀 EXPLORADOR FRED - INICIANDO...")
    explorer = FredExplorer()
    explorer.buscar_series_brasil()
    print("🎯 EXPLORAÇÃO CONCLUÍDA!")

if __name__ == "__main__":
    main()
