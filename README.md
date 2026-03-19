# DocDev IA

O **DocDev IA** é um sistema web simples desenvolvido com **Flask** que utiliza Inteligência Artificial para ajudar desenvolvedores iniciante a:

- explicar trechos de código
- gerar documentação técnica resumida
- gerar comentários no código
- sugerir melhorias simples

Além disso, o sistema salva o histórico das análises em um banco local **SQLite**.

---

# O que o sistema faz

Na prática, o usuário:

1. escolhe o provedor de IA
2. escolhe a linguagem do código
3. escolhe a ação desejada
4. cola um trecho de código
5. envia para processamento
6. visualiza a resposta na tela
7. pode consultar o histórico posteriormente

---

# Funcionalidades

O sistema possui as seguintes funcionalidades:

- escolha do provedor de IA diretamente na interface
- destaque visual do tipo de custo do provedor
- seleção da linguagem do código
- seleção da ação desejada
- envio do trecho para o provedor selecionado
- exibição da resposta na tela
- histórico local das análises realizadas
- armazenamento em SQLite
- configuração centralizada por arquivo `.env`

---

# Provedores de IA suportados

O sistema foi programado para funcionar com quatro provedores:

- **Ollama Local**
- **Gemini API**
- **Groq API**
- **OpenAI API**

## Classificação de custo exibida na interface

Na tela inicial, cada provedor aparece com um marcador visual de custo:

- **Gratuito**
- **Gratuito com limites**
- **Pago**

## Como cada um aparece no sistema

### 1. Ollama Local
- exibido como: **Gratuito**
- não utiliza chave para uso local
- exige que o Ollama esteja instalado e rodando no computador

### 2. Gemini API
- exibido como: **Gratuito com limites**
- exige chave da API
- depende de cota/limites do provedor

### 3. Groq API
- exibido como: **Gratuito com limites**
- exige chave da API
- depende de cota/limites do provedor

### 4. OpenAI API
- exibido como: **Pago**
- exige chave da API
- o uso da API é separado do ChatGPT

---

# Como a escolha do provedor funciona

O usuário escolhe o provedor na interface.

Com base nessa escolha, o backend chama automaticamente a função correta:

- `call_ollama(prompt)` para Ollama
- `call_gemini(prompt)` para Gemini
- `call_groq(prompt)` para GroK
- `call_openai(prompt)` para OpenAI

Isso significa que **não é necessário alterar o código para trocar de IA**.

Basta:

1. configurar o `.env`
2. iniciar o sistema
3. escolher a IA desejada na interface

---

# Ações disponíveis

O sistema possui quatro ações principais:

## 1. Explicar código
A IA explica o trecho de código de forma clara e objetiva, informando o que ele faz, entradas, saídas e lógica principal.

## 2. Gerar documentação
A IA gera uma documentação técnica curta para o trecho informado.

## 3. Gerar comentários
A IA reescreve o trecho adicionando comentários úteis sem alterar a lógica.

## 4. Sugerir melhorias
A IA analisa o código e sugere melhorias simples de organização, legibilidade, validação e boas práticas.

---

# Tecnologias utilizadas

## Backend
- Python
- Flask
- Requests
- python-dotenv
- SQLite

## Frontend
- HTML
- CSS

---

# Estrutura do projeto

```text
docdev_ia/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   └── history.html
│
└── static/
    └── style.css
```

---

# Descrição dos arquivos principais

## `app.py`
Arquivo principal do sistema.

Responsável por:

- iniciar o Flask
- carregar o `.env`
- criar e acessar o banco SQLite
- montar os prompts
- escolher o provedor correto
- processar as requisições
- salvar o histórico
- renderizar as páginas HTML

## `templates/index.html`
Tela principal do sistema.

Responsável por:

- mostrar os provedores disponíveis
- destacar custo por cor
- exibir formulário de linguagem, ação e código
- mostrar a resposta gerada

## `templates/history.html`
Tela de histórico.

Responsável por:

- exibir as análises já feitas
- mostrar o provedor usado
- mostrar a linguagem, ação, código, resposta e data

