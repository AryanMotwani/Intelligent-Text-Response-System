import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from text_generator import generate

def text_summarize(query):
    # initialize the pre-trained model
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained( 't5-small', legacy=False)
    device = torch.device('cpu')

    # input text
    text = generate(query)
    # preprocess the input text
    preprocessed_text = text.strip().replace('\n','')
    input_text =preprocessed_text

    #print(len(input_text.split()))

    tokenized_text = tokenizer.encode(input_text, return_tensors='pt', max_length=512, truncation=True).to(device)

    # summarize
    summary_ids = model.generate(tokenized_text, min_length=0, max_length=100)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    #print(summary)
    return summary