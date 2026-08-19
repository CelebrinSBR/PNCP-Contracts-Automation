import requests

# URL exata que o seu programa estava tentando acessar (peguei do seu log anterior)
url = "https://pncp.gov.br/api/consulta/v1/contratos?dataInicial=20260805&dataFinal=20260811&cnpjOrgao=00394429000100&pagina=1&tamanhoPagina=50"

# Disfarçando o nosso script como se fosse um Google Chrome de verdade
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# Forçando o Python a NÃO usar nenhuma configuração de proxy da sua casa
proxies = {
    "http": "",
    "https": ""
}

print("Batendo na porta do PNCP...")

try:
    response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\nSUCESSO! A API está online e respondeu:")
        # Imprime apenas o começo para não poluir a tela inteira
        print(str(response.json())[:500] + "...\n")
        
    else:
        print("\nO SITE RECUSOU A CONEXÃO. Veja o motivo:")
        print(response.text[:1000]) 
        
except Exception as e:
    print(f"\nERRO CRÍTICO (A conexão nem chegou a sair do seu PC): {e}")