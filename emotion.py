import torch
import torch.nn.functional as F

from transformers import AutoTokenizer, AutoModelForSequenceClassification


model_checkpoint = 'finiteautomata/bertweet-base-emotion-analysis'
directory_model = 'model_emotion'
directory_tokenizer = 'tokenizer_emotion'
dataset_file = 'dataset.txt'
train_file = 'train_tmp.txt'
validation_file = 'validation_tmp.txt'
# block_size_full = tokenizer.model_max_length


def model_tokenizer(model_checkpoint='finiteautomata/bertweet-base-emotion-analysis'):
    '''Model and Tokenizer launch'''

    model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    return model, tokenizer


def save_model_tokenizer(model, tokenizer,
                         directory_model=directory_model,
                         directory_tokenizer=directory_tokenizer):
    '''Saving model and tokenizer'''

    tokenizer.save_pretrained(directory_tokenizer)
    model.save_pretrained(directory_model)


def load_model_tokenizer(directory_model=directory_model,
                         directory_tokenizer=directory_tokenizer):
    '''Loading fine-tuned model'''

    tokenizer = AutoTokenizer.from_pretrained(
        directory_tokenizer, from_pt=True)
    model = AutoModelForSequenceClassification.from_pretrained(directory_model)
    return model, tokenizer


def argmax(iterable):
    '''Return index of max element in any iterable object'''

    return max(enumerate(iterable), key=lambda x: x[1])[0]


def generate_class(model, tokenizer, input_string):
    '''Predicting Classes'''
    classes = ["others", "joy", "sadness", "anger", "surprise", "disgust", "fear"]

    inputs = tokenizer([input_string], return_tensors='pt')
    reply_ids = model(**inputs).logits
    result = argmax(torch.softmax(reply_ids, dim=1).tolist()[0])

    return classes[result], result


def generate_probs(model, tokenizer, input_string):
    '''Predicting Probabilities'''

    inputs = tokenizer([input_string], return_tensors='pt')
    reply_ids = model(**inputs).logits

    return reply_ids


def normalize(reply_ids):
    '''Predicting and generating final classes'''
    classes = ["others", "joy", "sadness", "anger", "surprise", "disgust", "fear"]

    result = F.normalize(reply_ids)
    result = argmax(torch.softmax(reply_ids, dim=1).tolist()[0])

    return classes[result], result
