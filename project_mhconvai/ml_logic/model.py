### Import
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration


### Function

# Predict from user input, dialog history with a given tokenizer and a given model
def predict_output(text, history, tokenizer_blend, model_blend):
    # Tokenize input
    input_token = tokenizer_blend(text, return_tensors='pt')
    # Get result from model
    result = model_blend.generate(**input_token)
    # Decode result to model answer
    output = tokenizer_blend.decode(result[0])
    return output
