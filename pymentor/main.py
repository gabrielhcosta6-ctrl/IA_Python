import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as configuracoes do arquivo .env
load_dotenv()

# Recupera a chave e o modelo da API
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

# Verifica se a chave foi configurada
if not API_KEY:
    print("Erro: configure a chave no arquivo .env.")
    raise SystemExit

# Conecta o programa ao OpenRouter
cliente = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

# Permite ao usuario escolher o nome do assistente
nome = input("Qual sera o nome do seu assistente? ")
nome = nome.strip()

if not nome:
    nome = "Jarvis"

print("\n====================================")
print(f"       {nome.upper()} - ASSISTENTE")
print("====================================") 
print("Conexao iniciada!")
print("Digite 'sair' para encerrar.\n")

# Guarda as mensagens da conversa
historico = [
    {
        "role": "system",
        "content": (
            f"Seu nome e {nome}. "
            "Voce e um assistente virtual educado, "
            "prestativo e objetivo. "
            "Responda em portugues brasileiro e "
            "explique assuntos de forma clara."
        )
    }
]

# Mantem a conversa ativa
while True:
    mensagem = input("Voce: ").strip()

    if not mensagem:
        continue

    if mensagem.lower() == "sair":
        print(f"{nome}: Ate logo!")
        break

    # Adiciona a mensagem do usuario ao historico
    historico.append({
        "role": "user",
        "content": mensagem
    })

    try:
        # Envia a conversa para a API
        resposta = cliente.chat.completions.create(
            model=MODEL,
            messages=historico
        )

        # Recupera o texto da resposta
        texto = resposta.choices[0].message.content

        if not texto:
            texto = "Nao consegui gerar uma resposta."

        # Exibe a resposta na interface de texto
        print(f"\n{nome}: {texto}\n")

        # Guarda a resposta para manter o contexto
        historico.append({
            "role": "assistant",
            "content": texto
        })

    except Exception as erro:
        print("\nNao foi possivel obter uma resposta da API.")
        print("Verifique a internet, a chave e a disponibilidade.")
        print("Detalhe do erro:", erro, "\n")

        # Retira a mensagem que falhou do historico
        historico.pop()
