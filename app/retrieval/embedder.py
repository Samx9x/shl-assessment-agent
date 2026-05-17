from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np

vectorizer = HashingVectorizer(
    n_features=384
)

def embed_text(text):

    vector = vectorizer.transform(
        [text]
    ).toarray()[0]

    return vector.astype(
        np.float32
    ).tolist()


def embed_documents(texts):

    vectors = vectorizer.transform(
        texts
    ).toarray()

    return vectors.astype(
        np.float32
    ).tolist()