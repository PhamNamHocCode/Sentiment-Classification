from underthesea import word_tokenize
import torch
from transformers import AutoTokenizer, AutoModel
from app import user_input

labels = {
    0: 'Negative',
    1: 'Neutral',
    2: 'Positive'
}

phoBert = AutoModel.from_pretrained("vinai/phobert-base-v2")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2, use_fast = False")

def preprocess(text):
    processed_text = word_tokenize(text, format="text")
    
    return processed_text

input_ids = torch.tensor([tokenizer.encode(preprocess(user_input()))])

with torch.no_grad():
    features = phobert(input_ids) 