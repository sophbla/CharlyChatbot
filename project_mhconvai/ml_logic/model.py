
### Functions

# def instantiate(tokenizer_source, model_source, name):
#     tokenizer = tokenizer_source.from_pretrained(name)
#     model = model_source.from_pretrained(name)
#     return tokenizer, model


# Predict from input with a blender tokenizer and the blender model
def predict_blender_output(text, tokenizer_blend, model_blend):
    # Tokenize input
    input_token = tokenizer_blend(text, return_tensors='pt')
    # Get result from model
    result = model_blend.generate(**input_token)
    # Decode result to model answer
    output = tokenizer_blend.decode(result[0])
    return output
