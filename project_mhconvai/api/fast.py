from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

from project_mhconvai.ml_logic.filters import filter_preprocessing, filter_trigger_words, filter_bad_words
from project_mhconvai.ml_logic.model import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# with open("filter/trigger_words.txt") as file:
#     trigger_words = [line.rstrip() for line in file]

# with open("filter/bad_words.txt") as file:
#     bad_words = [line.rstrip() for line in file]


@app.get("/predict")
def predict_with_filters(input: str, history=''):

#preprocessing input
    input_cleaned = filter_preprocessing(input)
    print('--- input cleaned ---')
    #check for potential triggers
    if filter_trigger_words(input) is True:
        print('---filter trigger words ---')
        response = "A therapist will be in contact with you shortly."
        return response, history

    #check for potential bad words
    if filter_bad_words(input) is True:
        print('---filter bag words---')
        response = "Let's try and say this a bit nicer."
        return response, history

    #if neither triggers nor bad words are present, generate a model output
    output, new_history = predict(input_cleaned, history)
    print('--- predicting ---')

    # filter output for bad words
    n = 0
    if filter_bad_words(output) is True:
        #if there are bad words, try to generate new outputs 3 more times
        while n < 3:
            output, new_history = predict(input_cleaned, history)
            if filter_bad_words:
                n += 1
            #break the cycle once there are none
            else:
                break

    return dict(output, history)

@app.get("/")
def root():
    return {'greeting': 'Hello'}
