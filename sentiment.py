import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification


model_checkpoint = 'finiteautomata/bertweet-base-sentiment-analysis'
directory_model = 'model_sentiment'
directory_tokenizer = 'tokenizer_sentiment'
dataset_file = 'dataset.txt'
train_file = 'train_tmp.txt'
validation_file = 'validation_tmp.txt'
# block_size_full = tokenizer.model_max_length


def model_tokenizer(model_checkpoint='finiteautomata/bertweet-base-sentiment-analysis'):
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


def generate(model, tokenizer, input_string):
    '''Generating Text'''
    classes = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

    inputs = tokenizer([input_string], return_tensors='pt')
    reply_ids = model(**inputs).logits
    result = argmax(torch.softmax(reply_ids, dim=1).tolist()[0])

    return classes[result], result
