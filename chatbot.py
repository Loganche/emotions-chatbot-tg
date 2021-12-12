from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

model_checkpoint = 'facebook/blenderbot-400M-distill'
directory_model = 'model_chat'
directory_tokenizer = 'tokenizer_chat'
dataset_file = 'dataset.txt'
train_file = 'train_tmp.txt'
validation_file = 'validation_tmp.txt'
# block_size_full = tokenizer.model_max_length


def model_tokenizer(model_checkpoint='facebook/blenderbot-400M-distill'):
    '''Model and Tokenizer launch'''

    model = BlenderbotForConditionalGeneration.from_pretrained(model_checkpoint)
    tokenizer = BlenderbotTokenizer.from_pretrained(model_checkpoint)

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

    tokenizer = BlenderbotTokenizer.from_pretrained(
        directory_tokenizer, from_pt=True)
    model = BlenderbotForConditionalGeneration.from_pretrained(directory_model)
    return model, tokenizer


def generate(model, tokenizer, input_string):
    '''Generating Text'''

    inputs = tokenizer([input_string], return_tensors='pt')
    reply_ids = model.generate(**inputs)

    return tokenizer.batch_decode(
        reply_ids, skip_special_tokens=True)
