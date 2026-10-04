import os
from collections import defaultdict
import string
import math
import sys
import numpy as np
import spacy
import unicodedata
import re
from collections import Counter
# Dicionário para armazenar a frequência de palavras por arquivo
frequencia_palavras = defaultdict(lambda: defaultdict(int))
qtd_docs = 0
consulta = []
discriminante = 0
# Lista de stop words
stop_words = []

# Corte do vocabulario na opcao 2 (frequencia de documento):
# termo precisa aparecer em pelo menos MIN_DOCS documentos
MIN_DOCS = 5
# e em no maximo MAX_PROP_DOCS da colecao (0.5 = metade dos documentos)
MAX_PROP_DOCS = 0.5

# Carregue o modelo do spaCy para o português
nlp = spacy.load("pt_core_news_sm")


def extrair_radical(palavra):
    # Processa a palavra com o spaCy
    doc = nlp(palavra)

    # Extraia o lema (forma básica)
    lema = doc[0].lemma_

    return lema


def letras_indesejadas(string):
    # Use uma expressão regular para encontrar caracteres que não são letras do alfabeto português
    padrao = re.compile(r'[^a-zA-ZàáâãçéêíóôõúÀÁÂÃÇÉÊÍÓÔÕÚ]')

    # Use a função findall para encontrar todas as correspondências
    caracteres_nao_portugueses = padrao.findall(string)

    # Retorna a lista de caracteres não portugueses
    return caracteres_nao_portugueses


def remover_acentos(texto):
    return ''.join([c for c in unicodedata.normalize('NFD', texto) if not unicodedata.combining(c)])


def stops():
    global stop_words
    with open("portuguese", "r", encoding="iso-8859-1") as arquivo:
        texto = arquivo.read().lower()
        texto_sem_pontuacao = texto.translate(
            str.maketrans('', '', string.punctuation))
        # Divide o texto em palavras (separadas por espaço em branco)
        palavras = texto_sem_pontuacao.split()

        for palavra in palavras:
            stop_words.append(palavra)


def consultar(entrada):
    global consulta
    v2 = []

    print(entrada)
    entrada_l = entrada.lower()
    # Divide o texto em palavras (separadas por espaço em branco)
    palavras = entrada_l.split()

    with open("arq_fi/fi.txt", 'r') as file:
        for linha in file:
            partes = linha.split(":")
            if len(partes) == 2:
                chave = partes[0].strip()
                valor = partes[1].strip()
                if chave in palavras:
                  #  print(chave)
                    # mudar depois quantidade de palavras
                    ponderacao = round(float(valor)*(1 + math.log(1)), 2)
                    v2.append(ponderacao)
                else:
                    v2.append(0)
    consulta = v2


def dez_menos_sim(caminho, pasta):
    teste = 1


def busca_frequencia(arquivo, palavra):

    with open(arquivo, 'r') as file:
        for linha in file:
            partes = linha.split(":")
            if len(partes) == 2:
                chave = partes[0].strip()
                valor = partes[1].strip()
                if chave == palavra:
                    if valor.isnumeric():
                        return int(valor)
                    else:
                        return valor
    # Se a palavra não for encontrada no arquivo
    return 0


def busca_frequencia_mod(arquivo, palavra):

    for linha in arquivo:
        partes = linha.split(":")
        if len(partes) == 2:
            chave = partes[0]
            # print(chave)
            chave = remover_acentos(chave)
            pletra = chave[0]
            valor = float(partes[1].strip())
            tam = len(chave)

            if not chave.isdigit():
                # print(chave)
                lema = extrair_radical(chave).lower()
                # print(lema)

                if lema == palavra:
                    print(f"{chave} : {palavra}")
                    return valor
    return 0


def carregar_freq_inv(arquivo):
    termos = []
    idfs = []
    with open(arquivo, 'r', encoding='iso-8859-1') as file:
        for linha in file:
            partes = linha.split(":")
            if len(partes) == 2:
                termos.append(partes[0].strip())
                idfs.append(float(partes[1].strip()))
    return termos, idfs


