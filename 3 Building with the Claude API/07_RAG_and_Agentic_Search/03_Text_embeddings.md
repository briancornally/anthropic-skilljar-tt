## Text embeddings

#### Downloads

- [002_embeddings.ipynb(opens in new tab)](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic-poc/assets/1748558530/002_embeddings.ipynb?response-content-disposition=attachment&Expires=1778848109&Signature=HxPomC9qmfVAZ26Mqv4yqR2LiO3mk3ZSIlyz1U1Ej9CDz4HGzvAGiH-0QHZ6QCaQsVT5pGZe4yHHrLxkH0Mr6ccS8bbHqnAVx8MsUWhQjP7ZXm8a~O7IHZRu4A4XEJkb3HqubI3lER9mECeCAI3EgjoBqMrDCyZOqXblhMkS3Xc8rR2yUY-Qa~jW8uktgZFRCn4MFzfdSaQ5cdsiOYvffgdZ-kVAdhcBtg5nlN-nPBR59LAIQrTegReM~zR~n2ijZukLiYlJQvtAbu2OQ-ENqDF9J1xD3DI6aEIk~DpuxQQQKHk~D~mst42yVV4-eQAQQaX-2QGez8w61Hovsp7Mpg__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)
- [VoyageAI API Key Directions.pdf](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic-poc/assets/1748558581/VoyageAI_API_Key_Directions.pdf?response-content-disposition=attachment&Expires=1778848109&Signature=lB4wTJGWnOQDH32tBSUbEOdL66VlLc5I340sRjFUq-5NZ2eYmQ5FpTnxO6w246l3QoXW1KQwmNhFLU9R4yjp8sS9wKpwgNw1msOjaKNF-980ZurAkHXNcJJiM0ILFMQh1-ud5U-OkQEF~CXO645mRpaYq9MmTju~S0hz1epiLSJhUdVYhPwBXqyWERwJsrbZMNjuglKFK~WOlcSPef7N4csP-TFbguDYc~Kn0ytp8nWvflaWaE1EtuKjBJpGOAn5MuyMgQuFGhtarQO2uDpQKGKlNZZcp5N2NmE26kXXJYawPwAMlUJzIbQDwjP-Ak-6V0gjvQzOuLE54Cqi09o3cw__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ)

After breaking a document into chunks, the next step in a RAG pipeline is finding which chunks are most relevant to a user's question. This is essentially a search problem - you need to look through all your text chunks and identify the ones that relate to what the user is asking about.

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_03.jpg)

## Semantic Search

The most common approach for finding relevant chunks is semantic search. Unlike keyword-based search that looks for exact word matches, semantic search uses text embeddings to understand the meaning and context of both the user's question and each text chunk.

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_04.jpg)

## Text Embeddings

A text embedding is a numerical representation of the meaning contained in some text. Think of it as converting words and sentences into a format that computers can work with mathematically.

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_07.jpg)

Here's how the process works:

- You feed text into an embedding model
- The model outputs a long list of numbers (the embedding)
- Each number ranges from -1 to +1
- These numbers represent different qualities or features of the input text

## Understanding the Numbers

Each number in an embedding is essentially a "score" for some quality of the input text. However, here's the important caveat: we don't know precisely what each number represents.

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_09.jpg)

While it's helpful to imagine that one number might represent "how happy the text is" or "how much the text talks about oceans," these are just conceptual examples. The actual meaning of each dimension is learned by the model during training and isn't directly interpretable by humans.

## VoyageAI for Embeddings

Since Anthropic doesn't currently provide embedding generation, the recommended provider is VoyageAI. You'll need to:

- Sign up for a separate VoyageAI account at https://www.voyageai.com
- Get an API key (free to get started)
- Add the key to your environment variables

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_15.jpg)

In your `.env` file, add:

```
VOYAGE_API_KEY="your_key_here"
```

## Implementation

First, install the VoyageAI library:

```
%pip install voyageai
```

Then set up the client and create a function to generate embeddings:

```
from dotenv import load_dotenv
import voyageai

load_dotenv()
client = voyageai.Client()

def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]
```

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_18.jpg)

When you run this function on a text chunk, you'll get back a list of floating-point numbers representing the embedding. The process is quick and straightforward - the real challenge is understanding how to use these embeddings effectively in your RAG pipeline for finding the most relevant content.

![img](03_Text_embeddings.assets/07_-_003_-_Text_Embeddings_19.jpg)

The next step is learning how to compare embeddings to determine which chunks are most similar to a user's question, which forms the core of the semantic search process.
