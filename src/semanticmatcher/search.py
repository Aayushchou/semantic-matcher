"""
Search
-----
Module defines the main search and semantic parsing functionality.
"""

import faiss
import pandas as pd
import multiprocessing

from sentence_transformers import SentenceTransformer
from typing import List
from huggingface_hub.utils import RepositoryNotFoundError


def semantic_search(
    queries: List[str],
    documents: List[str],
    model_name: str = "all-MiniLM-L6-v2",
    num_matches: int = 2,
    normalise: bool = True,
    num_shards: int = round(multiprocessing.cpu_count() / 2),
    quantise: bool = False,
    nlist: int = 1,
):
    """
    Function to perform semantic search on a set of queries and documents.

    Args:
        queries - The search queries that we are looking to find in a document
        documents - The search space/corpus to search from
        model_name - The sentence transformer model that should be used
        num_matches - The number of matches to be returned.
        normalise - Whether to normalise the embeddings, to get a normalised similarity score
        num_shards - number of parallel processes
        quantise - whether to quantize index using Clustering
        nlist - number of clusters to apply when quantising
    Returns:
        scores - Matrix with "num_queries" rows and "num_matches" columns.
                 The value is the cosine distance for each match
        indices - Matrix with "num_queries" rows and "num_matches" columns.
                 The value is the index of the document sorted by closest match
    """
    if (not queries) or (not documents):
        raise ValueError("Empty queries and/or documents lists")

    model = SentenceTransformer(model_name)
    query_embeddings = model.encode(queries)
    doc_embeddings = model.encode(documents)
    dimension = doc_embeddings.shape[1]

    if normalise:
        faiss.normalize_L2(doc_embeddings)
        faiss.normalize_L2(query_embeddings)

    index = faiss.IndexFlatIP(dimension)

    index_shards = faiss.IndexShards(dimension)
    # Split the corpus embeddings into smaller chunks

    if len(doc_embeddings) >= 2 * num_shards:
        chunk_size = len(doc_embeddings) // num_shards
    else:
        chunk_size = 2

    chunks = [doc_embeddings[i:i + chunk_size] for i in range(0, len(doc_embeddings), chunk_size)]

    for chunk in chunks:

        if quantise: 
            index = faiss.IndexIVFFlat(index, dimension, nlist)
            index.train(chunk)
            index.add(chunk)
        else:
            index = faiss.IndexFlatIP(dimension)
            index.add(chunk)
        index_shards.add_shard(index)
        
    scores, indices = index_shards.search(query_embeddings, num_matches)

    return scores, indices


def semantic_search_df(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    model_name: str = "all-MiniLM-L6-v2",
    num_matches: int = 2,
    normalise: bool = True
):
    if (df1.empty) or (df2.empty):
        raise ValueError("One or both tables are empty")
    try:
        # Load the SentenceTransformer model and generate embeddings for the values in the columns
        model = SentenceTransformer(model_name)
        df1_embeddings = model.encode(df1.values.flatten())
        df2_embeddings = model.encode(df2.values.flatten())
    except IndexError as e:
        raise TypeError(
            "Please ensure you are providing only categorical or text columns"
        )
    except RepositoryNotFoundError as e:
        raise ValueError("Sentence transformer model does not exist")

    # Reshape the embeddings back into a 2D matrix, with one row per column and one column per embedding dimension
    df1_embeddings = df1_embeddings.reshape((df1.shape[1], -1))
    df2_embeddings = df2_embeddings.reshape((df2.shape[1], -1))

    if normalise:
        faiss.normalize_L2(df1_embeddings)
        faiss.normalize_L2(df2_embeddings)
        
    # Initialize a FAISS index and add the df2 embeddings to it
    d = df1_embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(df2_embeddings)

    # Search for the most similar columns in df2 for each df1 column
    scores, indices = index.search(df1_embeddings, num_matches)
    return scores, indices


if __name__ == "__main__":
    scores, indices = semantic_search(["I like tomatoes", "tomato", "ketchup"], 
                                      ["I like tomatoes", "potatoes", 
                                       "Every day there are new challenges"], 
                                       )
    breakpoint()
    #dfa = pd.read_csv("data/titanic.csv")