def ordenar_por_frequencia():
    # Loop sobre os arquivos e palavras
    for nome_arquivo, palavras in frequencia_palavras.items():
        # Ordenar o dicionário por frequência e atribuir de volta à variável
        frequencia_palavras[nome_arquivo] = dict(
            sorted(palavras.items(), key=lambda item: item[1], reverse=True))


def calcular(arq1, arq2):
    vet1 = txt_vetor(arq1)
    vet2 = txt_vetor(arq2)
    numerador = 0
    resultado = 0
    d1 = 0
    d2 = 0

    for i in range(len(vet1)):
        numerador += round(float(vet2[i]) * float(vet1[i]), 2)
        d1 += pow(float(vet2[i]), 2)
        d2 += pow(float(vet1[i]), 2)

    d3 = round(math.sqrt(d1) * math.sqrt(d2), 2)

    if d3 > 0:
        resultado = round(numerador / d3, 2)
    else:
        resultado = 0

    return resultado


def somar(vet1, arq2):

    vet2 = txt_vetor(arq2)
    vetor = []

    for i in range(len(vet1)):
        vetor.append(int(vet2[i]) + int(vet1[i]))

    return vetor


def txt_vetor(arq1):

    vetor = []

    nome_arquivo = os.path.basename(arq1)  # Obtém o nome do arquivo
    # Salva as frequências de palavras em arquivos
    caminho = os.path.join("arq_pesos", nome_arquivo)

    with open(arq1, 'r', encoding='iso-8859-1') as file:
        texto = file.read().lower()  # Lê o arquivo e converte para minúsculas
        # Remove a pontuação do texto
        palavras = texto.split()  # Divide o texto em palavras (separadas por espaço em branco)

        for freq in palavras:
            f2 = float(freq)
            vetor.append(f2)
    # print(vetor)
    return vetor


def compara_bits(arq, pasta):

    sim = {}
    menor_sim = {}
    diretorio = pasta

    if os.path.exists(pasta) and os.path.isdir(pasta):
        arquivos = os.listdir(pasta)
        files_i = 0
        for arquivo in arquivos:
            files_i += 1
            # print(arquivo)
            sys.stdout.write('\r'+'[✔] Processando: '+str(files_i)+'/'+str(
                len(arquivos))+' ' + '{:.2f}'.format(files_i/len(arquivos)*100)+'%')
            sys.stdout.flush()

            # print(arquivo)
            for arq2 in os.listdir(diretorio):
                if arq2.endswith('.txt'):
                    # print(arq2)
                    caminho_arq1 = os.path.join(diretorio, arquivo)
                    caminho_arq2 = arq
                    res = calcular(caminho_arq1, caminho_arq2)

    if not os.path.exists("compara_bits"):
        os.makedirs("compara_bits")

   # caminho = os.path.join("compara_bits/", classe)
    # with open(caminho, "w") as arq:
    #    for m in menor_sim:
    #        arq.write(f'{m}\n')

def sim_matriz():

    freq_inv = []

    nome_arquivo = "classes.txt"
    # Percorre os arquivos no diretório e conta as palavras
    with open(nome_arquivo, "r", encoding="iso-8859-1") as arquivo:

        texto = arquivo.read().lower()
        texto = texto.translate(str.maketrans('', '', string.punctuation))
        palavras = texto.split()  # Divide o texto em palavras (separadas por espaço em branco)

        for pasta in palavras:
            max = 0
            diretorio = f"arq_pesos/{pasta}"
            # calcula os valores dos termos do novo vetor
            freq_inv = similaridade(pasta)#mudar
            #print(freq_inv)
            #break
            tam = os.listdir(diretorio)
            for arq2 in os.listdir(diretorio):
                max += 1
                if max > 500:
                    break
                if arq2.endswith('.txt'):
                    caminho_arq2 = os.path.join(diretorio, arq2)
                    peso_simi(pasta, caminho_arq2, freq_inv, 0)

                    sys.stdout.write('\r'+f'[✔] Processando {pasta}: '+str(max)+'/'+str(
                        len(tam))+' ' + '{:.2f}'.format(max/len(tam)*100)+'%')
                    sys.stdout.flush()

