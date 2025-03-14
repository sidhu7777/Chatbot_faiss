# Chatbot with FAISS-Based Course Retrieval

This project is a **Fast and Efficient AI-Powered Chatbot** designed to retrieve course details using **FAISS (Facebook AI Similarity Search)**. The chatbot allows users to explore courses dynamically based on different queries.

## Features Implemented

- **Course Category Search** – Retrieve courses by category (e.g., `"List AI courses"`).
- **Course Title Search** – Fetch details of a course using its title (e.g., `"What is AI Pro Camp?"`).
- **Price & Lesson Retrieval** – Get price and lesson count for any course (e.g., `"What is the price of AI Pro Camp?"`).
- **Different Course Categories** – List all available course categories (e.g., `"What different courses are available?"`).
- **Full Course Listing** – Display all courses grouped by category (e.g., `"What courses are available?"`).
- **Lowest Price Course Search** – Find the **cheapest course overall** or within a **specific category** (e.g., `"What is the lowest price AI course?"`).

---

## Project Structure

````
Chatbot_faiss/
├── src/
│   ├── Scrapper.py              # Web scraping for course data (LangChain WebBaseLoader)
│   ├── data_preprocessing.py     # Extract & preprocess course data
│   ├── vector_utils.py           # FAISS retrieval logic
│   ├── metadata.py               # Main chatbot logic (course search, filtering)
│   ├── model.py                  # Query handling & embedding retrieval
│   ├── app.py                    # API to interact with the chatbot
│   ├── templates/
│   │   ├── index.html            # Frontend UI for chatbot
├── tests/
│   ├── Working_price_lesson.py
│   ├── courses_description_working.py
│   ├── metadata_working_category_based.py
│   ├── vector_test.py
├── data/
│   ├── processed_courses.json    # Cleaned & structured course metadata
│   ├── scraped_content.html      # Raw scraped course data
├── .gitignore                    # Excludes unnecessary files
├── requirements.txt               # Dependencies list
├── README.md                      # Project documentation

````

##  Technologies Used

````
| Category                | Tools & Libraries          |
|-------------------------|---------------------------|
| **Programming Language** | Python                 |
| **Vector Search**       | FAISS                    |
| **Data Handling**       | LangChain, ChromaDB        |
| **Web Scraping**        | LangChain WebBaseLoader    |
| **API Framework**       | Flask / FastAPI           |
| **Machine Learning**    | Sentence-Transformers     |
| **Testing**            | PyTest                    |

````
##  Sample Queries
````
Here are some example queries you can try with the chatbot:

General Course Queries

User: What courses are available?
Bot: Here are the available courses grouped by category:
- AI: AI Pro Camp, Time Mastery Camp, AI Camp for Jobs & Business...
- Python: Python Programming - Beginner, Python Programming - Intermediate...
- Web Development: Learn JavaScript, Learn Node.js, Web Development Pro...


User: List AI courses
Bot: Found 4 course(s) in 'AI':
- Time Mastery Camp (AI)
- AI Camp for Jobs & Business (AI)
- From Beginner to AI Pro (AI)
- AI Pro Camp (AI)


User: What different courses are available?
Bot: We offer courses in the following categories:
- Mobile Development
- Game Development
- Robotics
- Cloud Computing
- Python
- AI
- Other Programming
- Java
- Web Development
````
