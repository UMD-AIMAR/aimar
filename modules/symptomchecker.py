import re
import json
import pickle as pkl
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

AIMAR_DIR = "skills/mycroft_aimar"

wnl = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
# with open(f"{AIMAR_DIR}/symptom_data_dict.pkl", 'rb') as f:
#     symptom_data_dict = pkl.load(f)
mayo_clinic_dialog = json.load(open(f"{AIMAR_DIR}/mayo_clinic_dialog.json"))
mayo_clinic_dialog = {s['name']: s['dialogs'].items() for s in mayo_clinic_dialog}


def clean_text(s, remove_stopwords=False, return_tokens=False):
    pattern = re.compile('[\W_]+')
    words = pattern.sub(' ', s.lower()).split()
    if remove_stopwords:
        words = [word for word in words if word not in stop_words]
    if return_tokens:
        return words
    return ' '.join([wnl.lemmatize(word) for word in words])


def top_match(scores):
    return sorted(scores.items(), key=lambda x: x[1]['fuzz'], reverse=True)[0]


def match(query):
    if query is None:
        return None, None

    scores = {}
    tokens = clean_text(query, remove_stopwords=True, return_tokens=True)

    for symptom in mayo_clinic_dialog.keys():
        scores[symptom] = {}
        scores[symptom] = max([fuzz.partial_ratio(token, symptom) for token in tokens])

    top_symp_name, top_symp_score = sorted(scores.items(), key=lambda x: x[1], reverse=True)[0]
    return top_symp_name, mayo_clinic_dialog[top_symp_name]


def save_dialog(questions, responses):
    filename = "symptom_checker.txt"
    with open(filename, 'w') as f:
        for i, (question_prefix, choices) in enumerate(questions):
            response = responses[i]
            f.write(f"{question_prefix} {choices}\n")
            f.write(f"{response}\n")
