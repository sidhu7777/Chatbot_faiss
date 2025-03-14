def test_faiss_index():
    from vector_utils import load_embeddings, load_vector_store
    embeddings = load_embeddings()
    vector_store = load_vector_store(embeddings)
    
    # Check if data is loaded
    print(f"Number of documents in vector store: {len(vector_store.docstore._dict)}")
    
    assert len(vector_store.docstore._dict) > 0, "Vector store should contain at least one document."

    print("Test passed: FAISS vector store contains data.")

test_faiss_index()
