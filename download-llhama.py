import requests
import os
from tqdm import tqdm # Importa a biblioteca tqdm

# Crie a pasta de destino, se necessário
output_folder = "Llama-3.2-3B-Instruct" # Ou o nome do modelo que você está baixando
os.makedirs(output_folder, exist_ok=True)

# --- PASSO 1: COLOQUE A NOVA URL DA META AQUI ---
# ATENÇÃO: Esta URL é temporária e expira.
url = "https://llama3-2-lightweight.llamameta.net/?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoiZ29mMzV0bDNlaG9qdHJqYXBsOWpoOGNwIiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTItbGlnaHR3ZWlnaHQubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc1MDM1NjI4OH19fV19&Signature=NKiEfTdN3HVEmhRlYNui9h-194vDlkNrhrfCTqZ1KnzkvV4XS1b7pHdBWyD7IdhegNFaIncngefi4GZR5QoJTkpiyDGmZdcvq5SpPUc8hX4Uaf8OHipg6tcKQhk2J6-s-xWfCvYQMz0AWBt3ldUbvfjh9TeDXywXVlEQszXiymbG7DQUBeH1ftGh6-cduqQ9SeVV4hfeTCipl8H%7ElmZHounPIjFyBJQd%7EBFK0pvJ3-NM1sq3r0Q3aYBvanl5XngRDqsHkm4IHjZE0jxaBvjNwN6h3TCF%7EMq6Oj--wHINv-Ip5MqcBt1ZuVgi-vdPxPiNt3OGZKXDmnGxsy7U0LyUMw__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=3979955262221651" # Substitua esta string pela nova URL que você recebeu por e-mail

# Caminho onde o arquivo será salvo
# Certifique-se que o nome do arquivo corresponde ao modelo que você está baixando
# (ex: consolidated.00.pth, checklist.chk, params.json, tokenizer.model)
# Você pode precisar rodar este script várias vezes, uma para cada arquivo do modelo.
output_filename = "consolidated.00.pth" # Mude isso se estiver baixando outro arquivo
output_path = os.path.join(output_folder, output_filename)

# Cabeçalhos HTTP com User-Agent válido
headers = {
    "User-Agent": "Mozilla/5.0"
}

# --- PASSO 2: CONFIGURAÇÃO DO CERTIFICADO SSL ---
# Use o caminho para o seu arquivo cacert.pem
VERIFY_SSL = "C:\\cacert\\cacert.pem" # Caminho para o seu arquivo .pem

# Se o VERIFY_SSL acima não funcionar, como último recurso, você pode tentar:
# VERIFY_SSL = False # (Menos seguro, desabilita a verificação SSL)


print(f"Baixando {output_filename}...")
if VERIFY_SSL is False:
    print("AVISO: Verificação SSL desabilitada. Isso é menos seguro.")
elif isinstance(VERIFY_SSL, str):
    if os.path.exists(VERIFY_SSL):
        print(f"Usando certificado CA customizado: {VERIFY_SSL}")
    else:
        print(f"ERRO: Arquivo de certificado CA customizado não encontrado: {VERIFY_SSL}")
        print("Verifique o caminho e tente novamente, ou mude VERIFY_SSL para True ou False.")
        exit() # Sai do script se o arquivo de certificado não for encontrado


try:
    with requests.get(url, headers=headers, stream=True, verify=VERIFY_SSL) as r:
        r.raise_for_status() # Verifica se houve erros HTTP (4xx ou 5xx)
        total_size = int(r.headers.get('content-length', 0))

        with open(output_path, 'wb') as f, tqdm(
            desc=output_path,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # Filtra chunks vazios que podem ser enviados pelo keep-alive
                    size = f.write(chunk)
                    bar.update(size)

    print(f"\nDownload de {output_filename} concluído: {output_path}")

except requests.exceptions.SSLError as errs:
    print(f"Erro de SSL: {errs}")
    print("Isso pode ser devido a um proxy na sua rede que inspeciona tráfego HTTPS.")
    print("Verifique se o caminho para o arquivo 'VERIFY_SSL' está correto no script.")
    print(f"Caminho configurado: {VERIFY_SSL}")
    print("Se o erro persistir, tente configurar VERIFY_SSL = False (menos seguro).")
except requests.exceptions.HTTPError as errh:
    print(f"Erro HTTP: {errh}")
    print("Verifique se a URL de download ainda é válida. URLs da Meta podem expirar.")
    print("Se a URL expirou, você precisará gerar uma nova no site da Meta.")
except requests.exceptions.ConnectionError as errc:
    print(f"Erro de Conexão: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Erro de Timeout: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Erro na Requisição: {err}")
except IOError as e:
    print(f"Erro de I/O ao salvar o arquivo: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

