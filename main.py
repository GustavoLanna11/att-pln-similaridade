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
    # Jaccard: Positivo > Negativo -> Positiva, senão Negativa (inclui empates)
    class_j = 'Positiva' if j_pos > j_neg else 'Negativa'
    
    # Levenshtein: Positivo < Negativo -> Positiva, senão Negativa (inclui empates)
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
print("Processamento concluído! Arquivo 'resultado_avaliacoes.xlsx' gerado com sucesso.")