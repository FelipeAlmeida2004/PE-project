# PE-project
projeto de probabilidade e estatística referente as notas do ENEM 

## Instruções

### Pré-requisitos
- Python 3.12 ou superior
- Poetry (gerenciador de dependências do Python)

### 1. Instalação do Poetry

Caso não tenha Poetry instalado:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Configuração do Ambiente Virtual

No diretório raiz do projeto, execute:
```bash
poetry install
```

Isso criará um ambiente virtual e instalará todas as dependências listadas no `pyproject.toml`.

### 3. Configuração do Arquivo `.env.example`

Crie o arquivo `.env` como manda o arquivo `.env.example` (já existe no projeto) e modifique o valor das variavéis conforme o caminho do arquivo em seu dispositivo:
```
PATH_DICT=database/2024/DICIONÁRIO/Dicionário_Microdados_Enem_2024.xlsx
SHEET_NAME=PARTICIPANTES_2024,RESULTADOS_2024
```

Ajuste os caminhos e sheet names conforme necessário.

### 4. Executando o Projeto

Para executar o script principal:
```bash
poetry run python src/main_exec.py
```

Ou ative o shell do Poetry e execute sem o prefixo:
```bash
poetry shell
python src/main_exec.py
```

### 5. Estrutura do Projeto

```
.
├── src/                          # Código fonte
│   ├── __init__.py
│   ├── config.py               # Configurações do projeto
│   ├── dict_data_collect.py    # Coletor de dicionários de dados
│   └── main_exec.py            # Script principal de execução
├── database/                     # Base de dados (ignorado no Git)
│   └── 2024/
│       ├── DADOS/              # Dados em CSV
│       ├── DICIONÁRIO/         # Dicionários em Excel
│       ├── INPUTS/             # Scripts de importação (R, SAS, SPSS)
│       ├── LEIA-ME E DOCUMENTOS TÉCNICOS/
│       └── PROVAS E GABARITOS/
├── pyproject.toml              # Configuração do Poetry
├── poetry.lock                 # Lock file de dependências
├── .env                        # Variáveis de ambiente
├── .gitignore                  # Configuração Git
└── README.md                   # Este arquivo
```

### 6. Dependências Principais

- **pandas**: Manipulação e análise de dados
- **openpyxl**: Leitura de arquivos Excel (.xlsx)
- **python-dotenv**: Carregamento de variáveis de ambiente

### Troubleshooting

**Erro: "pandas não encontrado"**
- Execute: `poetry install`

**Erro: "openpyxl não encontrado"**
- Execute: `poetry install`

**Erro: "Arquivo não encontrado"**
- Verifique os caminhos no arquivo `.env`