## `static/style.css`
Arquivo de estilo da interface.

Responsável por:

- layout visual
- cores dos cards dos provedores
- badges de custo
- estilo do formulário
- estilo do histórico

## `.env`
Arquivo real de configuração local.

Responsável por:

- armazenar as chaves de API
- armazenar nomes de modelos
- armazenar URL e modelo do Ollama local
- definir configurações do Flask

## `.env.example`
Arquivo opcional de exemplo.

Serve apenas como modelo para o repositório e para mostrar quais variáveis precisam existir.

## `database.db`
Arquivo criado automaticamente pelo sistema.

Guarda o histórico das análises realizadas.

---

# Banco de dados

O sistema usa **SQLite** e cria automaticamente o arquivo:

```text
database.db
```

## Tabela usada
A tabela principal é `history`.

## Dados armazenados
Cada registro salva:

- `provider`
- `language`
- `action`
- `code`
- `response`
- `created_at`

## Observação importante
Se o banco já existir de uma versão anterior e ainda não tiver a coluna `provider`, o próprio sistema tenta ajustar a estrutura automaticamente ao iniciar.

---

# Requisitos para executar

Antes de rodar o sistema, você precisa ter instalado:

- Python 3
- VS Code ou outro editor
- pip
- acesso à internet para APIs remotas
- Ollama instalado, caso queira usar IA local

---

# Instalação do projeto

## 1. Criar a pasta do projeto

Crie a pasta:

```text
docdev_ia
```

Abra essa pasta no VS Code.

---

## 2. Criar o ambiente virtual

No terminal do VS Code:

### PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### CMD
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

## Se o PowerShell bloquear a ativação
Execute:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Depois ative novamente a `.venv`.

---

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## Conteúdo esperado de `requirements.txt`

```text
Flask
requests
python-dotenv
```

---

# Configuração do arquivo `.env`

O sistema usa **um único arquivo `.env` real**.

Você não precisa criar vários arquivos de ambiente.

## Exemplo completo de `.env`

```env
FLASK_SECRET_KEY=uma_chave_local_simples
FLASK_DEBUG=1

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

## Como usar esse `.env`
Você **não precisa preencher tudo**.

Preencha apenas o que pretende usar.

### Exemplo: usar só Ollama
```env
FLASK_SECRET_KEY=uma_chave_local_simples
FLASK_DEBUG=1

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

### Exemplo: usar Ollama e Gemini
```env
FLASK_SECRET_KEY=uma_chave_local_simples
FLASK_DEBUG=1

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=sua_chave_gemini_aqui
GEMINI_MODEL=gemini-2.5-flash

GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

### Exemplo: usar OpenAI
```env
FLASK_SECRET_KEY=uma_chave_local_simples
FLASK_DEBUG=1

OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

---

# Como rodar o sistema

Com a `.venv` ativada, execute:

```bash
python app.py
```

Se estiver tudo certo, aparecerá algo parecido com:

```text
* Running on http://127.0.0.1:5000
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

---

# Como usar o sistema na prática

## 1. Abrir o sistema
Abra o navegador em:

```text
http://127.0.0.1:5000
```

## 2. Escolher o provedor de IA
Na tela inicial, selecione um dos cards:

- Ollama Local
- Gemini API
- Groq API
- OpenAI API

## 3. Observar o tipo de custo
A interface destaca o custo do provedor por cor:

- verde = gratuito
- amarelo/laranja = gratuito com limites
- vermelho = pago

## 4. Escolher a linguagem
Selecione a linguagem correspondente ao código.

Opções da interface:

- Python
- JavaScript
- Java
- C
- C++
- HTML
- CSS
- SQL

## 5. Escolher a ação
Selecione o que deseja fazer:

- Explicar código
- Gerar documentação
- Gerar comentários
- Sugerir melhorias

## 6. Colar o código
Cole o trecho na área de texto.

## 7. Clicar em `Processar`
O sistema enviará o conteúdo ao provedor escolhido.

## 8. Ler a resposta
A resposta será exibida abaixo do formulário.

## 9. Consultar o histórico
Clique em **Ver histórico** ou acesse:

```text
http://127.0.0.1:5000/history
```

---

# Como usar o Ollama Local

O sistema possui suporte ao **Ollama Local** como opção de IA gratuita.

## Importante

Nesta versão do projeto, o sistema **permite escolher o Ollama na interface**, mas **não inicia o Ollama automaticamente**.

Isso significa que, antes de usar a opção **Ollama Local** no sistema, você precisa:

1. instalar o Ollama no computador
2. iniciar o Ollama localmente
3. baixar o modelo que será usado
4. só então abrir o sistema Flask e escolher **Ollama Local**

---

## O que o sistema espera no `.env`

O código atual usa estas variáveis para o Ollama:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

Isso significa que:

- o sistema tentará acessar o Ollama local em `http://localhost:11434`
- o modelo esperado por padrão é `llama3.2:3b`

