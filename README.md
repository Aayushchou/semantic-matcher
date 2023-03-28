# semantic-matcher

[![Unit Tests](https://github.com/Aayushchou/semantic-matcher/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/Aayushchou/semantic-matcher/actions/workflows/unit_tests.yml)

This library is built to handle anything related to semantic matching.

In its current state, it has two main uses:

* Find the closest matches of a user query to a text corpus, using sentence transformer encodings and FAISS for optimization.
* Measure the semantic similarity between two tables and determine common columns. Useful for detecting duplicates and determining which columns to join on.
