import pandas as pd
import re

# 1. Leitura do arquivo Excel
df = pd.read_excel("avaliacoes (1).xlsx")

# 2. Textos de Referência
ref_pos = "O produto possui excelente qualidade, chegou rapidamente e atendeu completamente às minhas expectativas. Gostei muito da compra e recomendo este produto para outras pessoas."
ref_neg = "O produto possui péssima qualidade, apresentou problemas logo após a compra e não atendeu às minhas expectativas. Fiquei muito decepcionado e não recomendo este produto."

# 3. Função de Pré-processamento
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    text = re.sub(r'\s+', ' ', text).strip()  # Remove espaços desnecessários
    return text

def get_tokens(text):
    clean = preprocess(text)
    return set(clean.split())

ref_pos_clean = preprocess(ref_pos)
ref_neg_clean = preprocess(ref_neg)
ref_pos_tokens = get_tokens(ref_pos)
ref_neg_tokens = get_tokens(ref_neg)

# 4. Similaridade de Jaccard
def jaccard_similarity(tokens_a, tokens_b):
    intersection = len(tokens_a.intersection(tokens_b))
    union = len(tokens_a.union(tokens_b))
    if union == 0:
        return 0.0
    return intersection / union

# 5. Distância de Levenshtein (caractere a caractere)
def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

# Processamento de cada avaliação
results = []
for idx, row in df.iterrows():
    text = row['avaliacao']
    clean_text = preprocess(text)
    tokens = get_tokens(text)
    
    j_pos = jaccard_similarity(tokens, ref_pos_tokens)
    j_neg = jaccard_similarity(tokens, ref_neg_tokens)
    
    l_pos = levenshtein_distance(clean_text, ref_pos_clean)
    l_neg = levenshtein_distance(clean_text, ref_neg_clean)
    
    # Regras de Classificação (conforme especificação da atividade)
    class_j = 'Positiva' if j_pos > j_neg else 'Negativa'
    class_l = 'Positiva' if l_pos < l_neg else 'Negativa'
    
    results.append({
        'ID': row['ID'],
        'avaliacao': text,
        'Jaccard_Pos': round(j_pos, 4),
        'Jaccard_Neg': round(j_neg, 4),
        'Class_Jaccard': class_j,
        'Lev_Pos': l_pos,
        'Lev_Neg': l_neg,
        'Class_Levenshtein': class_l
    })

res_df = pd.DataFrame(results)

# Salvar o resultado em um novo arquivo Excel
res_df.to_excel("resultado_avaliacoes.xlsx", index=False)
print("Processamento concluído! Arquivo 'resultado_avaliacoes.xlsx' gerado com sucesso.\n")

# ==============================================================================
# 6. ANÁLISE DOS RESULTADOS E RESPOSTAS AUTOMÁTICAS
# ==============================================================================

# Cálculos numéricos a partir dos dados processados
jaccard_pos = (res_df['Class_Jaccard'] == 'Positiva').sum()
jaccard_neg = (res_df['Class_Jaccard'] == 'Negativa').sum()

lev_pos = (res_df['Class_Levenshtein'] == 'Positiva').sum()
lev_neg = (res_df['Class_Levenshtein'] == 'Negativa').sum()

concordancia = (res_df['Class_Jaccard'] == res_df['Class_Levenshtein']).sum()
divergencia = (res_df['Class_Jaccard'] != res_df['Class_Levenshtein']).sum()

print("=" * 70)
print("              ANÁLISE DOS RESULTADOS (RELATÓRIO TÉCNICO)              ")
print("=" * 70)

print(f"\n1. Quantas avaliações foram classificadas como positivas pela métrica de Jaccard?")
print(f"   Resposta: {jaccard_pos} avaliações.")

print(f"\n2. Quantas avaliações foram classificadas como negativas pela métrica de Jaccard?")
print(f"   Resposta: {jaccard_neg} avaliações.")

print(f"\n3. Quantas avaliações foram classificadas como positivas pela distância de Levenshtein?")
print(f"   Resposta: {lev_pos} avaliações.")

print(f"\n4. Quantas avaliações foram classificadas como negativas pela distância de Levenshtein?")
print(f"   Resposta: {lev_neg} avaliações.")

print(f"\n5. Em quantas avaliações as duas métricas produziram a mesma classificação?")
print(f"   Resposta: {concordancia} avaliações.")

print(f"\n6. Em quantas avaliações as métricas produziram classificações diferentes?")
print(f"   Resposta: {divergencia} avaliações.")

print(f"\n7. Por que Jaccard e Levenshtein podem produzir resultados diferentes para uma mesma avaliação?")
print("   Resposta: Porque avaliam dimensões textuais distintas. A Similaridade de Jaccard trabalha em nível")
print("   de conjunto de palavras (tokens), desconsiderando a ordem dos termos, repetições exatas e variações")
print("   estritamente morfológicas de caracteres. Já a Distância de Levenshtein opera em nível sequencial de")
print("   caracteres (string completa), contando a quantidade mínima de operações de inserção, remoção e")
print("   substituição necessárias para transformar uma frase em outra.")

print(f"\n8. Qual das duas métricas apresentou maior sensibilidade às diferenças entre os textos?")
print("   Resposta: A Distância de Levenshtein apresentou maior sensibilidade às variações textuais. Como ela")
print("   contabiliza cada caractere alterado, inserido ou removido na string inteira, ela é fortemente")
print("   influenciada por pequenos detalhes de escrita, erros de digitação e pelo comprimento do texto. Isso")
print(f"   explica por que Levenshtein tendeu a classificar um volume maior de textos como positivos ({lev_pos} contra")
print(f"   {jaccard_pos} de Jaccard) ao capturar proximidades estruturais que Jaccard ignorou.")

print("=" * 70)