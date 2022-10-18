import re
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

f = open('article.txt', 'r')
text = f.read().split('.')
# print(len(text))
tf_idf_model = TfidfVectorizer(stop_words='english')
processed_text_tf = tf_idf_model.fit_transform(text)
# print(processed_text_tf)
print("\n\n\n")
query = "What is OOP?"
tfidf_df = pd.DataFrame(processed_text_tf.toarray(), columns=tf_idf_model.get_feature_names_out())
scores = processed_text_tf.toarray()
avgs = {}
one = [0, ""]
two = [0, ""]
three = [0, ""]
for i in range(len(scores)):
    avg = sum(scores[i]) / len(scores[i])
    if avg > three[0]:
        if avg > two[0]:
            if avg > one[0]:
                one = [avg, text[i]]
            else:
                two = [avg, text[i]]
        else:
            three = [avg, text[i]]
summary = one[1] + two[1] + three[1]
print(summary)

