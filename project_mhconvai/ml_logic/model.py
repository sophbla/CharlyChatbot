from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from project_mhconvai.ml_logic.filters import filter_preprocessing

def predict(input, history=''):
# initialize tokenizer and model
    tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
    model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")

#get full history
    # if len(history) != 0:
    #   input = ' '.join((*history, input))

#generate output
    input_token = tokenizer(input, return_tensors='pt')
    result = model.generate(**input_token)
    output = tokenizer.decode(result[0])

#append new input and output to history
    # history.append(' '.join((input, output)))
    history = ' '.join((input, output))

    return output, history