def similaridade(classe):

    matriz = np.empty((143421, 0))
    vet_res = []
    diretorio = f"arq_pesos/{classe}"
    print(f"\rCalculo da similaridade: {classe}")
    if os.path.exists(diretorio) and os.path.isdir(diretorio):
        arquivos = os.listdir(diretorio)
        files_i = 0
        for arquivo in arquivos:
            files_i += 1
            # print(arquivo)
            sys.stdout.write('\r'+'[✔] Processando: '+str(files_i)+'/'+str(
                len(arquivos))+' ' + '{:.2f}'.format(files_i/len(arquivos)*100)+'%')
            sys.stdout.flush()
            caminho = os.path.join(diretorio, arquivo)
            vet_res = txt_vetor(caminho)       
            # Conversão da lista em uma matriz NumPy
            vet_res_array = np.array(vet_res)
                # Adicionar colunas à matriz vazia
            matriz = np.hstack((matriz, vet_res_array[:, np.newaxis]))
            if files_i == 100:#comparação de similaridade com um numero pre-determinado
                break
            # Transponha a matriz para que cada linha represente um vetor,
        A_transposta = matriz.T
        # Calcule o produto interno entre todos os vetores usando a multiplicação de matrizes
        dot_products = np.dot(A_transposta, A_transposta.T)
        # Calcule as normas dos vetores "distancia"
        norms = np.linalg.norm(A_transposta, axis=1)
        # Inicializando uma matriz vazia para armazenar os resultados
        cos_angles = np.zeros_like(dot_products, dtype=float)
        # Realizando a multiplicação de matrizes usando um loop for
        for i in range(dot_products.shape[0]):
            for j in range(dot_products.shape[1]):
                if i <= j:
                    cos_angles[i, j] = dot_products[i, j] / (norms[i] * norms[j])
        
    return seleciona_mais_similar(matriz)

import numpy as np

def seleciona_mais_similar(matrix):
    # Calcular a soma das colunas (axis=0 para somar ao longo das colunas)
    soma_das_colunas = np.sum(matrix, axis=0)

    # Encontrar o índice da maior soma
    indice_maior_soma = np.argmax(soma_das_colunas)

    # Retornar a coluna correspondente ao índice encontrado
    coluna_maior_soma = matrix[:, indice_maior_soma]

    return coluna_maior_soma


def knn(classe, pasta, k):

    sim = {}
    menor_sim = {}
    diretorio = f"arq_pesos/{classe}"

    if os.path.exists(pasta) and os.path.isdir(pasta):
        arquivos = os.listdir(pasta)
        files_i = 0
        for arquivo in arquivos:
            files_i += 1
            # print(arquivo)
            sys.stdout.write('\r'+'[✔] Processando: '+str(files_i)+'/'+str(
                len(arquivos))+' ' + '{:.2f}'.format(files_i/len(arquivos)*100)+'%')
            sys.stdout.flush()

            # print(arquivo)
            for arq2 in os.listdir(diretorio):
                if arq2.endswith('.txt'):
                    # print(arq2)
                    caminho_arq1 = os.path.join(diretorio, arquivo)
                    caminho_arq2 = os.path.join(diretorio, arq2)
                    res = calcular(caminho_arq1, caminho_arq2)
                # print(res)
                    sim[arq2] = res
            # Ordenando o dicionário com base nos valores
            sim_ordenado = sorted(sim.items(), key=lambda x: x[1])

            # Obtendo os três menores pares chave-valor
            tres_menores = sim_ordenado[:1]  # menor
            v = []

            # Imprimindo os resultads
            for menores, val in tres_menores:
                resultado = menores
                valm = val
                print(f"{menores}:{val}")

        # --------------------------------------------------------------------------------
            if not menor_sim:
                menor_sim[resultado] = valm
            elif len(menor_sim) >= 10:
                valores_menor_sim = list(menor_sim.values())
                if valm < max(valores_menor_sim):
                    chave_menor_valor = max(menor_sim, key=menor_sim.get)
                    del menor_sim[chave_menor_valor]
                    menor_sim[resultado] = valm
            else:
                menor_sim[resultado] = valm

            print(f"{menor_sim}")

    if not os.path.exists("menor_sim"):
        os.makedirs("menor_sim")

    caminho = os.path.join("menor_sim/", classe)
    with open(caminho, "w") as arq:
        for m in menor_sim:
            arq.write(f'{m}\n')


