import pickle


class NaiveBayesClassifier:
    def __init__(self, alpha):
        """alpha - smoothing parameter"""

        self.alpha = alpha
        self.labels = set()
        self.words = set()
        self.word_dict = dict()
        self.label_dict = dict()

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""

        for sentence, label in zip(X, y):
            self.labels.add(label)
            self.label_dict[label] = self.label_dict.get(label, 0) + 1
            for word in sentence:
                self.words.add(word)
                if word not in self.word_dict:
                    self.word_dict[word] = dict()
                self.word_dict[word][label] = self.word_dict[word].get(label, 0) + 1

    def predict(self, X):
        """Perform classification on an array of test vectors X."""

        y_pred = []
        for sentence in X:
            max_label = None
            max_prob = 0
            for label in self.labels:
                prob = self.label_dict[label] / sum(self.label_dict.values())
                for word in sentence:
                    prob *= (self.word_dict.get(word, dict()).get(label, 0) + self.alpha) / (
                        self.label_dict[label] + self.alpha * len(self.words)
                    )
                if prob > max_prob:
                    max_prob = prob
                    max_label = label
            y_pred.append(max_label)
        return y_pred

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""

        _y = self.predict(X_test)
        return sum([1 if i == j else 0 for i, j in zip(_y, y_test)]) / len(y_test)

    def save(self, path):
        """Save model to path"""

        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        """Load model from path"""

        with open(path, "rb") as f:
            return pickle.load(f)
