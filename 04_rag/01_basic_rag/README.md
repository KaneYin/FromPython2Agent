It is a implementation of a simple RAG system that retrieves information from a predefined dataset and generates responses based on the retrieved knowledge.

- Embedding model: A pre-trained language model converts input text into embeddings, vector representations that capture semantic meaning. These vectors will be used to search for relevant information in the dataset.
- Vector database: A storage system for knowledge and its corresponding embedding vectors. We'll implement a simple in-memory database from scratch.
- Chatbot: A language model that generates responses based on retrieved knowledge.

# Indexing phase
The indexing phase is the first step in creating a RAG system. It involves breaking the dataset (or documents) into small chunks and calculating a vector representation for each chunk that can be efficiently searched during generation.

The size of each chunk can vary depending on the dataset and the application. For example, in a document retrieval system, each chunk can be a paragraph or a sentence. In a dialogue system, each chunk can be a conversation turn.

After the indexing phrase, each chunk with its corresponding embedding vector will be stored in the vector database.

The embedding vectors can be later used to retrieve relevant information based on a given query. Think of it as SQL `where` clause, but instead of querying by exact text matching, we can now query a set of chunks based on their vector representations.

To compare the similarity between two vectors, we can use cosine similarity, Euclidean distance, or other distance metrics. In this example, we will use cosine similarity. Here is the formula for cosine similarity between two vectors A and B:

![](https://cdn-gcs.ngxson.com/nuiblog2/2024/10/1730149025318_868a5548.webp)

# Retrieval phrase
In the diagram below, we will take an example of a given Input Query from User. We then calculate the Query Vector to represent the query, and compare it against the vectors in the database to find the most relevant chunks.

The result returned by The Vector Database will contain top N most relevant chunks to the query. These chunks will be used by the Chatbot to generate a response.

## Local setup and execution

This is an independent Python project with its own `pyproject.toml` and `uv.lock`. It pins Python 3.13 and uses Ollama for embeddings and generation.

The existing code selects these model identifiers:

- Embeddings: `hf.co/CompendiumLabs/bge-base-en-v1.5-gguf`
- Generation: `hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF`

Have an Ollama service running and make both models available before starting the demo. Model availability and answer quality were not tested during repository organization.

```sh
# From the repository root:
cd 04_rag/01_basic_rag
uv sync --locked
uv run --locked python main.py
```

Run from this directory because the code opens `cat-facts.txt` relative to the working directory. Each start embeds all 150 dataset rows, retrieves the three highest-scoring chunks for one question, and streams the model's answer.

## Review status

The full indexing/retrieval/generation path passed a check with mocked Ollama responses. Importing `main.py` also triggers indexing; cosine similarity currently has no zero-vector or dimension checks. These limitations and the original implementation were left unchanged. See the [code review](../../docs/CODE_REVIEW.md) for details.

[Repository home](../../README.md) · [Repository guide](../../docs/REPOSITORY_GUIDE.md)
