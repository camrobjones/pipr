"""
Language Models
---------------
Testing the extent to which physical inferences made by humans
in the course of resolving ambiguous pronouns can be predicted
by language models.

- GPT-2
- XLnet
- Jurassic

- Multiply & log
- 

Attributes
----------
BERT : TYPE
    Description
BERT_TOKENIZER : TYPE
    Description
DEVICE : TYPE
    Description
MODEL_NAMES_CAUSAL : list
    Description
MODEL_NAMES_LM : list
    Description
MODELS : list
    Description
USE_GPU : int
    Description

"""

import logging
import re

import numpy as np

import torch
from torch.nn import functional as F
from transformers import (AutoTokenizer, AutoModelForCausalLM,
                          # pipeline,
                          AutoModelForMaskedLM)


"""
Setup
-----
Logging & parameters

"""

logging.basicConfig(level=logging.INFO)

USE_GPU = 1

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODELS = {}

MODEL_NAMES_CAUSAL = ["gpt2", "xlnet-base-cased", "distilgpt2",
                      "gtp2-large"]
MODEL_NAMES_MASKED = ["bert-base-uncased", "roberta-base"]

"""
Model setup
-----------
Load BERT tokenizer & BERT for Masked LM and evaluate.
"""


def get_model_and_tokenizer(name):
    """Returns (model, tokenizer) tuple. Loads if needed.

    Parameters
    ----------
    name : str
        Name of a huggingface model

    Returns
    -------
    tuple
        (model, tokenizer)
    """

    # If model exists, return model
    if name in MODELS:
        return MODELS[name]

    # Load causal model
    if name in MODEL_NAMES_CAUSAL:
        logging.info("Loading model '%s'...", name)
        model = AutoModelForCausalLM.from_pretrained(name)
        logging.info("Model '%s' loaded", name)

    # Load masked model
    elif name in MODEL_NAMES_MASKED:
        logging.info("Loading model '%s'...", name)
        model = AutoModelForMaskedLM.from_pretrained(name)
        logging.info("Model '%s' loaded", name)

    else:
        raise ValueError("name not in model list: ", name)

    model.eval()

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(name)

    MODELS[name] = (model, tokenizer)

    return (model, tokenizer)


"""
Inference functions
-------------------
Pass texts to model and get probabilities of different completions.
"""


def predict_masked(text, model, tokenizer, n=5):
    """Top n predictions for all masked words in text

    Example
    -------
    >>> text = "[CLS] Sally hit Jenny because [MASK] was angry. [SEP]"
    >>> predict_masked(text, 20)

    Parameters
    ----------
    text : str
        Text containing masks
    n : int, optional
        Number of candidates to produce (5)
    model : TYPE, optional
        language model (BERT)
    tokenizer : TYPE, optional
        lm tokenizer (BERT)

    Returns
    -------
    candidates
        List of tuples  of (index, [(candidate, prob)])
    """
    tokenized_text = tokenizer.tokenize(text)
    mask_inds = np.where(np.array(tokenized_text) == "[MASK]")[0]

    # Convert token to vocabulary indices
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])

    # Predict all tokens
    with torch.no_grad():
        outputs = model(tokens_tensor)  # token_type_ids=segments_tensors)
        token_logits = outputs.logits

    # get predicted tokens
    out = []
    for mask in mask_inds:
        print("Predicting mask index: ", mask)

        # prediction for mask
        mask_preds = token_logits[0, mask.item()]
        mask_preds = torch.softmax(mask_preds, 0)
        predicted_indices = [x.item() for x in
                             torch.argsort(mask_preds, descending=True)[:n]]
        scores = [mask_preds[i].item() for i in predicted_indices]
        predicted_tokens = []
        for index in predicted_indices:
            predicted_tokens.append(tokenizer.convert_ids_to_tokens([index])[0])
        out.append((mask, list(zip(predicted_tokens, scores))))

    return out


