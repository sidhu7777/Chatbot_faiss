import re
from vector_utils import load_vector_store, query_embedding  # Import vector retrieval functions

# Load FAISS vector store
vector_store = load_vector_store()

def search_courses(query, k=5):
    """Retrieve top-k similar courses from FAISS vector store."""
    
    query_vec = query_embedding(query)  # Generate embedding

    if not vector_store:
        return "Error: Vector store not found."

    # Perform similarity search
    results = vector_store.similarity_search_by_vector(query_vec, k=k)

    if not results:
        return "No relevant courses found."

    # Format retrieved courses
    response = []
    for res in results:
        metadata = res.metadata
        title = metadata.get("title", "Unknown Course")
        price_per_session = metadata.get("price_per_session", "Not Available")
        total_price = metadata.get("total_price", "Not Available")
        lessons = metadata.get("number_of_lessons", "Not Available")
        description = metadata.get("description", "Not Available")

        course_details = (
            f"Course: {title}\n"
            f"Price per session: {price_per_session}\n"
            f"Total Price: {total_price}\n"
            f"Number of Lessons: {lessons}\n"
            f"Description: {description}\n"
        )
        response.append(course_details)

    return "\n".join(response)

if __name__ == "__main__":
    print("Chatbot is ready. Type 'exit' to quit.")
    while True:
        user_query = input("User: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting chatbot...")
            break
        print("Chatbot:\n", search_courses(user_query))