def centroide(classe):

    vet_res = []
    diretorio = f"arq_pesos/{classe}"
    print(f"\rCalculo do centroide: {classe}")
    if os.path.exists(diretorio) and os.path.isdir(diretorio):
        arquivos = os.listdir(diretorio)
        files_i = 0
        for arquivo in arquivos:
            files_i += 1
            # print(arquivo)
            sys.stdout.write('\r'+'[✔] Processando: '+str(files_i)+'/'+str(
                len(arquivos))+' ' + '{:.2f}'.format(files_i/len(arquivos)*100)+'%')
            sys.stdout.flush()
            caminho = os.path.join(diretorio, arquivo)

            if files_i == 1:
                vet_res = txt_vetor(caminho)

            else:
                vet_res = somar(vet_res, caminho)

    # Encontrar os 10 maiores valores usando sorted
    # maiores_10_valores = sorted(vet_res, reverse=True)[:10]

    # print("Os 10 maiores valores são:", maiores_10_valores)

    tam = len(arquivos)
    # Dividindo cada elemento pelo valor usando um loop
    resultado = [round(x / tam, 2) for x in vet_res]

    # maiores = sorted(resultado, reverse=True)[:1000]
    # print("Os 100 maiores valores apos divisão são:", maiores)

    return resultado


def centroide_csv(valor):
    freq_inv = []

    nome_arquivo = "classes.txt"
    # Percorre os arquivos no diretório e conta as palavras
    with open(nome_arquivo, "r", encoding="iso-8859-1") as arquivo:

        texto = arquivo.read().lower()
        texto = texto.translate(str.maketrans('', '', string.punctuation))
        palavras = texto.split()  # Divide o texto em palavras (separadas por espaço em branco)

        for pasta in palavras:
            max = 0
            diretorio = f"arq_pesos/{pasta}"
            # calcula os valores dos termos do novo vetor
            freq_inv = centroide(pasta)
            tam = os.listdir(diretorio)
            for arq2 in os.listdir(diretorio):
                max += 1
                if max > 2000:
                    break
                if arq2.endswith('.txt'):
                    caminho_arq2 = os.path.join(diretorio, arq2)
                    peso_cent(pasta, caminho_arq2, freq_inv, valor)

                    sys.stdout.write('\r'+f'[✔] Processando {pasta}: '+str(max)+'/'+str(
                        len(tam))+' ' + '{:.2f}'.format(max/len(tam)*100)+'%')
                    sys.stdout.flush()


def knnM(classe, pasta, k):

    sim = {}
    maiores = {}
    diretorio = f"arq_pesos/{classe}"

    if os.path.exists(pasta) and os.path.isdir(pasta):
        arquivos = os.listdir(pasta)
        files_i = 0
        for arquivo in arquivos:
            files_i += 1
            # print(arquivo)
            sys.stdout.write('\r'+'[✔] Processando: '+str(files_i)+'/'+str(
                len(arquivos))+' ' + '{:.2f}'.format(files_i/len(arquivos)*100)+'%')
            sys.stdout.flush()

            # print(arquivo)
            for arq2 in os.listdir(diretorio):
                if arq2.endswith('.txt'):
                    # print(arq2)
                    caminho_arq1 = os.path.join(diretorio, arquivo)
                    caminho_arq2 = os.path.join(diretorio, arq2)
                    res = calcular(caminho_arq1, caminho_arq2)
                # print(res)
                    sim[arq2] = res
            # Ordenando o dicionário com base nos valores
            sim_ordenado = sorted(sim.items(), key=lambda x: x[1])

            # Obtendo os três menores pares chave-valor
            tres_menores = sim_ordenado[-2:]  # maior
            v = []

            # Imprimindo os resultads
            for menores, val in tres_menores:
                if int(val) < 1:
                    resultado = menores
                    valm = val
                    print(f"{menores}:{val}")

        # --------------------------------------------------------------------------------
            if not maiores:
                maiores[resultado] = valm
            elif len(maiores) >= 10:
                valores_maiores = list(maiores.values())
                if valm > min(valores_maiores):
                    chave_menor_valor = min(maiores, key=maiores.get)
                    del maiores[chave_menor_valor]
                    maiores[resultado] = valm
            else:
                maiores[resultado] = valm

            print(f"{maiores}")

    if not os.path.exists("maior_sim"):
        os.makedirs("maior_sim")

    caminho = os.path.join("maior_sim/", classe)
    with open(caminho, "w") as arq:
        for m in maiores:
            arq.write(f'{m}\n')


