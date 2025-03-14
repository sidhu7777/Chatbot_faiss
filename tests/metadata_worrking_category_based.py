import json
from vector_utils import search_courses, load_vector_store

def get_all_categories():
    """Retrieve all course categories from FAISS metadata."""
    vector_store = load_vector_store()
    if not vector_store:
        return []  # If FAISS is not loaded, return an empty list
    
    categories = set()
    for doc in vector_store.docstore._dict.values():
        category = doc.metadata.get("course_category", "").lower()
        if category:
            categories.add(category)
    
    return list(categories)

def detect_category(query):
    """Match user query to the correct category from FAISS metadata."""
    all_categories = get_all_categories()

    for category in all_categories:
        if category in query.lower():
            return category  

    return None  

def retrieve_courses(query):
    """Retrieve exactly `k=5` courses per category before enabling dynamic retrieval."""

    detected_category = detect_category(query)
    
    if not detected_category:
        return "No specific category detected. Try asking about Python, Java, AI, Web Development, etc."

    # Retrieve exactly `k=5` results from FAISS
    results = search_courses(query, category=detected_category, k=5, threshold=0.7)

    if isinstance(results, str) or not results:
        return f"No courses found in '{detected_category}'. Try searching in other categories."

    # Format results properly
    response = f"\nFound {len(results)} course(s) in '{detected_category}':\n"
    for course in results:
        response += f"- {course['title']} ({course['course_category']})\n"

    return response

if __name__ == "__main__":
    print("Course Metadata Retrieval Ready. Type a query or 'exit' to quit.")

    while True:
        user_query = input("User: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        response = retrieve_courses(user_query)
        print(response)
