import json
from lang_retriever import LangRetriever

if __name__ == "__main__":
    title = "Pragmatics of Understanding: Centrality of the Local Cases from Japanese Discourse and Alzheimer's Interaction"
    retriever = LangRetriever(title)
    result = retriever.retrieve()
    print(result)