# Função para processar um arquivo .txt e contar palavras

def processar_arquivo(arquivo, pasta):

    global qtd_docs
    qtd_docs += 1
    diretorio = f"frequencia/{pasta}"
    # Crie a pasta se ela ainda não existir
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    global frequencia_palavras

    nome_arquivo = os.path.basename(arquivo)  # Obtém o nome do arquivo
    # Salva as frequências de palavras em arquivos
    caminho = os.path.join(diretorio, nome_arquivo)

    with open(arquivo, 'r', encoding='iso-8859-1') as file:
        texto = file.read().lower()  # Lê o arquivo e converte para minúsculas
        # Remove a pontuação do texto
        texto_sem_pontuacao = texto.translate(
            str.maketrans('', '', string.punctuation))
        # Divide o texto em palavras (separadas por espaço em branco)
        palavras = texto_sem_pontuacao.split()

        for palavra in palavras:
            palavra = remover_acentos(palavra)
            if not letras_indesejadas(palavra):
                if not palavra.isdigit():
                    if palavra not in stop_words:  # Verifica se a palavra não está na lista de stop words
                        lema = extrair_radical(palavra)
                        frequencia_palavras[nome_arquivo][lema] += 1

        ordenar_por_frequencia()

        for nome_arquivo, frequencia in frequencia_palavras.items():
            with open(caminho, "w") as arq:
                for palavra, contagem in frequencia.items():
                    arq.write(f'{palavra}: {contagem}\n')


def adicionar_linha_csv(nome_arquivo, nova_linha):
    dircsv = "csv/"
    caminho_csv = os.path.join(dircsv, nome_arquivo)

    # Crie o diretório se ele ainda não existir (inclui subpastas como csv/aTribuna-21dir/)
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)

    # Acrescenta a linha no fim do arquivo (cria o arquivo se nao existir)
    with open(caminho_csv, "a") as arq:
        arq.write(f"{nova_linha}\n")


def peso_cent(pasta, arquivo, freq_inv, valor):

    limite = float(valor)
    diretorio_p = f"arq_cent/{pasta}"
    # Inicialize uma lista vazia
    vetor = []
    # Crie a pasta se ela ainda não existir
    if not os.path.exists(diretorio_p):
        os.makedirs(diretorio_p)

    nome_arquivo = os.path.basename(arquivo)  # Obtém o nome do arquivo
    # Salva as frequências de palavras em arquivos
    caminho = os.path.join(diretorio_p, nome_arquivo)
    diretorio = f"arq_pesos/{pasta}"
    caminhoF = os.path.join(diretorio, nome_arquivo)

    with open(caminhoF, "r", encoding="iso-8859-1") as arqp:
        texto = arqp.read().lower()
        vetor1 = texto.split()

    for i in range(min(len(freq_inv), len(vetor1))):
        if float(freq_inv[i]) > limite and float(vetor1[i]) > 0:
            vetor.append(1)
        else:
            vetor.append(0)

    # Fora do loop, escreva o vetor em um arquivo
    nova_linha = f"{pasta},"
    tam = len(vetor)
    cont = 0
    with open(caminho, "w") as arq:
        for freq in vetor:
            cont += 1
            arq.write(f'{freq}\n')
            nova_linha += f"{freq}"

            if not cont == tam:
                nova_linha += f","

    tabela = f"{pasta}.csv"
    # print(tabela)
    adicionar_linha_csv(tabela, nova_linha)

