
### Import

from better_profanity import profanity

import numpy as np #### Do we need it here?
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from scipy.special import softmax



### Functions

# Check if sentence contains bad words (True or false)
def filter_bad_words(sentence, bad_words):
    profanity.load_censor_words(bad_words)
    return profanity.contains_profanity(sentence)

# Check if sentence contains trigger words (True or false)
def filter_trigger_words(sentence, trigger_words):
    profanity.load_censor_words(trigger_words)
    return profanity.contains_profanity(sentence)


# Function for predicting neutrality / Return true or false
def predict_neutrality(text, tokenizer_neut, model_neut):
    # Get prediction
    encoded_input = tokenizer_neut(text, return_tensors='pt')
    output = model_neut(**encoded_input)
    scores = output[0][0].detach().numpy() # conert tensor output to numpy array
    scores = softmax(scores)
    # Create dictionary with scores for neutrality
    labels_neut = ['negative', 'neutral', 'positive']
    neutrality = {}
    for i in range(len(scores)):
        neutrality[labels_neut[i]] = scores[i]
    # Check if user input is neutral or not
    if neutrality['neutral'] > neutrality['negative'] and neutrality['neutral'] > neutrality['positive']:
        return True
    else:
        return False


# Function for predicting offensive language / Returns True or False
def predict_offensive(text, tokenizer_off, model_off):
    # Get prediction
    encoded_input = tokenizer_off(text, return_tensors='pt')
    output = model_off(**encoded_input)
    scores = output[0][0].detach().numpy() # convert tensor output to numpy array
    scores = softmax(scores)
    # Create dictionary with scores for offensive language
    labels_off = ['not-offensive', 'offensive']
    offensive = {}
    for i in range(len(scores)):
        offensive[labels_off[i]] = scores[i]
    # Check if text is offensive or not
    if offensive['offensive'] > offensive['not-offensive']:
        return True
    else:
        return False
