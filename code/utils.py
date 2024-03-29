import faiss
from embeddings import get_text_embedding
import numpy as np


def faiss_index(emb_vec, dimension=384):
    index = faiss.IndexFlatL2(dimension)
    index.add(emb_vec)
    return index


def faiss_search(index, emb_vec, target, k):
    distance, indicies = index.search(emb_vec[target].reshape(1, -1), k)
    return distance, indicies


if __name__ == '__main__':
    # here is a list of 10 texts

    texts = [
        "The cat sat on the windowsill, watching the world go by.",
        "It purred softly as it spotted a bird flying across the clear blue sky.",
        "Suddenly, the cat leaped off the sill, ready for a new adventure.",
        "The scientist carefully adjusted the microscope, focusing on the specimen.",
        "Under the lens, a whole new world of cells and organisms came to life.",
        "She noted down her observations, excited about the potential discoveries.",
        "The old library held secrets in every corner, with books stacked high.",
        "A dusty tome caught my eye, its pages yellowed with age.",
        "As I opened it, a hidden map fell out, hinting at buried treasure.",
        "The sun dipped below the horizon, painting the sky with shades of orange and pink.",
        "Stars began to twinkle, appearing one by one in the vast night sky.",
        "The gentle sound of waves added a serene soundtrack to the beautiful sunset."
    ]
    emb_vec = []
    for text in texts:
        embedded = get_text_embedding(text)  # size is default 384
        emb_vec.append(embedded)

    emb_vec = np.array(emb_vec)
    faiss_obj = faiss_index(emb_vec, dimension=384)
    target = 0
    k = 3
    distance, indicies = faiss_search(faiss_obj, emb_vec, target, k)
    print(f'\nFor the text under index: {target}')
    print(f'Text starts with: {texts[0][:50]}\n')
    for i, d in zip(indicies[0], distance[0]):
        print(f'\nCorresponding text: {texts[i][:50]}')
        print(f'Cossine distance: {d}')