def peso_simi(pasta, arquivo, freq_inv, valor):

    limite = float(valor)
    diretorio_p = f"arq_simi/{pasta}"
    # Inicialize uma lista vazia
    vetor = []
    # Crie a pasta se ela ainda não existir
    if not os.path.exists(diretorio_p):
        os.makedirs(diretorio_p)

    nome_arquivo = os.path.basename(arquivo)  # Obtém o nome do arquivo
    # Salva as frequências de palavras em arquivos
    caminho = os.path.join(diretorio_p, nome_arquivo)
    diretorio = f"arq_pesos/{pasta}"
    caminhoF = os.path.join(diretorio, nome_arquivo)

    with open(caminhoF, "r", encoding="iso-8859-1") as arqp:
        texto = arqp.read().lower()
        vetor1 = texto.split()

    for i in range(min(len(freq_inv), len(vetor1))):
        if float(freq_inv[i]) > limite and float(vetor1[i]) > 0:
            vetor.append(1)
        else:
            vetor.append(0)

    # Fora do loop, escreva o vetor em um arquivo
    nova_linha = f"{pasta},"
    tam = len(vetor)
    cont = 0
    with open(caminho, "w") as arq:
        for freq in vetor:
            cont += 1
            arq.write(f'{freq}\n')
            nova_linha += f"{freq}"

            if not cont == tam:
                nova_linha += f","

    tabela = f"{pasta}.csv"
    # print(tabela)
    adicionar_linha_csv(tabela, nova_linha)

# abre a pasta obtem o nome dos documentos


def abrePasta(pasta):
    # Inicializa um dicionário vazio para armazenar as palavras e suas frequência
    print(f"\nArquivo : {pasta}")

    if os.path.exists(pasta) and os.path.isdir(pasta):
        arquivos = os.listdir(pasta)
        files_i = 0
        for arquivo in arquivos:
            files_i += 1
            sys.stdout.write('\r'+'[✔] Processando: '+str(files_i)+'/'+str(
                len(arquivos))+' ' + '{:.2f}'.format(files_i/len(arquivos)*100)+'%')
            sys.stdout.flush()
            # ler(arquivo, pasta)
            caminho = os.path.join(pasta, arquivo)
            processar_arquivo(caminho, pasta)
    else:
        print("O caminho especificado não é uma pasta válida.")


def freq_invertida():

    qtd_docs = 0
    freq_arq = {}
    freq_inv = {}
    radical = []
    max = 0
    print(f"teste")
    nome_arquivo = "classes.txt"  # aquivo de entrada com o arquivo inicial

    if not os.path.exists("arq_fi"):
        os.makedirs("arq_fi")

    caminho_arqfi = os.path.join("arq_fi", "fi.txt")

    with open(nome_arquivo, "r", encoding="iso-8859-1") as arquivo:
        texto = arquivo.read()
        #texto = texto.translate(str.maketrans('', '', string.punctuation))
        palavras = texto.split()  # Divide o texto em palavras (separadas por espaço em branco)

        for pasta in palavras:
            diretorio = f"frequencia/{pasta}"
            print(f"\r{pasta}")
            for arquivo in os.listdir(diretorio):  # abro a pasta
                if arquivo.endswith('.txt'):  # pego o txt
                    qtd_docs += 1
                    # concateno a pasta com nome do arquivo
                    caminho = os.path.join(diretorio, arquivo)
                    with open(caminho, "r", encoding="iso-8859-1") as texto:  # abro o arquivo de texto
                        for linha in texto:  # percorro as linhas
                            partes = linha.split(":")
                            if len(partes) == 2:
                                chave = partes[0].strip()
                                tam = len(chave)
                                if not chave.isdigit() and tam > 1:
                                    if not chave in freq_arq:
                                        freq_arq[chave] = 1
                                    else:
                                        freq_arq[chave] += 1

    # remove termos raros (erros, nomes proprios) e comuns demais
    max_docs = MAX_PROP_DOCS * qtd_docs
    freq_filtrada = {chave: df for chave, df in freq_arq.items()
                     if MIN_DOCS <= df <= max_docs}
    print(f"\nVocabulario: {len(freq_arq)} termos -> {len(freq_filtrada)} termos "
          f"(em {MIN_DOCS} a {int(max_docs)} de {qtd_docs} documentos)")

    palavras_frequentes = sorted(
        freq_filtrada.items(), key=lambda x: x[1], reverse=True)

    # with open("arq_fi/fir4.txt", "w", encoding="iso-8859-1") as arquivo:
    #    for palavraR,freq in palavras_frequentes:
    #        arquivo.write(f"{palavraR}\n")

    with open(caminho_arqfi, "w") as arq10:
        for (palavra, frequencia) in palavras_frequentes:
            resultado = round(math.log(qtd_docs/frequencia), 2)
            # print(qtd_docs)
            freq_inv[palavra] = resultado
            arq10.write(f'{palavra}: {resultado}\n')

    return freq_inv

