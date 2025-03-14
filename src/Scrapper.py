from langchain.document_loaders import WebBaseLoader

def scrape_data(url):
    print("Loading webpage content...")
    loader = WebBaseLoader(url)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")
    
    if documents:
        html_content = documents[0].page_content
        print("Webpage content loaded successfully.")
        return html_content
    else:
        print("No documents found.")
        return None

if __name__ == '__main__':
    url = "https://brainlox.com/courses/category/technical"
    print("Scraping data from:", url)
    
    try:
        html_content = scrape_data(url)
        if html_content:
            print("Scraped content (first 1000 characters):")
            print(html_content[:1000])  # Print the first 1000 characters for debugging

            # Save the scraped content to a file for later use
            with open("scraped_content.html", "w", encoding="utf-8") as file:
                file.write(html_content)
            print("Scraped content saved to 'scraped_content.html'")
        else:
            print("No content to save.")
    except Exception as e:
        print(f"An error occurred: {e}")