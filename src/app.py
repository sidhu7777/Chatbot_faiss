from flask import Flask, request, jsonify, render_template
from vector_utils import load_embeddings, load_vector_store

# Initialize Flask app and specify the templates folder
app = Flask(__name__, template_folder='templates')

print("Loading embeddings...")
embeddings = load_embeddings()
print("Embeddings loaded.")

print("Loading vector store...")
vector_store = load_vector_store(embeddings)
print("Vector store loaded.")


# Create a retriever for similarity search
retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 documents

# Root endpoint with a simple HTML form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the user query from the form
        query = request.form.get("query")

        if not query:
            return render_template('index.html', error="No query provided")

        # Perform a similarity search using the retriever
        relevant_docs = retriever.get_relevant_documents(query)

        # Format the results
        results = []
        for doc in relevant_docs:
            result = {
                "content": doc.page_content,  # The text content of the relevant document
            }
            results.append(result)

        # Render the results in the same HTML template
        return render_template('index.html', query=query, results=results)

    # Render the initial form for GET requests
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
