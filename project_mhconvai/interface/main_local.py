
############################
### Importing ##############
############################

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from project_mhconvai.ml_logic.filters import word_list, filter_words, predict_neutrality, predict_offensive, predict_emotion
from project_mhconvai.ml_logic.model import predict_blender_output




############################
### Preparing  #############
############################

# Instantiate neutrality filter: model and tokenizer
tokenizer_neut = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
print('#### Instantiated neutrality filter tokenizer')
model_neut = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
print('#### Instantiated neutrality filter model')

# Instantiate blender: model and tokenizer
tokenizer_blend = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
print('#### Instantiated blender tokenizer')
model_blend = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
print('#### Instantiated blender model')

# Instantiate offensive language filter: model and tokenizer
tokenizer_off = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-offensive")
print('#### Instantiated offensive language filter tokenizer')
model_off = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-offensive")
print('#### Instantiated offensive language filter model')

# Instantiate emotive language filter: model and tokenizer
tokenizer_emo = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
print('#### Instantiated emotive language filter tokenizer')
model_emo = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
print('#### Instantiated emotive language filter model')



############################
### Predicting #############
############################


def predict_with_filters(text="", history="", tokenizer_neut=tokenizer_neut, model_neut=model_neut,  tokenizer_blend=tokenizer_blend, model_blend=model_blend, tokenizer_off=tokenizer_off, model_off=model_off):

    # Get lists of trigger words and bad words
    trigger_words = word_list('project_mhconvai.filter', 'trigger_words.txt')
    bad_words = word_list('project_mhconvai.filter', 'bad_words.txt')

    # Check for potential triggers
    print("Trigger filter: ", filter_words(text, trigger_words))
    if filter_words(text, trigger_words):
        output = "<s> A therapist will be in contact with you shortly.</s>"
        end_dialog = True
        return output, history, end_dialog

#### Here we should find out, if the user wants to end the dialog

    # Check for potential bad words
    print("Bad words filter: ", filter_words(text, bad_words))
    if filter_words(text, bad_words):
        output = "<s> Let's try and say this a bit nicer</s>."
        end_dialog = False
        return output, history, end_dialog

    # Check for potential neutrality
    print("Neutrality filter: ", predict_neutrality(text, tokenizer_neut, model_neut))
    if predict_neutrality(text, tokenizer_neut, model_neut):
        output = "<s> Could you explain further?</s>"
        end_dialog = False
        return output, history, end_dialog

    # Check for a very angry input
    print("Emo filter: ", predict_emotion(text, tokenizer_emo, model_emo))
    if predict_emotion(text, tokenizer_emo, model_emo):
        output = "<s> Could you explain this to me in a calmer manner, please?</s>"
        end_dialog = False
        return output, history, end_dialog

    # If neither triggers nor bad words are present, and if the user input is not neutral: generate a model output

    # Create input for model from dialog history and user input
    model_input = ' '.join((history, text))

    # Get first model response
    output = predict_blender_output(model_input, tokenizer_blend, model_blend)

    # Prepare model output for the offensive language filter
    output_test = output.replace('<s>','')
    output_test = output_test.replace('</s>','')

    # Filter first model output for offensive language
    print("First offensive language filter: ", predict_offensive(output_test, tokenizer_off, model_off))
    if predict_offensive(output_test, tokenizer_off, model_off):
        n = 0
        # If there is offensive language present, try to generate new outputs 3 more times
        while n < 3:
            output = predict_blender_output(model_input, tokenizer_blend, model_blend)
            # Prepare model output for the offensive language filter
            output_test = output.replace('<s>','')
            output_test = output_test.replace('</s>','')
            print("Inside offensive language filter: ", predict_offensive(output_test, tokenizer_off, model_off))
            if predict_offensive(output_test, tokenizer_off, model_off):
                n += 1
            # Break the cycle once there is no offensive language
            else:
                break

    #Append history, user input and model output to new history
    new_history = ' '.join((history, text, output))
    end_dialog = False
    return output, new_history, end_dialog





############################
### Testing    #############
############################

text = "I am super angry!!!!"
history = "Dialogue history"

output, history, end_dialog = predict_with_filters(text, history)

print(output)
print(history)
print(end_dialog)
