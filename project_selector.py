import os
import sys
import time
import requests

# Script para automação de triagem de projetos do GitHub para replicação da validação do pytest-ranking
# Requisitos: pip install requests
# Para rodar, você precisará de um Token do GitHub (PAT) para evitar limites de requisições (rate limits).
# Defina a variável de ambiente: export GITHUB_TOKEN="seu_token_aqui"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"
else:
    print("Aviso: GITHUB_TOKEN não está configurado. Você atingirá os limites de taxa da API rapidamente.")

BASE_URL = "https://api.github.com"

def get_repo_details(owner, repo):
    """Obtém detalhes do repositório como estrelas e tamanho."""
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return {
            "stars": data.get("stargazers_count", 0),
            "size": data.get("size", 0),  # em KB
            "default_branch": data.get("default_branch", "main")
        }
    return None

def check_github_actions(owner, repo):
    """Verifica se há workflows do GitHub Actions no repositório."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/contents/.github/workflows"
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200

def has_failed_runs(owner, repo):
    """Verifica se há pelo menos uma execução de teste (TSR) com falha no branch padrão."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/actions/runs"
    params = {"status": "failure", "per_page": 5}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        return len(runs) > 0
    return False

def check_pytest_usage(owner, repo):
    """Verifica se o projeto faz menção a pytest nos arquivos de dependência mais comuns."""
    filenames = ["requirements.txt", "pyproject.toml", "setup.py"]
    for filename in filenames:
        url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{filename}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            content = response.json().get("content", "")
            # Decodificar base64 básico se necessário
            import base64
            try:
                decoded = base64.b64decode(content).decode("utf-8")
                if "pytest" in decoded.lower():
                    return True
            except Exception:
                pass
    return False

def evaluate_project(repo_path):
    """Aplica os filtros de seleção dos autores em um repositório específico."""
    parts = repo_path.strip().split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[-2], parts[-1]
    
    print(f"\nAvaliando {owner}/{repo}...")
    
    # 1. Obter detalhes do repositório (Estrelas, Tamanho)
    details = get_repo_details(owner, repo)
    if not details:
        print(f"[-] Repositório não encontrado ou inacessível: {owner}/{repo}")
        return None
        
    # Critério: > 1000 estrelas
    if details["stars"] < 1000:
        print(f"[-] Reprovado: {details['stars']} estrelas (mínimo exigido: 1000)")
        return None
    print(f"[+] Aprovado: {details['stars']} estrelas")
    
    # Critério sugerido: clonagem rápida (tamanho aproximado < 150MB para garantir < 1 min)
    if details["size"] > 150000:  # ~150MB
        print(f"[-] Reprovado: Repositório muito grande ({details['size'] / 1024:.1f} MB)")
        # Este é um proxy para o critério "clone < 1 min"
    else:
        print(f"[+] Aprovado: Tamanho aceitável ({details['size'] / 1024:.1f} MB)")

    # 2. Verificar uso de GitHub Actions
    if not check_github_actions(owner, repo):
        print("[-] Reprovado: Sem workflows do GitHub Actions ativos.")
        return None
    print("[+] Aprovado: Usa GitHub Actions")

    # 3. Verificar uso do Pytest
    if not check_pytest_usage(owner, repo):
        print("[-] Reprovado: Não foi detectado uso direto de 'pytest' nas dependências básicas.")
        # Pode ser um falso negativo se o pytest estiver em arquivos aninhados, mas serve de filtro rápido
    else:
        print("[+] Aprovado: Usa Pytest")

    # 4. Verificar se possui builds com falha no histórico recente
    if not has_failed_runs(owner, repo):
        print("[-] Reprovado: Nenhuma execução falha recente encontrada no branch padrão.")
        return None
    print("[+] Aprovado: Histórico possui execuções falhas recentes")

    print(f"[🎉] PROJETO ELEGÍVEL PARA FORK: https://github.com/{owner}/{repo}")
    return {
        "repo": f"{owner}/{repo}",
        "stars": details["stars"],
        "url": f"https://github.com/{owner}/{repo}"
    }

if __name__ == "__main__":
    # Exemplo de uso com alguns repositórios de teste conhecidos
    test_repos = [
        "django/django",
        "psf/requests",
        "pytest-dev/pytest",
        "encode/django-rest-framework"
    ]
    
    print("Iniciando varredura de exemplo nos seguintes repositórios:")
    for r in test_repos:
        print(f" - {r}")
        
    eligible = []
    for r in test_repos:
        res = evaluate_project(r)
        if res:
            eligible.append(res)
        time.sleep(1) # Evitar limites de taxa secundários
        
    print("\n" + "="*40)
    print(f"Varredura concluída. Encontrados {len(eligible)} projetos elegíveis de {len(test_repos)} testados.")
    for el in eligible:
        print(f" - {el['repo']} ({el['stars']} estrelas) -> {el['url']}")
