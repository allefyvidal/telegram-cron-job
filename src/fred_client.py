"""
🇺🇸 CLIENTE FRED API
"""

import requests
from src.config import API_KEYS, FRED_SERIES

class FredClient:
    def __init__(self):
        self.api_key = API_KEYS['fred']
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
    
    def buscar_serie(self, serie_id: str):
        """Busca dados de uma série específica do FRED"""
        try:
            params = {
                'series_id': serie_id,
                'api_key': self.api_key,
                'file_type': 'json',
                'sort_order': 'desc',
                'limit': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                observations = data.get('observations', [])
                
                if observations:
                    return observations[0]
            
            return None
            
        except Exception as e:
            print(f"❌ Erro FRED {serie_id}: {e}")
            return None
    
    def buscar_todos_dados(self):
        """Busca dados de todas as séries configuradas"""
        resultados = []
        
        for nome, serie_id in FRED_SERIES.items():
            print(f"🔍 FRED: Buscando {nome}...")
            
            dados = self.buscar_serie(serie_id)
            if dados and dados.get('value') and dados['value'] != '.':
                resultados.append({
                    'fonte': 'FRED',
                    'nome': nome,
                    'valor': float(dados['value']),
                    'data': dados.get('date'),
                    'categoria': 'Econômico'
                })
                print(f"   ✅ {nome}: {dados['value']}")
            else:
                print(f"   ⚠️  {nome}: Sem dados")
        
        return resultados
