"""
📊 INTEGRAÇÃO GOOGLE SHEETS - Gerenciador de Preços de Compra
"""

import gspread
from google.oauth2.service_account import Credentials
import os
import json
from datetime import datetime

class GoogleSheetsManager:
    def __init__(self):
        self.credenciais = self._carregar_credenciais()
        self.client = None
        self.planilha = None
        self.worksheet = None
        
    def _carregar_credenciais(self):
        """Carrega credenciais do Google Sheets do environment variable"""
        try:
            creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
            if not creds_json:
                print("❌ GOOGLE_SHEETS_CREDENTIALS não encontrado")
                return None
            
            # Converte string JSON para dict
            creds_dict = json.loads(creds_json)
            
            # Define escopos
            escopos = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credenciais = Credentials.from_service_account_info(
                creds_dict, 
                scopes=escopos
            )
            
            return credenciais
            
        except Exception as e:
            print(f"❌ Erro ao carregar credenciais: {e}")
            return None
    
    def conectar_planilha(self, planilha_id: str, worksheet_name: str = "Criptomoedas"):
        """Conecta à planilha específica"""
        try:
            if not self.credenciais:
                return False
                
            self.client = gspread.authorize(self.credenciais)
            self.planilha = self.client.open_by_key(planilha_id)
            
            # Tenta acessar a worksheet, se não existir cria
            try:
                self.worksheet = self.planilha.worksheet(worksheet_name)
            except gspread.exceptions.WorksheetNotFound:
                print(f"📝 Criando nova worksheet: {worksheet_name}")
                self.worksheet = self.planilha.add_worksheet(
                    title=worksheet_name, 
                    rows="100", 
                    cols="10"
                )
                # Cria cabeçalhos
                self._criar_cabecalhos()
            
            print(f"✅ Conectado à planilha: {planilha_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar planilha: {e}")
            return False
    
    def _criar_cabecalhos(self):
        """Cria cabeçalhos da planilha"""
        cabecalhos = [
            "Criptomoeda",
            "Símbolo", 
            "Preço de Compra",
            "Quantidade",
            "Preço Atual",
            "Variação %",
            "Status",
            "Última Atualização",
            "Alerta Ativo",
            "Notas"
        ]
        self.worksheet.update('A1:J1', [cabecalhos])
    
    def adicionar_cripto(self, nome: str, simbolo: str, preco_compra: float, quantidade: float = 0):
        """Adiciona uma criptomoeda à planilha"""
        try:
            # Verifica se já existe
            registros = self.worksheet.get_all_records()
            for registro in registros:
                if registro.get('Símbolo') == simbolo:
                    print(f"⚠️ {nome} já existe na planilha")
                    return False
            
            # Adiciona nova linha
            nova_linha = [
                nome,
                simbolo,
                preco_compra,
                quantidade,
                0,  # Preço Atual
                0,  # Variação %
                "Ativo",
                datetime.now().strftime('%d/%m/%Y %H:%M'),
                "SIM",
                "Adicionado automaticamente"
            ]
            
            self.worksheet.append_row(nova_linha)
            print(f"✅ {nome} adicionado à planilha")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar cripto: {e}")
            return False
    
    def obter_criptos_monitoradas(self):
        """Obtém todas as criptomoedas para monitorar"""
        try:
            registros = self.worksheet.get_all_records()
            criptos = []
            
            for registro in registros:
                if registro.get('Alerta Ativo', '').upper() == 'SIM':
                    criptos.append({
                        'nome': registro.get('Criptomoeda', ''),
                        'simbolo': registro.get('Símbolo', ''),
                        'preco_compra': float(registro.get('Preço de Compra', 0)),
                        'quantidade': float(registro.get('Quantidade', 0)),
                        'status': registro.get('Status', '')
                    })
            
            return criptos
            
        except Exception as e:
            print(f"❌ Erro ao obter criptos: {e}")
            return []
    
    def atualizar_preco_atual(self, simbolo: str, preco_atual: float, variacao: float):
        """Atualiza preço atual e variação na planilha"""
        try:
            # Encontra a linha do símbolo
            celula = self.worksheet.find(simbolo)
            if not celula:
                return False
            
            linha = celula.row
            
            # Atualiza preço atual (coluna E) e variação (coluna F)
            self.worksheet.update_cell(linha, 5, preco_atual)  # Preço Atual
            self.worksheet.update_cell(linha, 6, variacao)     # Variação %
            self.worksheet.update_cell(linha, 8, datetime.now().strftime('%d/%m/%Y %H:%M'))  # Última atualização
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar preço: {e}")
            return False

# Exemplo de uso
def main():
    """Teste da integração com Google Sheets"""
    gs = GoogleSheetsManager()
    
    # Você precisa do ID da sua planilha (encontre na URL)
    planilha_id = "SEU_PLANILHA_ID_AQUI"  # Ex: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
    
    if gs.conectar_planilha(planilha_id):
        # Adiciona algumas criptos de exemplo
        gs.adicionar_cripto("Bitcoin", "BTC-USD", 45000.00, 0.1)
        gs.adicionar_cripto("Ethereum", "ETH-USD", 3000.00, 1.5)
        
        # Obtém criptos para monitorar
        criptos = gs.obter_criptos_monitoradas()
        print(f"📊 Criptos monitoradas: {len(criptos)}")

if __name__ == "__main__":
    main()
