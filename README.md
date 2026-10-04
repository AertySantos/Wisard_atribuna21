# Classificador WiSARD — Jornal A Tribuna (TF-IDF + termômetro)

Classificação de páginas do jornal **A Tribuna** por editoria usando uma rede neural sem peso
**WiSARD** (`wisardpkg`). O notebook principal é o [`wisard0.ipynb`](wisard0.ipynb).

O pipeline é:

1. **Pré-processamento** (`__init__.py`): conta as palavras de cada documento (removendo stopwords,
   acentos e reduzindo ao radical), monta o vocabulário com o IDF de cada termo e gera um CSV por classe
   com os pesos TF-IDF (`idf × (1 + ln(tf))`).
2. **Classificação** (`wisard0.ipynb`):
   - lê os CSVs como matriz esparsa;
   - divide em treino/teste (80% / 20%);
   - seleciona os `K_TERMOS` termos mais relevantes com **chi²** (calculado só no treino);
   - binariza os pesos com um **termômetro** de `BITS_TERMOMETRO` bits por termo;
   - treina e classifica com a **WiSARD**;
   - mostra acurácia, precisão, recall, F1 (micro e macro), relatório por classe e matriz de confusão.

---

## Requisitos

- **Python 3.8+**
- **Compilador C++** (`g++`) e headers do Python — o `wisardpkg` é uma extensão C++ e, dependendo da
  versão do Python, é compilado na instalação
- **Jupyter** (ou VS Code com a extensão Jupyter) para rodar o notebook
- **Memória**: recomenda-se pelo menos 8 GB de RAM. A entrada binária da WiSARD tem
  `K_TERMOS × BITS_TERMOMETRO` bits por documento (7000 × 8 = 56 000 por padrão); se faltar memória,
  reduza `K_TERMOS` ou `BITS_TERMOMETRO`.

### Bibliotecas Python

| Biblioteca | Usada em | Para quê |
|---|---|---|
| `numpy` | ambos | vetores e matrizes |
| `scipy` | notebook | matriz esparsa |
| `scikit-learn` | notebook | divisão treino/teste, chi², métricas |
| `wisardpkg` | notebook | rede WiSARD |
| `spacy` + modelo `pt_core_news_sm` | `__init__.py` | processamento do português |
| `jupyter` / `ipykernel` | notebook | executar o `.ipynb` |

---

## Instalação

### 1. Dependências do sistema (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-dev build-essential
```

### 2. Ambiente virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Pacotes Python

```bash
pip install --upgrade pip
pip install numpy scipy scikit-learn spacy wisardpkg jupyter ipykernel
python3 -m spacy download pt_core_news_sm
```

Para conferir se a WiSARD foi instalada:

```bash
python3 -c "import wisardpkg; print('wisardpkg OK')"
```

---

## Dataset

Baixe o dataset **aTribuna-21dir** pelo Google Drive:

**https://drive.google.com/file/d/1dZd3guCdfE2U_j_ENBhR63QcGe8JyZAt/view?usp=sharing**

Extraia o arquivo na **raiz do projeto**, de modo que fique assim:

```
Classificador_Atribuna21/
├── aTribuna-21dir/
│   ├── at2/            # um .txt por página do jornal
│   ├── eco/
│   ├── esp/
│   └── ...
├── classes.txt
├── portuguese
├── __init__.py
└── wisard0.ipynb
```

Se o arquivo baixado for um `.tar.gz`:

```bash
tar -xzf aTribuna-21dir.tar.gz
```

Também é possível baixar pela linha de comando com o `gdown`:

```bash
pip install gdown
gdown 1dZd3guCdfE2U_j_ENBhR63QcGe8JyZAt
```

### Classes usadas

O arquivo [`classes.txt`](classes.txt) define quais pastas (classes) do dataset são processadas, uma por
linha. Por padrão:

```
aTribuna-21dir/at2
aTribuna-21dir/eco
aTribuna-21dir/esp
```

Para usar outras editorias, adicione as pastas correspondentes nesse arquivo antes do pré-processamento.

---

## Como executar

### Passo 1 — Pré-processamento (gera os CSVs)

Rode o `__init__.py` **três vezes**, escolhendo no menu as opções **1**, **2** e **3**, nessa ordem:

```bash
python3 __init__.py   # opção 1: contagem de palavras  -> frequencia/
python3 __init__.py   # opção 2: vocabulário e IDF      -> arq_fi/fi.txt
python3 __init__.py   # opção 3: pesos TF-IDF           -> csv/aTribuna-21dir/<classe>.csv
```

| Opção | Gera | Descrição |
|---|---|---|
| 1 | `frequencia/aTribuna-21dir/<classe>/` | frequência das palavras de cada documento |
| 2 | `arq_fi/fi.txt` | termos do vocabulário e seus IDFs |
| 3 | `csv/aTribuna-21dir/<classe>.csv` | um documento por linha: classe + pesos TF-IDF |

O corte do vocabulário na opção 2 é controlado pelas constantes `MIN_DOCS` e `MAX_PROP_DOCS` no início do
`__init__.py`. Se alterá-las, rode as opções 2 e 3 novamente.

> Os arquivos `portuguese` (lista de stopwords) e `classes.txt` precisam estar na raiz do projeto.

### Passo 2 — Classificação com a WiSARD

```bash
jupyter notebook wisard0.ipynb
```

Execute as células em ordem (*Run All*). No VS Code, abra o `wisard0.ipynb` e selecione o kernel do
ambiente virtual criado acima.

---

## Parâmetros do notebook

Definidos na primeira célula de código do `wisard0.ipynb`:

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `pasta_dados` | `csv/aTribuna-21dir/` | pasta com os CSVs gerados pela opção 3 |
| `arquivo_fi` | `arq_fi/fi.txt` | vocabulário (usado só para exibir os nomes dos termos) |
| `K_TERMOS` | `7000` | quantidade de termos mantidos pela seleção chi² |
| `BITS_TERMOMETRO` | `8` | bits do termômetro por termo |
| `ENDERECAMENTO` | `5` | bits de endereçamento de cada RAM da WiSARD |

Dicas de ajuste:

- **`K_TERMOS`**: menos termos = entrada menor e mais rápida, mas pode perder informação (teste 1000, 3000, 5000).
- **`BITS_TERMOMETRO`**: mais bits = mais resolução do peso, porém mais memória e tempo (teste 4, 8, 16).
- **`ENDERECAMENTO`**: valores maiores deixam a rede mais específica (memoriza mais, generaliza menos);
  menores generalizam mais, mas podem saturar as RAMs. Valores comuns ficam entre 4 e 32.

---

## Problemas comuns

| Erro | Solução |
|---|---|
| `ModuleNotFoundError: No module named 'wisardpkg'` | `pip install wisardpkg` no mesmo ambiente do kernel do Jupyter |
| Falha ao compilar o `wisardpkg` | instale `build-essential` e `python3-dev` (passo 1 da instalação) |
| `OSError: [E050] Can't find model 'pt_core_news_sm'` | `python3 -m spacy download pt_core_news_sm` |
| `FileNotFoundError: csv/aTribuna-21dir/` | rode as opções 1, 2 e 3 do `__init__.py` antes do notebook |
| `FileNotFoundError: frequencia/...` | o dataset não foi extraído na raiz do projeto ou `classes.txt` aponta para pastas inexistentes |
| Kernel morre / `MemoryError` | reduza `K_TERMOS` ou `BITS_TERMOMETRO` |
