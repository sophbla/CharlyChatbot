from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import string
from project_mhconvai.ml_logic.filters import filter_preprocessing, filter_trigger_words, filter_bad_words
from project_mhconvai.ml_logic.model import predict

with open("../filter/trigger_words.txt") as file:
    trigger_words = [line.rstrip() for line in file]

with open("../filter/bad_words.txt") as file:
    bad_words = [line.rstrip() for line in file]

def predict_with_filters(input, history=[]):
    #preprocessing input
    input_cleaned = filter_preprocessing(input)

    #check for potential triggers
    if filter_trigger_words(input, trigger_words) is True:
      response = "A therapist will be in contact with you shortly."
      return response, history

    #check for potential bad words
    elif filter_bad_words(input, bad_words) is True:
      response = "Let's try and say this a bit nicer."
      return response, history

    #if neither triggers nor bad words are present, generate a model output
    else:
      output, new_history = predict(input_cleaned, history)

    #filter output for bad words
    if filter_bad_words(output, bad_words) is True:
        n = 0
        #if there are bad words, try to generate new outputs 3 more times
        while n < 3:
            output, new_history = predict(input_cleaned, history)
            if filter_bad_words:
                n += 1
            #break the cycle once there are none
            else:
                break

    return output, history

if __name__ == '__main__':
    try:
        n = 0
        history = []
        while n < 3:
            input = input('Enter input:')
            output, history = predict_with_filters(input, history)
            print(output)
            n += 1

    except:
        import ipdb, traceback, sys
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
