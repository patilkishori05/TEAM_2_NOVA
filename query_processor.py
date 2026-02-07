"""
Query Processing Model
----------------------
Implements:
1. Take user query
2. Extract keywords
3. Expand into multiple search queries
4. Classify intent (informational, commercial, navigational)
"""

# =========================
# IMPORTS
# =========================
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# =========================
# LOAD NLP MODEL
# =========================
nlp = spacy.load("en_core_web_sm")


# =========================
# INTENT CLASSIFIER (ML)
# =========================

training_queries = [
    "what is artificial intelligence",
    "how does machine learning work",
    "explain deep learning",
    "best mobile under 20000",
    "buy laptop online",
    "price of iphone 15",
    "open youtube",
    "facebook login",
    "amazon website",
    "nearest hospital"
]

training_labels = [
    "informational",
    "informational",
    "informational",
    "commercial",
    "commercial",
    "commercial",
    "navigational",
    "navigational",
    "navigational",
    "navigational"
]

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(training_queries)

intent_model = LogisticRegression()
intent_model.fit(X_train, training_labels)


def classify_intent(query):
    query_vector = vectorizer.transform([query])
    return intent_model.predict(query_vector)[0]


# =========================
# KEYWORD EXTRACTION
# =========================

def extract_keywords(query):
    doc = nlp(query)
    keywords = [
        token.text.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN", "VERB"]
        and not token.is_stop
        and token.is_alpha
    ]
    return list(set(keywords))


# =========================
# QUERY EXPANSION
# =========================

def expand_query(query, keywords):
    expanded_queries = set()

    expanded_queries.add(query)
    expanded_queries.add(" ".join(keywords))
    expanded_queries.add(query + " tutorial")
    expanded_queries.add("best " + " ".join(keywords))
    expanded_queries.add("how to " + " ".join(keywords))

    return list(expanded_queries)


# =========================
# QUERY PROCESSOR
# =========================

def process_query(user_query):
    intent = classify_intent(user_query)
    keywords = extract_keywords(user_query)
    expanded_queries = expand_query(user_query, keywords)

    return {
        "original_query": user_query,
        "intent": intent,
        "keywords": keywords,
        "expanded_queries": expanded_queries
    }


# =========================
# MAIN (CHATBOT INTERFACE)
# =========================

if __name__ == "__main__":
    print(" Query Processing Model")
    print("Type 'exit' to quit\n")

    while True:
        user_query = input("Enter your query: ")

        if user_query.lower() == "exit":
            print("Goodbye 👋")
            break

        result = process_query(user_query)

        print("\n--- QUERY ANALYSIS ---")
        print("Intent:", result["intent"])
        print("Keywords:", result["keywords"])
        print("Expanded Queries:")
        for q in result["expanded_queries"]:
            print(" -", q)
        print("----------------------\n")
