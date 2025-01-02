import yfinance as yf

class GetCoins():
    def __init__(self):
        self.dollar_symbol = "USDBRL=X"  # Símbolo do dólar em relação ao real
        self.bitcoin_symbol = "BTC-USD"  # Símbolo do Bitcoin em relação ao dólar
    
    def get_dollar_quote(self):
        try:
            ticker = yf.Ticker(self.dollar_symbol)
            data = ticker.history(period="1d")
            # Retorna o preço de fechamento mais recente
            return data["Close"].iloc[-1]
        except Exception as e:
            print("Erro ao obter cotação do dólar:", e)
            return None

    def get_bitcoin_quote(self):
        try:
            ticker = yf.Ticker(self.bitcoin_symbol)
            data = ticker.history(period="1d")
            # Retorna o preço de fechamento mais recente
            return data["Close"].iloc[-1]
        except Exception as e:
            print("Erro ao obter cotação do Bitcoin:", e)
            return None
        

