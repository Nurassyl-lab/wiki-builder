import pandas as pd
import numpy as np
from embeddings import get_text_embedding
import faiss

df = pd.read_csv('dataset/wiki_text.csv')

columns = df.columns

emb_vec = []
texts = []

stop_col = 2  # load only 5 columns

for col_index, col in enumerate(columns):
    print(f"\nColumn index: {col_index}")
    for text_index, text in enumerate(df[col]):
        print(f"Text index: {text_index}")
        e_vec = np.array(get_text_embedding(text[:-1]))
        emb_vec.append(e_vec)
        texts.append(text[:-1])
    if col_index == stop_col:
        break

emb_vec = np.array(emb_vec)
index = faiss.IndexFlatL2(384)
index.add(emb_vec)

target = 0
k = 3

distance, indicies = index.search(emb_vec[target].reshape(1, -1), k)

print(f'For the text under index: {target}')
print(f'Text starts with: {texts[0][:50]}')

for i, d in zip(indicies[0], distance[0]):
    print(f'Corresponding text: {texts[i][:50]}')
    print(f'Cossine distance: {d}')
