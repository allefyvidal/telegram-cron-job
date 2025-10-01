# 🤖 Bot de Alertas do Telegram - Bolsa de Valores

Bot automatizado que monitora ações da bolsa brasileira e envia alertas inteligentes via Telegram quando preços-alvo são atingidos.

## ✨ Funcionalidades

- 📊 **Monitoramento em tempo real** de múltiplas ações
- 🎯 **Alertas personalizados** para preços máximos e mínimos
- 📈 **Análise técnica básica** (tendência, amplitude, posição no range)
- ⏰ **Execução automática** via GitHub Actions (cron job)
- 🔔 **Notificações formatadas** com emojis e informações relevantes
- 🛡️ **Tratamento robusto de erros** e logging detalhado

## 🚀 Como Usar

### 1. Criar Bot no Telegram

1. Abra o Telegram e busque por [@BotFather](https://t.me/botfather)
2. Envie `/newbot` e siga as instruções
3. Guarde o **token** que o BotFather fornecer (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
4. Inicie uma conversa com seu novo bot
5. Para obter seu **Chat ID**, envie uma mensagem para [@userinfobot](https://t.me/userinfobot)

### 2. Configurar no GitHub

1. Fork este repositório
2. Vá em `Settings` → `Secrets and variables` → `Actions`
3. Adicione dois secrets:
   - `TELEGRAM_BOT_TOKEN`: Cole o token do BotFather
   - `TELEGRAM_CHAT_ID`: Cole seu Chat ID

### 3. Personalizar Ações Monitoradas

Edite o arquivo `alertas_config.json`:

```json
{
  "acoes": [
    {
      "ticker": "PETR4",
      "nome": "Petrobras PN",
      "preco_alvo_max": 42.00,  // Alerta de VENDA
      "preco_alvo_min": 38.00,  // Alerta de COMPRA
      "descricao": "Petróleo e gás"
    }
  ]
}
```

### 4. Ativar GitHub Actions

1. Vá na aba `Actions` do seu repositório
2. Clique em "I understand my workflows, go ahead and enable them"
3. O bot começará a executar automaticamente!

## ⏰ Quando o Bot Executa?

Por padrão, o bot executa:
- **De hora em hora** durante o horário de pregão (09:00 às 18:00, horário de Brasília)
- **Apenas em dias úteis** (segunda a sexta-feira)
- Você também pode executar **manualmente** pela aba Actions

Para alterar a frequência, edite o arquivo `.github/workflows/telegram-cron.yml`:

```yaml
schedule:
  - cron: '0 12-21 * * 1-5'  # Ajuste conforme necessário
```

## 📋 Exemplo de Alerta

```
📊 Relatório de Mercado
🕐 01/10/2025 14:30:45
────────────────────────────────────────

🟢 ALERTA COMPRA: PETR4 atingiu R$ 38.00 (alvo mínimo: R$ 38.00)

🟢 PETR4: R$ 38.00 (+1.25%)
   └ Tendência: ALTA
   └ Amplitude: 2.50%

🔴 VALE3: R$ 62.50 (-0.80%)
   └ Tendência: BAIXA
   └ Amplitude: 1.75%

✅ Nenhum outro alerta disparado no momento
```

## 🛠️ Melhorias Implementadas

### Em relação à versão original:

✅ **Código Profissional**
- Orientação a objetos (classes separadas por responsabilidade)
- Type hints para melhor documentação
- Docstrings completas

✅ **Tratamento de Erros Robusto**
- Try/except em todas operações críticas
- Logging detalhado de erros
- Fallbacks para configurações

✅ **API de Cotações Real**
- Integração com BRAPI (API gratuita de ações BR)
- Dados em tempo real
- Informações completas (preço, variação, volume, etc.)

✅ **Análise Técnica**
- Cálculo de tendência (ALTA/BAIXA/LATERAL)
- Amplitude do dia
- Posição no range

✅ **GitHub Actions Otimizado**
- Verificação de horário de pregão
- Cache de dependências Python
- Upload de logs em caso de erro
- Execução manual disponível

✅ **Configuração Flexível**
- Suporte a variáveis de ambiente
- Configuração padrão robusta
- Fácil adição de novas ações

## 🔧 Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/telegram-cron-job.git
cd telegram-cron-job

# Configure as variáveis de ambiente
export TELEGRAM_BOT_TOKEN="seu_token_aqui"
export TELEGRAM_CHAT_ID="seu_chat_id_aqui"

# Instale dependências
pip install requests

# Execute o bot
python bot_alertas.py
```

## 📊 APIs Utilizadas

- **BRAPI** (https://brapi.dev) - Cotações da bolsa brasileira
  - Gratuito
  - Sem necessidade de API key
  - Dados em tempo real

## 🤝 Contribuindo

Sugestões de melhorias:

1. 📱 Adicionar suporte a múltiplos chats
2. 📈 Implementar médias móveis (SMA, EMA)
3. 🎨 Gráficos de candlestick inline
4. 💾 Histórico de preços em banco de dados
5. 🔔 Alertas de volume anormal
6. 📊 Indicadores avançados (RSI, MACD, Bollinger)

## ⚠️ Avisos Importantes

- Este bot é apenas para fins educacionais
- Não constitui recomendação de investimento
- Sempre faça sua própria análise antes de investir
- A API gratuita pode ter limites de requisições
- Resultados passados não garantem resultados futuros

## 📝 Licença

MIT License - Sinta-se livre para usar e modificar!

## 💡 Dicas Pro

### Para Day Trading:
- Configure alertas mais próximos do preço atual
- Execute a cada 15-30 minutos (ajuste o cron)
- Adicione mais indicadores técnicos

### Para Swing Trading:
- Configure alvos mais distantes
- Execute 1-2 vezes por dia
- Foque em tendências de médio prazo

### Para Long Term:
- Monitore apenas suportes/resistências importantes
- Execute diariamente
- Adicione análise fundamentalista

---

Feito com ❤️ para traders brasileiros 🇧🇷
