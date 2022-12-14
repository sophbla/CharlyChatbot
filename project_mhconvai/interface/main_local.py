
############################
### Importing ##############
############################

# Question 1: Do we need to import here the packages that are needed for the execution of the filter functions?
# We import them in filters.py but in this file we only import the functions from filers.py, not the packages that are needed for their execution?

# Question 2: What is the best moment to read the text files for the filters and to instantiate different models and tokenizers?
# Here we do it each time the predict function is called (like it is done in the taxifare package). But is it really the best way`?
# Our model is big and maybe the prediction gets very slow like this.`

# Question 3: Do we have to include the <s> tag in the hard-coded output of our filters? The model output has this tag,
# so I guess the hard-coded output needs the tag, too.

# Question 4: I do not understand what if __name__ == '__main__' does.

# Comment/Question 5: In the function "predict with filters" I included an additional "end_dialog" variable in the function's return.
# At some points of the dialog we want to give a final response end the dialog.
# This is f. e. the case, if the user's input contains a trigger word or if the user's input contains something like "Good bye".
# How does this interact with the chat bot interface?



from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from project_mhconvai.ml_logic.filters import word_list, filter_trigger_words, filter_bad_words, predict_neutrality, predict_offensive
from project_mhconvai.ml_logic.model import instantiate, predict_blender_output



############################
### Predicting #############
############################

def predict_with_filters(text="", history=""):

    # Instantiate tokenizer and model for input filter
    tokenizer_neut, model_neut = instantiate(AutoTokenizer, AutoModelForSequenceClassification, "cardiffnlp/twitter-roberta-base-sentiment")

    # Get lists of trigger words and bad words
    trigger_words = word_list('project_mhconvai.filter', 'trigger_words.txt')
    bad_words = word_list('project_mhconvai.filter', 'bad_words.txt')

    # Check for potential triggers
    if filter_trigger_words(text, trigger_words):
        output = "A therapist will be in contact with you shortly."
        end_dialog = True
        return output, history, end_dialog

#### Here we should find out, if the user wants to end the dialog

    # Check for potential bad words
    elif filter_bad_words(text, bad_words):
        output = "Let's try and say this a bit nicer."
        end_dialog = False
        return output, history, end_dialog

    # Check for potential neutrality
    elif predict_neutrality(text, tokenizer_neut, model_neut):
        output = "Could you explain further?"
        end_dialog = False
        return output, history, end_dialog


#### Here the emotion analysis might step in.

    # If neither triggers nor bad words are present, and if the user input is not neutral: generate a model output
    else:
        # Create input for model from dialog history and user input
        model_input = ' '.join((history, text))

        # Instantiate blender model and blender tokenizer
        tokenizer_blend, model_blend = instantiate(BlenderbotTokenizer, BlenderbotForConditionalGeneration, "facebook/blenderbot-400M-distill")

        # Get first model response
        output = predict_blender_output(model_input, tokenizer_blend, model_blend)

    # Instantiate tokenizer and model for offensive language filter
    tokenizer_off, model_off = instantiate(AutoTokenizer, AutoModelForSequenceClassification, "cardiffnlp/twitter-roberta-base-offensive")

    # Filter first model output for offensive language
    if predict_offensive(output, tokenizer_off, model_off):
        n = 0

        # If there is offensive language present, try to generate new outputs 3 more times
        while n < 3:
            output = predict_blender_output(model_input, tokenizer_blend, model_blend)
            if predict_offensive(output, tokenizer_off, model_off):
                n += 1

            # Break the cycle once there is no offensive language
            else:
                break

    # Append history, user input and model output to new history
    new_history = ''.join((history, text, output))
    end_dialog = False



    return output, new_history, end_dialog






if __name__ == '__main__':
    try:
        n = 0
        history = ''
        while n < 3:
            user_input = input('Enter input:')
            output, history, end_dialog = predict_with_filters(user_input, history)
            print(output)
            n += 1

    except:
        import ipdb, traceback, sys
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
