import joblib
import pickle
from textblob import TextBlob


def pred(news):
    filename = 'LogisticRegression_model.sav'
    # load the model from disk
    loaded_model = joblib.load(filename)

    vector = pickle.load(open("vectorizer.pk", "rb"))

    X_new = [str(news)]

    X_new = vector.transform(X_new)

    prediction = loaded_model.predict(X_new)

    if abs(TextBlob(news).polarity) > 0.6:
        return False

    if prediction[0] == 0:
        return True
    else:
        return False
