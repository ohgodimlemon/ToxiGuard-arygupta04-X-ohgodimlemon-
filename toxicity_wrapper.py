import tensorflow as tf
from tensorflow.keras.layers import TextVectorization
import pandas as pd


class ToxicityClassifier:
    def __init__(self, model_paths, max_features=200000, sequence_length=1800):
        """
        Initializes the classifier with multiple models and a text vectorizer.

        Args:
            model_paths (dict): A dictionary where keys are labels (e.g., 'toxic')
                                and values are paths to the respective models.
            max_features (int): Maximum number of features for the text vectorizer.
            sequence_length (int): Length of output sequences from the vectorizer.
        """
        # Load models
        self.models = {label: tf.keras.models.load_model(path) for label, path in model_paths.items()}

        # Load dataset for adapting the vectorizer
        df = pd.read_csv('jigsaw-toxic-comment-classification-challenge/train.csv')
        df = df.drop(columns=['severe_toxic'])
        X = df['comment_text']

        # Initialize and adapt the text vectorizer
        self.vectorizer = TextVectorization(max_tokens=max_features,
                                            output_sequence_length=sequence_length,
                                            output_mode='int')
        self.vectorizer.adapt(X.values)

    def predict(self, comment):
        """
        Predicts the attributes of a comment using all loaded models.

        Args:
            comment (str): The comment to classify.

        Returns:
            dict: A dictionary of labels and their corresponding predictions.
        """
        # Vectorize the comment
        vectorized_comment = self.vectorizer([comment])

        # Get predictions from all models
        predictions = {label: model.predict(vectorized_comment)[0][0] for label, model in self.models.items()}

        return predictions

    def classify(self, comment, threshold=0.5):
        """
        Classifies a comment based on prediction thresholds.

        Args:
            comment (str): The comment to classify.
            threshold (float): The decision threshold for each label.

        Returns:
            list: A list of labels where the prediction exceeds the threshold.
        """
        predictions = self.predict(comment)
        return [label for label, score in predictions.items() if score > threshold]
