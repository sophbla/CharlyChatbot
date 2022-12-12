from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
# from project_mhconvai.ml_logic.filters import word_list, filter_trigger_words, filter_bad_words, predict_neutrality, predict_offensive
from project_mhconvai.ml_logic.model import instantiate, predict_blender_output

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

tokenizer_blend, model_blend = instantiate(BlenderbotTokenizer, BlenderbotForConditionalGeneration, "facebook/blenderbot-400M-distill")

@app.get("/predict")
def predict(text="", history=""):
    global tokenizer_blend
    global model_blend

    model_input = ' '.join((history, text))

    # Get first model response
    output = predict_blender_output(model_input, tokenizer_blend, model_blend)

    new_history = ''.join((history, text, output))
    end_dialog = False

    return dict(output=output, new_history=new_history, end_dialog=end_dialog)


@app.get("/")
def root():
    return {'greeting': 'Hello'}
