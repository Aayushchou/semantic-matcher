"""
Search
-----
Module defines the main search and semantic parsing functionality.
"""

import faiss
import pandas as pd

from sentence_transformers import SentenceTransformer
from typing import List


def semantic_search_1d(queries: List[str], 
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


def semantic_search_df(df1: pd.DataFrame, 
                       df2: pd.DataFrame, 
                       model_name: str = 'all-MiniLM-L6-v2',
                       num_matches: int=2):
    try: 
        # Load the SentenceTransformer model and generate embeddings for the values in the columns
        model = SentenceTransformer(model_name)
        df1_embeddings = model.encode(df1.values.flatten())
        df2_embeddings = model.encode(df2.values.flatten())
    except TypeError as e:
        print(e)
        raise TypeError("Please ensure you are providing only categorical or text columns")

    # Reshape the embeddings back into a 2D matrix, with one row per column and one column per embedding dimension
    df1_embeddings = df1_embeddings.reshape((df1.shape[1], -1))
    df2_embeddings = df2_embeddings.reshape((df2.shape[1], -1))

    # Initialize a FAISS index and add the df2 embeddings to it
    d = df1_embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(df2_embeddings)


    # Search for the most similar columns in df2 for each df1 column
    scores, indices = index.search(df1_embeddings, num_matches)
    return scores, indices


if __name__ == '__main__':
    #scores, indices = semantic_search(["I like tomatoes", "tomato", "ketchup"], ["I like tomatoes", "I like potatoes"])
    #breakpoint()
    dfa = pd.read_csv("data/titanic.csv")