import os
import sqlite3
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

DB_NAME = "database.db"

PROVIDERS = {
    "ollama": {
        "label": "Ollama Local",
        "cost_label": "Gratuito",
        "cost_class": "free",
        "description": "Roda no seu computador e não exige chave para uso local.",
        "key_hint": "Sem chave local",
    },
    "gemini": {
        "label": "Gemini API",
        "cost_label": "Gratuito com limites",
        "cost_class": "free-limited",
        "description": "Boa opção para testes e pequenos projetos.",
        "key_hint": "Usa GEMINI_API_KEY",
    },
    "Grok": {
        "label": "Grok API",
        "cost_label": "Gratuito com limites",
        "cost_class": "free-limited",
        "description": "API rápida para inferência com free tier.",
        "key_hint": "Usa Grok_API_KEY",
    },
    "openai": {
        "label": "OpenAI API",
        "cost_label": "Pago",
        "cost_class": "paid",
        "description": "Integração paga, separada do ChatGPT.",
        "key_hint": "Usa OPENAI_API_KEY",
    },
}


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_history_schema():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT NOT NULL DEFAULT 'ollama',
            language TEXT NOT NULL,
            action TEXT NOT NULL,
            code TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = [row["name"] for row in conn.execute("PRAGMA table_info(history)").fetchall()]

    if "provider" not in columns:
        conn.execute("ALTER TABLE history ADD COLUMN provider TEXT NOT NULL DEFAULT 'ollama'")

    conn.commit()
    conn.close()


def save_history(provider, language, action, code, response_text):
    conn = get_connection()
    conn.execute("""
        INSERT INTO history (provider, language, action, code, response)
        VALUES (?, ?, ?, ?, ?)
    """, (provider, language, action, code, response_text))
    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM history
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows


def build_prompt(language, action, code):
    instructions = {
        "explain": (
            "Explique o código abaixo de forma clara, simples e didática. "
            "Diga o que ele faz, entradas, saídas e lógica principal."
        ),
        "document": (
            "Gere uma documentação técnica curta para o código abaixo. "
            "Inclua objetivo, parâmetros, retorno e observações."
        ),
        "comment": (
            "Reescreva o código abaixo adicionando comentários úteis, "
            "sem mudar a lógica."
        ),
        "improve": (
            "Analise o código abaixo e sugira melhorias simples de "
            "legibilidade, organização, validação e boas práticas."
        ),
    }

    instruction = instructions.get(action, instructions["explain"])

    return (
        f"Linguagem: {language}\n\n"
        f"{instruction}\n\n"
        f"Código:\n{code}"
    )


def extract_openai_response_text(data):
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    texts = []

    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                text = content.get("text", "")
                if isinstance(text, str) and text.strip():
                    texts.append(text.strip())

    if texts:
        return "\n\n".join(texts)

    raise RuntimeError(f"Formato de resposta inesperado da OpenAI: {data}")


def call_openai(prompt):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    url = "https://api.openai.com/v1/responses"

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada no arquivo .env.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "input": prompt,
        "instructions": (
            "Você é um assistente para desenvolvedores. "
            "Responda em português do Brasil, de forma clara e objetiva."
        ),
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao conectar com a OpenAI: {e}")

    try:
        data = response.json()
    except ValueError:
        data = None

    if response.status_code >= 400:
        message = "Erro desconhecido na OpenAI."
        if isinstance(data, dict):
            message = data.get("error", {}).get("message", message)
        raise RuntimeError(f"OpenAI ({response.status_code}): {message}")

    if not isinstance(data, dict):
        raise RuntimeError("A OpenAI retornou uma resposta inválida.")

    return extract_openai_response_text(data)


