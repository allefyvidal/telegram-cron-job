"""
🔍 TESTADOR API B3 CORE CALCULATION
"""

import requests
import json

def testar_api_b3_core():
    """Testa acesso à API de Cálculo CORE da B3"""
    
    base_url = "https://api-listados-cert.b3.com.br/api/cors-app/v2"
    
    endpoints = [
        "/reference-data",           # Dados de referência (mais provável de funcionar)
        "/risk-accounts",            # Lista de contas
    ]
    
    print("🔍 TESTANDO API B3 CORE CALCULATION...")
    print("=" * 50)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"📡 Testando: {endpoint}")
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ SUCESSO! Status: {response.status_code}")
                data = response.json()
                print(f"   📊 Resposta: {json.dumps(data, indent=2)[:200]}...")
            elif response.status_code == 401:
                print(f"   🔐 PRECISA DE OAUTH2 - Apenas clientes B2B")
            elif response.status_code == 403:
                print(f"   🚫 ACESSO PROIBIDO - Restrito a participantes")
            else:
                print(f"   ❌ Status: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"   💥 ERRO: {e}")
        
        print("-" * 40)

def verificar_documentacao():
    """Analisa a documentação para entender requisitos"""
    print("\n📋 ANÁLISE DA DOCUMENTAÇÃO:")
    print("• Tipo: REST com OAuth2")
    print("• Basepath: /api/cors-app/v2") 
    print("• Tags: LISTADOSPUBLICA")
    print("• Schemes: https")
    print("• Autenticação: OAuth2 com scope específico")
    print("• Destinada a: Participantes do serviço de risco")

def main():
    print("🚀 INICIANDO TESTE DA API B3 CORE...")
    testar_api_b3_core()
    verificar_documentacao()
    print("\n🎯 CONCLUSÃO: API para cálculo de risco institucional")

if __name__ == "__main__":
    main()