def mask_probability(text, candidates, model, tokenizer):
    """Probabilities for candidates as replacement for [MASK] in text
    
    Example
    -------
    >>> text = "[CLS] When the rock fell on the vase, the [MASK] broke. [SEP]"
    >>> candidates = ["rock", "vase"]
    >>> mask_probability(text, candidates)
    
    Parameters
    ----------
    text : str
        Text containing a single [MASK]
    candidates : list of str
        Candidate mask replacements
    model : TYPE, optional
        language model (BERT)
    tokenizer : TYPE, optional
        lm tokenizer (BERT)
    
    Returns
    -------
    candidates : dict
        {candidate: prob}
    
    Raises
    ------
    ValueError
        Description
    """

    # Check exactly one mask
    masks = sum(np.array(text.split()) == "[MASK]")
    if masks != 1:
        raise ValueError(
            f"Must be exactly one [MASK] in text, {masks} supplied.")

    # Get candidate ids
    candidate_ids = {}
    for candidate in candidates:
        candidate_tokens = candidate.split()
        candidate_ids[candidate] = tokenizer.convert_tokens_to_ids(
            candidate_tokens)

    # TODO: Check for 100 tokens

    candidate_probs = {}

    # Loop through candidates and infer probability
    for candidate, ids, in candidate_ids.items():

        # Add a mask for each token in candidate

        candidate_text = re.sub("\[MASK\] ", "[MASK] " * len(ids), text)

        # Tokenize text
        tokenized_text = tokenizer.tokenize(candidate_text)
        mask_inds = np.where(np.array(tokenized_text) == "[MASK]")

        # Convert token to vocabulary indices
        indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([indexed_tokens])

        # Predict all tokens
        with torch.no_grad():
            outputs = model(tokens_tensor)  # token_type_ids=segments_tensors)
            predictions = outputs[0]

        # get predicted tokens
        probs = []

        for (i, mask) in enumerate(mask_inds[0]):
            # prediction for mask
            mask_preds = predictions[0, mask.item()]
            mask_preds = torch.softmax(mask_preds, 0)
            prob = mask_preds[ids[i]].item()
            probs.append(np.log(prob))

        candidate_probs[candidate] = np.exp(np.mean(probs))

    return candidate_probs


def next_seq_prob(seen, unseen, model_name, log=True):
    """Get p(unseen | seen)
    
    Parameters
    ----------
    seen : str
        Preceding context
    unseen : str
        Unseen text to be tokenized
    model : str
        Name of transformer model
    """

    # Load model
    model, tokenizer = get_model_and_tokenizer(model_name)

    # Pad unseen
    unseen = unseen if unseen[0] == " " else " " + unseen

    # Get ids for tokens
    input_ids = tokenizer.encode(seen, return_tensors="pt")
    unseen_ids = tokenizer.encode(unseen)

    # Loop through unseen tokens & sum log probs
    probs = []
    for unseen_id in unseen_ids:

        with torch.no_grad():
            logits = model(input_ids).logits

        next_token_logits = logits[0, -1]
        next_token_probs = torch.softmax(next_token_logits, 0)
    
        prob = next_token_probs[unseen_id]
        probs.append(np.log(prob))

        # Add input tokens incrementally to input
        input_ids = torch.cat((input_ids, torch.tensor([[unseen_id]])), 1)

    # Return log or raw prob
    prob = sum(probs) if log else np.exp(sum(probs))
    return prob


"""
Apply to csv
------------
"""


def mask_probability_df(df):
    """Summary
    
    Parameters
    ----------
    df : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    """
    np1_probs = []
    np2_probs = []

    for i, row in df.iterrows():

        # Extract text
        text = row['text']

        # Enforce CLS and SEP tags
        if text[:5] != "[CLS]":
            text = "[CLS] " + text

        if text[-5:] != "[SEP]":
            text = text + " [SEP]"

        # Extract candidates
        np1 = row['np1'].lower()
        np2 = row['np2'].lower()

        # Get probs
        probs = mask_probability(text, [np1, np2])

        # Add to lists
        np1_probs.append(probs[np1])
        np2_probs.append(probs[np2])

        print("\n\n" + "-" * 30 + "\n\n")
        print(f"{i} / {len(df)}: {text}")
        for k, v in probs.items():
            print(f"{k}: {v:.3g}")

    df["bert_np1_prob"] = np1_probs
    df["bert_np2_prob"] = np2_probs

    return df
