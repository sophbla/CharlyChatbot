import string

# with open("filter/trigger_words.txt") as file:
#     trigger_words = [line.rstrip() for line in file]

# with open("filter/bad_words.txt") as file:
#     bad_words = [line.rstrip() for line in file]

def filter_preprocessing(sentence):
    # lower all words
    sentence = sentence.lower()
    # remove punctuation
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')
    # strip withespaces
    sentence = sentence.strip()
    print(sentence)
    return sentence

def filter_bad_words(sentence):

    bad_words = ['bad', 'word']
    # Check
    for word in sentence.split():
        if word in bad_words:
            return True
    else:
        return False


def filter_trigger_words(sentence):

    trigger_words = ['trigger', 'word']
    # Check
    for word in sentence.split():
        if word in trigger_words:
            return True
    else:
        return False