---

## Como instalar o Ollama no Windows

A forma mais simples é:

1. acessar o site oficial do Ollama
2. baixar o instalador para Windows
3. executar o instalador
4. concluir a instalação normalmente

Depois da instalação, o comando `ollama` deve ficar disponível no terminal.

---

## Como abrir o Ollama pelo terminal

Depois de instalar, abra um terminal e rode:

```bash
ollama
```

Esse comando abre o menu interativo do Ollama.

Se você quiser iniciar o servidor local explicitamente pelo terminal, use:

```bash
ollama serve
```

Esse comando é útil para garantir que a API local do Ollama esteja ativa para o seu sistema Flask.

---

## Como baixar o modelo que o sistema usa

O projeto está configurado para usar o modelo:

```text
llama3.2:3b
```

Para baixar esse modelo, use:

```bash
ollama pull llama3.2:3b
```

Esse download normalmente precisa ser feito apenas uma vez.

---

## Como listar os modelos instalados

Para verificar se o modelo foi baixado corretamente:

```bash
ollama ls
```

Se o modelo `llama3.2:3b` aparecer na lista, ele já está disponível para uso no sistema.

---

## Fluxo completo para usar Ollama com este projeto

Siga esta ordem:

### 1. Instalar o Ollama
Instale o Ollama no Windows.

### 2. Abrir o Ollama
No terminal, rode:

```bash
ollama serve
```

Se preferir, você também pode usar:

```bash
ollama
```

### 3. Baixar o modelo padrão
```bash
ollama pull llama3.2:3b
```

### 4. Confirmar se o modelo está disponível
```bash
ollama ls
```

### 5. Conferir o `.env`
Verifique se o seu `.env` está assim:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

### 6. Rodar o sistema Flask
Dentro da pasta do projeto:

```bash
python app.py
```

### 7. Abrir o navegador
Abra:

```text
http://127.0.0.1:5000
```

### 8. Escolher o provedor na interface
Na tela inicial do sistema:

- selecione **Ollama Local**
- escolha a linguagem
- escolha a ação
- cole o código
- clique em **Processar**

---

## Exemplo de teste com Ollama

Cole este código no sistema:

```python
def calcular_total(preco, quantidade):
    return preco * quantidade
```

Depois escolha:

- provedor: **Ollama Local**
- linguagem: **Python**
- ação: **Explicar código**

Clique em **Processar**.

---

## Problemas comuns com Ollama

### 1. Erro de conexão com Ollama
Isso normalmente significa que o Ollama não está rodando.

Tente rodar:

```bash
ollama serve
```

### 2. Modelo não encontrado
Isso significa que o modelo definido no `.env` ainda não foi baixado.

Baixe com:

```bash
ollama pull llama3.2:3b
```

### 3. O sistema abre, mas não responde com Ollama
Verifique:

- se o Ollama está instalado
- se o Ollama está rodando
- se o modelo foi baixado
- se o `.env` está apontando para:
  - `OLLAMA_BASE_URL=http://localhost:11434`
  - `OLLAMA_MODEL=llama3.2:3b`

---

# Como usar o Gemini API

## O que precisa
- chave da API do Gemini

## Configuração no `.env`

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## Fluxo de uso

