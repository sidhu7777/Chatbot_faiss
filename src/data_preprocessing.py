import json
import re

def categorize_course(title, description):
    """Categorize course based on simple keyword matching."""
    categories = {
        "Python": ["python"],
        "Java": ["java"],
        "Cloud Computing": ["aws", "cloud"],
        "AI": ["ai", "artificial intelligence", "chatgpt", "machine learning"],
        "Game Development": ["game development", "unity", "scratch", "minecraft", "roblox"],
        "Web Development": ["javascript", "node", "html", "css", "web development"],
        "Mobile Development": ["mobile development"],
        "Robotics": ["robotics"],
        "Other Programming": []  # Placeholder for uncategorized courses
    }

    lower_title = title.lower()
    lower_desc = description.lower()

    for category, keywords in categories.items():
        if any(keyword in lower_title or keyword in lower_desc for keyword in keywords):
            return category
    
    return "Other Programming"  # Ensure uncategorized courses are assigned here

def preprocess_data(html_content):
    """Extract course details from HTML and structure them into JSON format."""
    pattern = re.compile(
        r'\$(\d+)\s*per session\s*(.*?)\s*(\d+)\s*Lessons\s*View Details',
        re.DOTALL
    )

    matches = pattern.findall(html_content)
    courses = []

    for match in matches:
        price_per_session = int(match[0])  # Convert price to integer
        content = match[1].strip()
        number_of_lessons = int(match[2])  # Convert lessons to int for calculation

        # Extract title and description
        if ":" in content:
            title, description = content.split(":", 1)
        elif "\n" in content:
            title, description = content.split("\n", 1)
        else:
            words = content.split()
            if len(words) > 5:
                title = " ".join(words[:5])
                description = " ".join(words[5:])
            else:
                title = content
                description = ""

        title = title.strip()
        description = description.strip()

        # Calculate total price as integer
        total_price = price_per_session * number_of_lessons

        # Categorize course
        course_category = categorize_course(title, description)

        # Store course details
        course = {
            "title": title,
            "description": description,
            "price_per_session": f"${price_per_session} per session",
            "number_of_lessons": number_of_lessons,
            "total_price": total_price,  # Store as integer
            "course_category": course_category
        }
        courses.append(course)

    return courses

if __name__ == '__main__':
    try:
        with open("scraped_content.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        if not html_content.strip():
            print(" Error: scraped_content.html is empty!")
            exit()

        processed_courses = preprocess_data(html_content)

        if not processed_courses:
            print(" Error: No courses extracted!")
            exit()

        # Save processed courses to JSON
        with open("processed_courses.json", "w", encoding="utf-8") as json_file:
            json.dump(processed_courses, json_file, indent=4)

        print(f" Processed {len(processed_courses)} courses and saved to 'processed_courses.json'.")

    except FileNotFoundError:
        print(" Error: scraped_content.html not found! Run scraper.py first.")
