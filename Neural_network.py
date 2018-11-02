import tensorflow as tf
from tensorflow import keras

class Neural_network:

    def __init__(self, name,train_path,test_path, sample):
        self.name = name
        self.train_path = train_path
        self.test_path = test_path
        self.sample = sample
    def load_data(self):
    def model_create(self):
        # Build 2 hidden layer DNN with 10, 10 units respectively.
        # To implement a neural network, the premade_estimators.py program uses a pre-made Estimator
        # named tf.estimator.DNNClassifier. This Estimator builds a neural network that classifies examples.
        # Nous avons un Réseau de Neurons avec 3 couches
        # Chaque couche a 10 neurons

        classifier = tf.estimator.DNNClassifier(
            feature_columns= my_feature_columns,
            # Two hidden layers of 10 nodes each.
            # Use the hidden_units parameter to define the number of neurons in each hidden layer of the neural network.
            # The length of the list assigned to hidden_units identifies the number of hidden layers (2, in this case).
            # Each value in the list represents the number of neurons in a particular hidden
            # layer (10 in the first hidden layer and 10 in the second hidden layer).
            # To change the number of hidden layers or neurons, simply assign a different list to the hidden_units parameter.
            hidden_units=[10, 10],
            # The model must choose between 3 classes.
            n_classes=3)