1. gere a chave do Gemini
2. preencha o `.env`
3. rode `python app.py`
4. escolha **Gemini API** na interface

---

# Como usar o Groq API

## O que precisa
- chave da API da Groq

## Configuração no `.env`

```env
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=llama-3.1-8b-instant
```

## Fluxo de uso

1. gere a chave da Groq
2. preencha o `.env`
3. rode `python app.py`
4. escolha **Groq API** na interface

---

# Como usar o OpenAI API

## O que precisa
- chave da API da OpenAI

## Configuração no `.env`

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

## Fluxo de uso

1. gere a chave da OpenAI
2. preencha o `.env`
3. rode `python app.py`
4. escolha **OpenAI API** na interface

---

# Exemplo de teste rápido

Use este código:

```python
def calcular_total(preco, quantidade):
    return preco * quantidade
```

Na interface:

- provedor: escolha qualquer um configurado
- linguagem: `Python`
- ação: `Explicar código`

Clique em **Processar**.

---

# Comportamento do sistema em caso de erro

## Se faltar chave
Se você escolher um provedor que depende de chave e ela não estiver configurada, o sistema mostrará uma mensagem de erro clara na interface.

Exemplos:

- `OPENAI_API_KEY não configurada no arquivo .env.`
- `GEMINI_API_KEY não configurada no arquivo .env.`
- `GROQ_API_KEY não configurada no arquivo .env.`

## Se o Ollama não estiver rodando
O sistema mostrará erro de conexão com o Ollama local.

## Se o provedor retornar erro de API
A mensagem também será exibida na interface, incluindo o nome do provedor e detalhes quando disponíveis.

---

# Erros comuns e soluções

## 1. O sistema não inicia
Verifique:

- se a `.venv` foi ativada
- se as dependências foram instaladas
- se o `app.py` está na raiz do projeto

## 2. O navegador abre, mas a IA não responde
Verifique:

- se o provedor escolhido foi configurado no `.env`
- se a chave está preenchida corretamente
- se o Flask foi reiniciado após alterar o `.env`

## 3. Ollama não conecta
Verifique:

- se o Ollama está instalado
- se o Ollama está aberto
- se o modelo existe localmente
- se `OLLAMA_BASE_URL` está correto
- se `OLLAMA_MODEL` corresponde a um modelo instalado

## 4. Erro ao usar Gemini, Groq ou OpenAI
Verifique:

- se a chave foi copiada corretamente
- se não há espaços extras
- se a conta do provedor está ativa
- se o modelo configurado existe para aquele provedor

## 5. Histórico não aparece
Verifique:

- se o `database.db` foi criado
- se a requisição chegou a ser processada com sucesso
- se você está acessando `/history`

---

# Histórico de uso

O histórico pode ser acessado em:

```text
http://127.0.0.1:5000/history
```

Cada item mostra:

- ID
- provedor
- linguagem
- ação
- data
- código enviado
- resposta gerada

---

# Segurança

## O que fazer
- manter as chaves no `.env`
- usar `.gitignore`
- subir para o GitHub apenas o `.env.example`

## O que não fazer
- não colocar chaves dentro do `app.py`
- não enviar o `.env` para o GitHub
- não compartilhar chaves em prints ou documentação pública

---

# Limitações atuais do projeto

Esta versão é propositalmente simples e possui algumas limitações:

- trabalha com trecho colado manualmente
- não faz upload de arquivos
- não faz autenticação de usuários
- não gera PDF
- não integra com GitHub automaticamente
- não interpreta projetos inteiros, apenas o trecho informado
- não inicia o Ollama automaticamente pela interface

---

# Melhorias futuras sugeridas

Algumas melhorias que podem ser implementadas depois:

- botão para verificar status do Ollama
- botão para iniciar Ollama pela interface
- upload de arquivos `.py`, `.js`, `.java`
- filtros no histórico
- exportação para PDF
- autenticação de usuários
- geração automática de README
- integração com GitHub
- suporte a mais linguagens
- opção de limpar histórico

---

# Autor

Thiago N Barros