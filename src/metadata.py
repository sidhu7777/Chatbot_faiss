import json
from vector_utils import search_courses, load_vector_store

def get_all_categories():
    """Retrieve all unique course categories from FAISS metadata."""
    vector_store = load_vector_store()
    if not vector_store:
        return []  # If FAISS is not loaded, return an empty list
    
    categories = set()
    for doc in vector_store.docstore._dict.values():
        category = doc.metadata.get("course_category", "").title()
        if category:
            categories.add(category)
    
    return list(categories)

def detect_category(query):
    """Match user query to the correct category from FAISS metadata."""
    all_categories = get_all_categories()

    for category in all_categories:
        if category.lower() in query.lower():
            return category  

    return None  

def load_course_metadata():
    """Load structured course metadata from processed_courses.json."""
    try:
        with open("processed_courses.json", "r", encoding="utf-8") as file:
            return json.load(file)  # Return structured metadata
    except FileNotFoundError:
        print("Error: processed_courses.json not found! Run data_preprocessing.py first.")
        return []

def retrieve_courses(query):
    """
    Retrieve courses dynamically with category-based filtering and course description lookup.
    """
    # Step 1: Load courses from JSON
    courses = load_course_metadata()

    # Step 2: Handle "What different courses do you have?" → Return only categories
    if any(keyword in query.lower() for keyword in ["different courses", "types of courses"]):
        categories = get_all_categories()
        if categories:
            return "We offer courses in the following categories:\n- " + "\n- ".join(categories)
        return "No course categories found."

    # Step 3: Handle "What courses are available?" → Return all courses grouped by category
    if any(keyword in query.lower() for keyword in ["available courses", "list all courses", "what courses do you have"]):
        categories = get_all_categories()
        if not categories:
            return "No course categories found."
        
        response = "Here are the available courses grouped by category:\n"
        for category in categories:
            category_courses = [course["title"] for course in courses if course["course_category"].lower() == category.lower()]
            if category_courses:
                response += f"\n**{category} Courses:**\n" + "\n".join(f"- {title}" for title in category_courses)

        response += "\n\nWould you like to know more about any specific course?"
        return response

    # Step 4: Check for an **exact** course title match first
    exact_match = next((course for course in courses if course["title"].lower() == query.lower()), None)

    # Step 5: If exact match found, return its details immediately
    if exact_match:
        if "price" in query.lower() or "cost" in query.lower():
            return f"Course: {exact_match['title']}\nPrice per session: {exact_match['price_per_session']}\nTotal price: ${exact_match['total_price']}"
        elif "session" in query.lower() or "lesson" in query.lower():
            return f"Course: {exact_match['title']}\nNumber of lessons: {exact_match['number_of_lessons']}"
        else:
            return f"Course: {exact_match['title']}\nDescription: {exact_match['description']}"

    # Step 6: If no exact match, try **partial matching**, prioritizing longer course names
    matched_courses = sorted(
        [course for course in courses if course["title"].lower() in query.lower()],
        key=lambda x: len(x["title"]),  # Sort by length to prefer full names
        reverse=True
    )

    if matched_courses:
        best_match = matched_courses[0]  # Pick the longest title match
        if "price" in query.lower() or "cost" in query.lower():
            return f"Course: {best_match['title']}\nPrice per session: {best_match['price_per_session']}\nTotal price: ${best_match['total_price']}"
        elif "session" in query.lower() or "lesson" in query.lower():
            return f"Course: {best_match['title']}\nNumber of lessons: {best_match['number_of_lessons']}"
        else:
            return f"Course: {best_match['title']}\nDescription: {best_match['description']}"

    # Step 7: If no specific course is detected, check category-based search
    detected_category = detect_category(query)
    if not detected_category:
        return "No specific category detected. Try asking about Python, Java, AI, Web Development, etc."

    # Step 8: Retrieve category-based courses
    results = search_courses(query, category=detected_category, k=5, threshold=0.6)

    if isinstance(results, str) or not results:
        return f"No courses found in '{detected_category}'. Try searching in other categories."
    
    # Format results as a list of courses
    response = f"\nFound {len(results)} course(s) in '{detected_category}':\n"
    for course in results:
        response += f"- {course['title']} ({course['course_category']})\n"
    
    return response

if __name__ == "__main__":
    print("Course Metadata Retrieval Ready. Type a query or 'exit' to quit.")

    while True:
        user_query = input("User: ").strip()  # Normalize input
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        response = retrieve_courses(user_query)
        print(response)