# Função para processar um arquivo .txt e contar palavras


def peso_bin(pasta, arquivo, freq_inv):

    diretorio_p = f"arq_pesos/{pasta}"
    # Inicialize uma lista vazia
    vetor = [0]*len(freq_inv)
    # Crie a pasta se ela ainda não existir
    if not os.path.exists(diretorio_p):
        os.makedirs(diretorio_p)

    nome_arquivo = os.path.basename(arquivo)  # Obtém o nome do arquivo
    # Salva as frequências de palavras em arquivos
    caminho = os.path.join(diretorio_p, nome_arquivo)

    with open(arquivo, "r", encoding="iso-8859-1") as file:

        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                if not key.isdigit():
                    radical = extrair_radical(key)
                    radical = remover_acentos(radical)
                    # print(radical)
                    if radical in freq_inv:
                        # print(radical)
                        indice = freq_inv.index(radical)
                        vetor[indice] = 1

    # Fora do loop, escreva o vetor em um arquivo

    nova_linha = f"{pasta},"
    tam = len(vetor)
    cont = 0
    with open(caminho, "w") as arq:
        for freq in vetor:
            cont += 1
            arq.write(f'{freq}\n')
            nova_linha += f"{freq}"

            if not cont == tam:
                nova_linha += f","

    tabela = f"{pasta}.csv"
    # print(tabela)
    adicionar_linha_csv(tabela, nova_linha)

# Função para processar um arquivo .txt e contar palavras


def peso_arq(pasta, arquivo, indices, idfs):

    diretorio_p = f"arq_pesos/{pasta}"
    # Inicialize o vetor com zeros (um peso por termo)
    vetor = [0]*len(idfs)
    # Crie a pasta se ela ainda não existir
    if not os.path.exists(diretorio_p):
        os.makedirs(diretorio_p)

    nome_arquivo = os.path.basename(arquivo)
    caminho = os.path.join(diretorio_p, nome_arquivo)
    caminhoF = os.path.join(f"frequencia/{pasta}", nome_arquivo)

    with open(caminhoF, "r", encoding="iso-8859-1") as file:

        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                # os arquivos de frequencia ja estao lematizados
                key = parts[0].strip()
                tf = int(parts[1].strip())
                if key in indices and tf > 0:
                    indice = indices[key]
                    # TF-IDF: idf * (1 + log(tf))
                    vetor[indice] = round(idfs[indice] * (1 + math.log(tf)), 2)

    # Fora do loop, escreva o vetor em um arquivo
    valores = [str(freq) for freq in vetor]
    with open(caminho, "w") as arq:
        arq.write("\n".join(valores) + "\n")

    nova_linha = f"{pasta}," + ",".join(valores)

    tabela = f"{pasta}.csv"
    adicionar_linha_csv(tabela, nova_linha)


def help():
    print("Vetorizacao:")
    print("python3 __init__.py\n")


