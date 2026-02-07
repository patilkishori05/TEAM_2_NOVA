from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_documents(contents, query):
    """
    Ranks documents based on their relevance to the query using TF-IDF and cosine similarity.

    Args:
        contents (list): A list of dictionaries, where each dictionary represents a document
                         and must contain a 'content' key with the text of the document.
                         Example: [{'url': '...', 'content': '...'}, ...]
        query (str): The search query to rank the documents against.

    Returns:
        list: The input list of documents, sorted by relevance score in descending order.
              Each dictionary in the list will have an additional 'relevance_score' key.
    """
    if not contents:
        return []

    # Extract text content from the list of dictionaries
    documents = [doc.get('content', '') for doc in contents]
    
    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # Fit and transform the documents and the query
        # We combine them to ensure the vocabulary is consistent
        tfidf_matrix = vectorizer.fit_transform(documents + [query])
        
        # Calculate cosine similarity between the query (last vector) and all documents (all but last)
        # tfidf_matrix[-1] is the query vector
        # tfidf_matrix[:-1] are the document vectors
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        
        # Add scores to the original content dictionaries
        for i, doc in enumerate(contents):
            # Convert numpy float to native python float for better compatibility
            doc['relevance_score'] = float(cosine_similarities[i])
            
        # Sort documents by relevance score in descending order
        ranked_contents = sorted(contents, key=lambda x: x['relevance_score'], reverse=True)
        
        return ranked_contents

    except ValueError:
        # Handle cases where documents might be empty or vectorization fails
        # Return original list with 0 scores if something goes wrong
        print("Warning: Could not vectorize documents. Returning unranked list.")
        for doc in contents:
            doc['relevance_score'] = 0.0
        return contents

if __name__ == "__main__":
    # Test data
    sample_contents = [
        {"url": "doc1", "content": "Python is a great programming language for data science."},
        {"url": "doc2", "content": "Bananas are a rich source of potassium."},
        {"url": "doc3", "content": "Machine learning with Scikit-Learn in Python is powerful."}
    ]
    
    query = "python data science"
    
    print(f"Ranking {len(sample_contents)} documents for query: '{query}'...")
    ranked = rank_documents(sample_contents, query)
    
    print("\n--- Ranked Results ---")
    for doc in ranked:
        print(f"Score: {doc['relevance_score']:.4f} | Content: {doc['content']}")

