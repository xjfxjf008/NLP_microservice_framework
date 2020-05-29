import numpy as np
import fasttext
import time

def nlp_predict(text: str, threshold=0.5):
    """
    Need to be implemented with real NLP model function, currently with MOCK only.
    """
    # time.sleep(3)
    score = np.random.rand()
    label = 'positive' if score > threshold else 'negative'
    return score, label