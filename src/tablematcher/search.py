"""
Search
-----
Module defines the main search and semantic parsing functionality.
"""

import faiss

from sentence_transformers import SentenceTransformer
from typing import List


def semantic_search(queries: List[str], 
                    documents: List[str], 
                    model_name='all-MiniLM-L6-v2', 
                    num_matches=2):
    """
    Function to perform semantic search on a set of queries and documents. 
    
    Args: 
        queries - The search queries that we are looking to find in a document
        documents - The search space/corpus to search from
        model_name - The sentence transformer model that should be used
        num_matches - The number of matches to be returned. The
    Returns: 
        scores - Matrix with "num_queries" rows and "num_matches" columns.
                 The value is the cosine distance for each match
        indices - Matrix with "num_queries" rows and "num_matches" columns. 
                 The value is the index of the document sorted by closest match
    """
    model = SentenceTransformer(model_name)
    query_embeddings = model.encode(queries)
    doc_embeddings = model.encode(documents)
    
    num_queries = query_embeddings.shape[1]
    index = faiss.IndexFlatIP(num_queries)
    index.add(doc_embeddings)

    scores, indices = index.search(query_embeddings, num_matches)
    return scores, indices


if __name__ == '__main__':
    scores, indices = semantic_search(["I like tomatoes", "tomato", "ketchup"], ["I like tomatoes", "I like potatoes"])
    breakpoint()