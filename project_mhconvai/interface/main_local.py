
############################
### Importing ##############
############################

# Import text files
import importlib.resources as ir
# Used in filter functions (bad words, trigger words)
from better_profanity import profanity
# Used in filter functions (neutrality, offensive language, emotions)
import numpy as np
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from scipy.special import softmax
# Filter functions from own module
from project_mhconvai.ml_logic.filters import filter_trigger_words, filter_bad_words, predict_neutrality, predict_offensive
# Predict response to user input
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from project_mhconvai.ml_logic.model import predict_output



############################
### Preparing ##############
############################

# Loading bad words and trigger words and convert them to lists
bad_words_text = ir.read_text('project_mhconvai.filter', 'bad_words.txt')
bad_words = [line.rstrip() for line in bad_words_text .split('\n')]
trigger_words_text = ir.read_text('project_mhconvai.filter', 'trigger_words.txt')
trigger_words = [line.rstrip() for line in trigger_words_text .split('\n')]

# Instantiating tokenizer and model for neutrality filter
tokenizer_neut = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model_neut = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# Instantiating tokenizer and model for offensive language filter
tokenizer_off = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-offensive")
model_off = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-offensive")

# Instantiating tokenizer and model for predicting an answer form user input
tokenizer_blend = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model_blend = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")



############################
### Predicting #############
############################

def predict_with_filters(text, history, tokenizer_neut, model_neut, tokenizer_blend , model_blend, tokenizer_off, model_off):

    # Check for potential triggers
    if filter_trigger_words(text, trigger_words):
        ####### Question: Do we need here and in the following hard codes answers the <s> tag that comes with the model output?
        output = "A therapist will be in contact with you shortly."
        return output, history

    # Check for potential bad words
    elif filter_bad_words(text, bad_words):
        output = "Let's try and say this a bit nicer."
        return output, history

    # Check for potential neutrality
    elif predict_neutrality(text, tokenizer_neut, model_neut):
        output = "Could you explain further?"
        return output, history

#### Here the emotion analysis needs to step in with the thresholds and hard coded output

    # If neither triggers nor bad words are present, and if the user input is not neutral: generate a model output
    else:
      output = predict_output(text, history, tokenizer_blend, model_blend)

    # Filter output for offensive language
    if predict_offensive(text, tokenizer_off, model_off):
        n = 0
        # If there is offensive language present, try to generate new outputs 3 more times
        while n < 3:
            output = predict_output(text, history, tokenizer_blend, model_blend)
            if predict_offensive(text, tokenizer_off, model_off):
                n += 1
            # Break the cycle once there is no offensive language
            else:
                break

    # Append history, user input and model output to new history
    new_history = ''.join((history, text, output))

    return output, new_history






if __name__ == '__main__':
    try:
        n = 0
        history = ''
        while n < 3:
            user_input = input('Enter input:')
            output, history = predict_with_filters(user_input, history, tokenizer_neut, model_neut, tokenizer_blend , model_blend, tokenizer_off, model_off)
            print(output)
            n += 1

    except:
        import ipdb, traceback, sys
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
