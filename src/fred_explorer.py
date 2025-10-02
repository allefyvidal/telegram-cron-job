"""
🔍 EXPLORADOR FRED - Encontra fontes e séries automaticamente
"""

import requests
from src.config import API_KEYS

class FredExplorer:
    def __init__(self):
        self.api_key = API_KEYS['fred']
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def listar_fontes(self):
        """Lista TODAS as fontes de dados disponíveis"""
        print("🔍 Buscando fontes de dados...")
        
        endpoint = "sources"
        params = {
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                fontes = data.get('sources', [])
                
                print(f"✅ {len(fontes)} fontes encontradas:")
                print("-" * 50)
                
                for fonte in fontes:
                    print(f"📁 ID: {fonte['id']} | Nome: {fonte['name']}")
                    if fonte.get('link'):
                        print(f"   🔗 {fonte['link']}")
                    print()
                
                return fontes
            else:
                print(f"❌ Erro: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"💥 Erro ao buscar fontes: {e}")
            return []
    
    def buscar_series_por_fonte(self, source_id: int):
        """Busca séries de uma fonte específica"""
        print(f"🔍 Buscando séries da fonte {source_id}...")
        
        endpoint = "source/series"
        params = {
            'api_key': self.api_key,
            'file_type': 'json',
            'source_id': source_id,
            'limit': 50  # Primeiras 50 séries
        }
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                series = data.get('seriess', [])
                
                print(f"✅ {len(series)} séries encontradas:")
                print("-" * 50)
                
                for serie in series:
                    print(f"📊 {serie['id']}: {serie['title']}")
                    print(f"   📝 {serie.get('notes', 'Sem descrição')[:100]}...")
                    print(f"   🕐 Frequência: {serie.get('frequency', 'N/A')}")
                    print()
                
                return series
            else:
                print(f"❌ Erro: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"💥 Erro ao buscar séries: {e}")
            return []
    
    def buscar_series_brasil(self):
        """Busca especificamente séries brasileiras"""
        print("🇧🇷 Buscando séries do Brasil...")
        
        # Método 1: Buscar por categoria Brasil (ID 32351)
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
                print("-" * 50)
                
                series_brasil = []
                for serie in series:
                    info = {
                        'id': serie['id'],
                        'title': serie['title'],
                        'frequency': serie.get('frequency', 'N/A'),
                        'units': serie.get('units', 'N/A')
                    }
                    series_brasil.append(info)
                    
                    print(f"📊 {serie['id']}")
                    print(f"   📝 {serie['title']}")
                    print(f"   🕐 {serie.get('frequency', 'N/A')} | 📏 {serie.get('units', 'N/A')}")
                    print()
                
                return series_brasil
            else:
                print(f"❌ Erro: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"💥 Erro ao buscar séries brasileiras: {e}")
            return []

def explorar_fred():
    """Função para explorar o FRED"""
    explorer = FredExplorer()
    
    print("🎯 FRED EXPLORER - Descobrindo dados automaticamente")
    print("=" * 60)
    
    # 1. Buscar séries brasileiras
    series_brasil = explorer.buscar_series_brasil()
    
    # 2. Listar algumas fontes (opcional)
    print("\n📁 ALGUMAS FONTES DISPONÍVEIS:")
    fontes = explorer.listar_fontes()
    
    # Filtrar fontes internacionais interessantes
    fontes_interessantes = [
        fonte for fonte in fontes 
        if any(palavra in fonte['name'].lower() for palavra in 
              ['brazil', 'brasil', 'international', 'world', 'bank'])
    ]
    
    print("\n🌎 FONTES INTERNACIONAIS INTERESSANTES:")
    for fonte in fontes_interessantes[:10]:  # Mostrar apenas 10
        print(f"📍 {fonte['id']}: {fonte['name']}")

if __name__ == "__main__":
    explorar_fred()
