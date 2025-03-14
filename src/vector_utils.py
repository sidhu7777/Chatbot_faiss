from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import json

def load_embeddings():
    """Load the sentence-transformers model once."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Centralized embeddings instance
embeddings = load_embeddings()

import json

def load_course_metadata():
    """Load structured course metadata from processed_courses.json."""
    try:
        with open("processed_courses.json", "r", encoding="utf-8") as file:
            return json.load(file)  # Return structured metadata
    except FileNotFoundError:
        print("Error: processed_courses.json not found! Run data_preprocessing.py first.")
        return []

def query_embedding(query, category=None):
    """Generate embedding with category awareness."""
    category_text = f"Category: {category}\n" if category else ""
    return embeddings.embed_query(category_text + query)

def create_vector_store(courses):
    """Create FAISS vector store with category-based metadata."""
    texts = [
        f"Category: {course['course_category']}\nTitle: {course['title']}\nDescription: {course['description']}"
        for course in courses
    ]
    metadata = [
        {
            "title": course["title"],
            "description": course["description"],
            "price_per_session": course["price_per_session"],
            "number_of_lessons": course["number_of_lessons"],
            "total_price": course["total_price"],
            "course_category": course["course_category"]
        }
        for course in courses
    ]

    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadata)
    vector_store.save_local("faiss_index")
    print("Vector store created and saved successfully!")

def load_vector_store():
    """Load FAISS vector store with metadata."""
    if not os.path.exists("faiss_index"):
        print("Error: Vector store not found! Run vector_utils.py first.")
        return None
    
    try:
        return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"Error loading FAISS vector store: {e}")
        return None

def search_courses(query, category=None, k=10, threshold=0.7):
    """Retrieve courses with category filtering and similarity threshold."""
    vector_store = load_vector_store()
    if not vector_store:
        return "Error: Vector store not found."
    
    query_vec = query_embedding(query, category)
    results = vector_store.similarity_search_by_vector(query_vec, k=k)
    
    filtered_results = []
    for res in results:
        metadata = res.metadata
        similarity = res.score if hasattr(res, 'score') else 1.0  # Default to 1 if no score
        if category and metadata.get("course_category", "").lower() != category.lower():
            continue  # Skip if category doesn't match
        if similarity >= threshold:
            filtered_results.append(metadata)
    
    return filtered_results if filtered_results else "No relevant courses found."


if __name__ == "__main__":
    print("Loading preprocessed courses...")
    try:
        with open("processed_courses.json", "r", encoding="utf-8") as file:
            courses = json.load(file)
        
        if not courses:
            print("Error: No courses found!")
            exit()

        print(f"Loaded {len(courses)} courses. Creating vector store...")
        create_vector_store(courses)
        print("Vector store successfully created!")

    except FileNotFoundError:
        print("Error: processed_courses.json not found! Run data_preprocessing.py first.")
