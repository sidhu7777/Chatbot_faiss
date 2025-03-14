import json
from src.vector_utils import search_courses, load_vector_store

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
    """
    Retrieve courses dynamically with category-based filtering and course description lookup.
    """
    # Step 1: Check for category in the query
    detected_category = detect_category(query)
    if not detected_category:
        return "No specific category detected. Try asking about Python, Java, AI, Web Development, etc."
    
    # Step 2: Load courses from JSON or vector store
    courses = load_course_metadata()
    
    # Step 3: Check if the user is asking for a specific course title
    for course in courses:
        if course["title"].lower() in query.lower():
            return f"Course: {course['title']}\nDescription: {course['description']}"
    
    # Step 4: If no specific course is detected, list all courses in the detected category
    results = search_courses(query, category=detected_category, k=5, threshold=0.6)  # Lower threshold for listing
    if isinstance(results, str) or not results:
        return f"No courses found in '{detected_category}'. Try searching in other categories."
    
    # Format results as a list of courses
    response = f"\nFound {len(results)} course(s) in '{detected_category}':\n"
    for course in results:
        response += f"- {course['title']} ({course['course_category']})\n"
    return response

def load_course_metadata():
    """Load structured course metadata from processed_courses.json."""
    try:
        with open("processed_courses.json", "r", encoding="utf-8") as file:
            return json.load(file)  # Return structured metadata
    except FileNotFoundError:
        print("Error: processed_courses.json not found! Run data_preprocessing.py first.")
        return []

if __name__ == "__main__":
    print("Course Metadata Retrieval Ready. Type a query or 'exit' to quit.")

    while True:
        user_query = input("User: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        response = retrieve_courses(user_query)
        print(response)