def main():

    nome_arquivo = "classes.txt"  # aquivo de entrada com o arquivo inicial
    global frequencia_palavras
    stops()

    print("Menu:")
    print("Digite (1): para contagem de palavras")
    print("Digite (2): para criar um vetor com os termos")
    print("Digite (3): para pesar os arquivos")
    print("Digite (4): para verificar a similaridade entre arquivos")
    print("Digite (5): Verificar os 10 menos similares")
    print("Digite (6): Verificar os 10 mais similares")
    print("Digite (7): Comparar bits")
    print("Digite (8): Calculo centroide")
    print("Digite (9): Pesar os arquivos baseado no centroide minimo")
    print("Digite (10): Comparar bits Matriz")

    op = input("")

    if op == "1":

        try:
            with open(nome_arquivo, "r", encoding="iso-8859-1") as arquivo:
                texto = arquivo.read()
                #texto = texto.translate(
                #    str.maketrans('', '', string.punctuation))
                palavras = texto.split()  # Divide o texto em palavras (separadas por espaço em branco)
                    
                for palavra in palavras:
                    abrePasta(palavra)
                    frequencia_palavras.clear()  # limpar dicionario principal

        except FileNotFoundError:
            print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao abrir o arquivo: {e}")

    elif op == "2":

        if not os.path.exists("arq_fi"):
            os.makedirs("arq_fi")
        freq_invertida()  # cria o vetor com os termos

    elif op == "3":

        termos, idfs = carregar_freq_inv("arq_fi/fi.txt")
        # posicao de cada termo no vetor (montado uma unica vez)
        indices = {termo: i for i, termo in enumerate(termos)}

        # Percorre os arquivos no diretório e conta as palavras
        with open(nome_arquivo, "r", encoding="iso-8859-1") as arquivo:
            texto = arquivo.read()
           # texto = texto.translate(str.maketrans('', '', string.punctuation))
            palavras = texto.split()  # Divide o texto em palavras (separadas por espaço em branco)

            for pasta in palavras:
                max = 0
                diretorio = f"frequencia/{pasta}"
                tam = os.listdir(diretorio)
                for arq2 in os.listdir(diretorio):
                    max += 1
                    # if max > 2000:
                    # break

                    if arq2.endswith('.txt'):
                        caminho_arq2 = os.path.join(diretorio, arq2)
                        peso_arq(pasta, caminho_arq2, indices, idfs)

                    sys.stdout.write('\r'+f'[✔] Processando {pasta}: '+str(max)+'/'+str(
                        len(tam))+' ' + '{:.2f}'.format(max/len(tam)*100)+'%')
                    sys.stdout.flush()

    elif op == "4":

        print("Digite o nome dos documentos para verificar similaridade\n")
        op1 = input("Digite o nome do primeiro documento txt\n")

        op2 = input("Digite o nome do segundo documento txt\n")
    # arq_pesos/at2/0212112005at2.txt
    # 4     /home/aerty/RecInf/prova/ex141/arq_pesos/at2/09082005at2.txt
    # arq_pesos/bro/1102022003bro.txt
    # bro/1201022004bro.txt
    # arq_pesos/bro/h1623042005bro.txt
        caminho_arq1 = os.path.join("arq_pesos/", op1)
        caminho_arq2 = os.path.join("arq_pesos/", op2)

        resultado = calcular(caminho_arq1, caminho_arq2)
        print(f"A similaridade entre os docs {op1} e {op2} é :{resultado}")

    elif op == "5":

        nom_classe = input(
            "Digite o nome da classe\n")
        vizinhos = input("Digite a quantidade de vizinhos k\n")
        pasta = os.path.join("arq_pesos/", nom_classe)

        knn(nom_classe, pasta, int(vizinhos))

    elif op == "6":

        nom_classe = input(
            "Digite o nome da classe\n")
        vizinhos = input("Digite a quantidade de vizinhos k\n")
        pasta = os.path.join("arq_pesos/", nom_classe)

        knnM(nom_classe, pasta, int(vizinhos))

    elif op == "7":
        compbits = input(
            "Digite o nome da classe seguida do documento(tvt/b0516072006tvt.txt)\n")
        classebits = input(
            "Digite o nome da classe\n")

        arq_men = os.path.join("menor_sim/", compbits)
        pastama = os.path.join("maior_sim/", classebits)
        compara_bits(arq_men, pastama)

    elif op == "8":
        classe_cent = input(
            "Digite o nome da classe \n")

        centroide(classe_cent)

    elif op == "9":
        valor = input(
            "Digite um valor minimo para corte centroide entre 0 e 1 float\n")
        centroide_csv(valor)

    elif op == "10":
        sim_matriz()

    return 0


if __name__ == "__main__":
    main()
