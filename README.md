# Análise de Similaridade Textual em Avaliações (PLN)

Este repositório contém a atividade prática de Processamento de Linguagem Natural (PLN) desenvolvida para o estudo de caso de classificação de avaliações de produtos utilizando as métricas **Similaridade de Jaccard** e **Distância de Levenshtein**[cite: 1, 3].

## 📋 Sobre o Projeto
O objetivo do programa é ler uma base de dados com 100 avaliações de clientes de comércio eletrônico, realizar o pré-processamento dos textos (conversão para minúsculas, remoção de pontuação e tokenização) e compará-los com duas avaliações de referência (uma positiva e uma negativa) para determinar a proximidade e classificação de cada texto[cite: 1, 2, 3, 4].

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Pandas** (manipulação de dados e leitura/escrita de arquivos Excel)
* **Re** (expressões regulares para pré-processamento de texto)

## 📁 Estrutura de Arquivos
* `main.py`: Script principal contendo o código de leitura, pré-processamento e cálculo das métricas.
* `avaliacoes (1).xlsx`: Arquivo de entrada contendo as 100 avaliações brutas[cite: 1].
* `resultado_avaliacoes.xlsx`: Arquivo gerado automaticamente pelo script com as colunas de pontuação e classificações finais de Jaccard e Levenshtein.

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python instalado na sua máquina.
2. Instale a biblioteca necessária para leitura de arquivos Excel (`openpyxl`):
   ```bash
   pip install openpyxl
   ```
3. Certifique-se de que o arquivo avaliacoes (1).xlsx está na mesma pasta do script main.py.

5. Execute o script:

  ```bash
    python main.py
    ```
O arquivo resultado_avaliacoes.xlsx será gerado na pasta com os resultados da classificação.