def call_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada no arquivo .env.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao conectar com o Gemini: {e}")

    try:
        data = response.json()
    except ValueError:
        data = None

    if response.status_code >= 400:
        message = "Erro desconhecido no Gemini."
        if isinstance(data, dict):
            message = data.get("error", {}).get("message", message)
        raise RuntimeError(f"Gemini ({response.status_code}): {message}")

    if not isinstance(data, dict):
        raise RuntimeError("O Gemini retornou uma resposta inválida.")

    candidates = data.get("candidates", [])
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        texts = [part.get("text", "").strip() for part in parts if part.get("text", "").strip()]
        if texts:
            return "\n\n".join(texts)

    block_reason = data.get("promptFeedback", {}).get("blockReason")
    if block_reason:
        raise RuntimeError(f"Resposta bloqueada pelo Gemini: {block_reason}")

    raise RuntimeError(f"Formato de resposta inesperado do Gemini: {data}")


def call_Grok(prompt):
    api_key = os.getenv("Grok_API_KEY", "").strip()
    model = os.getenv("Grok_MODEL", "llama-3.1-8b-instant").strip()
    url = "https://api.Grok.com/openai/v1/chat/completions"

    if not api_key:
        raise RuntimeError("Grok_API_KEY não configurada no arquivo .env.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um assistente para desenvolvedores. "
                    "Responda em português do Brasil, de forma clara e objetiva."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao conectar com o Grok: {e}")

    try:
        data = response.json()
    except ValueError:
        data = None

    if response.status_code >= 400:
        message = "Erro desconhecido no Grok."
        if isinstance(data, dict):
            message = data.get("error", {}).get("message", message)
        raise RuntimeError(f"Grok ({response.status_code}): {message}")

    if not isinstance(data, dict):
        raise RuntimeError("O Grok retornou uma resposta inválida.")

    try:
        content = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Formato de resposta inesperado do Grok: {data}")

    if not content:
        raise RuntimeError("O Grok retornou uma resposta vazia.")

    return content


def call_ollama(prompt):
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b").strip()
    url = f"{base_url}/api/generate"

    payload = {
        "model": model,
        "prompt": (
            "Você é um assistente para desenvolvedores. "
            "Responda em português do Brasil, de forma clara e objetiva.\n\n"
            f"{prompt}"
        ),
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
    except requests.RequestException as e:
        raise RuntimeError(
            "Erro ao conectar com o Ollama local. "
            "Verifique se o Ollama está instalado, aberto e executando. "
            f"Detalhes: {e}"
        )

    try:
        data = response.json()
    except ValueError:
        data = None

    if response.status_code >= 400:
        message = "Erro desconhecido no Ollama."
        if isinstance(data, dict):
            message = data.get("error", message)
        raise RuntimeError(f"Ollama ({response.status_code}): {message}")

    if not isinstance(data, dict):
        raise RuntimeError("O Ollama retornou uma resposta inválida.")

    content = data.get("response", "").strip()
    if not content:
        raise RuntimeError(f"Formato de resposta inesperado do Ollama: {data}")

    return content


def generate_with_provider(provider, prompt):
    if provider == "ollama":
        return call_ollama(prompt)
    if provider == "gemini":
        return call_gemini(prompt)
    if provider == "Grok":
        return call_Grok(prompt)
    if provider == "openai":
        return call_openai(prompt)

    raise RuntimeError("Provedor de IA inválido.")


ensure_history_schema()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    provider = "ollama"
    language = ""
    action = ""
    code = ""

    if request.method == "POST":
        provider = request.form.get("provider", "ollama").strip().lower()
        language = request.form.get("language", "").strip()
        action = request.form.get("action", "").strip()
        code = request.form.get("code", "").strip()

        if provider not in PROVIDERS:
            flash("Selecione um provedor válido.", "error")
            provider = "ollama"

        elif not language or not action or not code:
            flash("Preencha todos os campos.", "error")

        else:
            try:
                prompt = build_prompt(language, action, code)
                result = generate_with_provider(provider, prompt)
                save_history(provider, language, action, code, result)
            except Exception as e:
                flash(str(e), "error")

    return render_template(
        "index.html",
        providers=PROVIDERS,
        result=result,
        provider=provider,
        language=language,
        action=action,
        code=code
    )


@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records, providers=PROVIDERS)


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug_mode)