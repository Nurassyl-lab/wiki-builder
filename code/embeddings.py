from sentence_transformers import SentenceTransformer

def get_text_embedding(text):
    # Load a pre-trained sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate the embedding for the input text
    embedding = model.encode(text)

    return embedding

if __name__ == "__main__":
    # Example usage
    text = """Sentence embedding models are designed to capture the semantic meaning of the entire sentence or text in a fixed-length vector. This fixed length is a feature of the model's architecture and is independent of the length of the input text. The idea is that this vector can then be used in various downstream tasks like text classification, clustering, or similarity comparisons, providing a consistent representation regardless of the original text length."""
    embedding_vector = get_text_embedding(text)
    print("Embedding vector:", embedding_vector)
    size = embedding_vector.shape
    print(f"Embedding shape: {size}")
