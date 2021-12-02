# Write a function to get the surprisal of the target word given the context using GPT-2

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_surprisal(context, target):
    """
    Get the surprisal of the target word given the context using GPT-2
    
    Parameters
    ----------
    context: str
        The context
    target: str
        The target word
    
    Returns
    -------
    float
        The surprisal of the target word
    """
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    context_tokens = tokenizer.encode(context)
    target_tokens = tokenizer.encode(target)
    input_ids = torch.tensor(context_tokens + target_tokens).unsqueeze(0)
    outputs = model(input_ids)
    loss = outputs[0]
    return -loss[0, -1, target_tokens[0]].item()

# Test your function
get_surprisal("The", "cat")
