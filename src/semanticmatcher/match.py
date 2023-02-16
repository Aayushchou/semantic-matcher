"""
Match
----- 

Module containing table matching functionality. 

1. Columns from one table can be compared with columns from another table.
2. Columns from one table can be compared to columns from the same table.
3. Can return an overall match score between two tables. 

Tables are expected to be inputted as pandas dataframes.
"""
import pandas as pd

from semanticmatcher.search import semantic_search_df
from semanticmatcher.utils import normalize_df

def column_search(df1: pd.DataFrame, df2: pd.DataFrame, num_matches=2):

    scores, indices = semantic_search_df(df1, df2, num_matches=num_matches)
    
    results = {}
    for i, col in enumerate(df1.columns):
        results[col] = [df2.columns[idx] for idx in indices[i]]

    # Create a new DataFrame to display the results
    results_df = pd.DataFrame(results.items(), columns=['df1_column', 'df2_similar_columns'])
    return results_df


def similarity_matrix(df1: pd.DataFrame, df2: pd.DataFrame): 

    scores, indices = semantic_search_df(df1, df2, num_matches=df2.shape[1])
    similarity_matrix = pd.DataFrame(0, index=df1.columns, columns=df2.columns)
    for i, col in enumerate(df1.columns):
        similarity_matrix.loc[col, df2.columns[indices[i]]] = scores[i]

    # Display the similarity matrix
    return similarity_matrix

if __name__ == '__main__':
    df = pd.read_csv("data/titanic.csv")
    df = df[["Lname", "Name", "Sex"]]
    res = similarity_matrix(df, df)
    breakpoint()