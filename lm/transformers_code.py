"""
Stolen from James Michaelov
"""


import argparse
from transformers import pipeline, AutoTokenizer, top_k_top_p_filtering,AutoModelForCausalLM,AutoModelForMaskedLM
import torch
from torch.nn import functional as F
from pprint import pprint
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

parser = argparse.ArgumentParser(description='Extracts softmax surprisal for specified words')

parser.add_argument('--stimuli', '-i', type=str,
                    help='stimuli to test')
parser.add_argument('--output_directory','-o', type=str,
                    help='output directory')
parser.add_argument('--seed', type=int, default=1111,
                    help='random seed')
parser.add_argument('--output_type','-t', type=str,default='selected',
                    help='choose whether to output all surprisals or just those marked on the stimuli')
parser.add_argument('--model','-m', type=str,default='distilbert-base-cased',
                    help='select a model to use')
parser.add_argument('--model_list','-l', type=str,
                    help='path to file with a model list')
parser.add_argument('--task', type=str, default = "surprisal",
                    help='path to file with a model list')
args = parser.parse_args()


torch.manual_seed(args.seed)   
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")




def get_causal_lm_probability(preceding_context,target_word,model):
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(model)

    sequence = preceding_context

    input_ids = tokenizer.encode(sequence, return_tensors="pt")

    next_token_logits = model(input_ids, return_dict=True).logits[:, -1, :]
    
    probs = F.softmax(next_token_logits,dim=-1)
    
    tw_encoded = tokenizer.encode(target_word)
    
    probability = probs[0,tw_encoded]

    return(probability)
    
def get_masked_lm_probability(cleaned_sentence,target_word,model):
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForMaskedLM.from_pretrained(model).to(device)
    
    sequence = cleaned_sentence.replace(target_word,tokenizer.mask_token)

    input = tokenizer.encode(sequence, return_tensors="pt").to(device)
    mask_token_index = torch.where(input == tokenizer.mask_token_id)[1]

    token_logits = model(input, return_dict=True).logits.to(device)
    mask_token_logits = token_logits[0, mask_token_index, :]
    
    probs = F.softmax(mask_token_logits,dim=-1)
    
    tw_encoded = tokenizer.encode(target_word)[1:-1]
    
    
    probability = probs[0,tw_encoded]
    
    return(probability)
    
# # filter
# filtered_next_token_logits = top_k_top_p_filtering(next_token_logits, top_k=50, top_p=1.0)

# # sample
# probs = F.softmax(filtered_next_token_logits, dim=-1)
# next_token = torch.multinomial(probs, num_samples=1)

# generated = torch.cat([input_ids, next_token], dim=-1)

# resulting_string = tokenizer.decode(generated.tolist()[0])
# print(resulting_string)


def output_surprisal_and_probability(chosen_models,stimuli,out_dir):
    for model in chosen_models:

        out_file = out_dir + '/' + stimuli.split('/')[-1].split('.')[0] + '.' + args.task + '.'+ model.replace("/","-") + '.output'
        with open(out_file, 'w') as wf:
            wf.write('Sentence;TargetWord;Probability;Surprisal\n')
        with open(stimuli, 'r') as rf:
            for line in rf:
                sentence_split = line.split()
                cleaned_sentence = ' '.join(sentence_split).replace('*',"")
                if args.output_type == 'selected':
                    record_index = [i for (i,word) in enumerate(sentence_split) if '*' in word][0]
                    preceding_context = f' '.join(sentence_split[:record_index])
                    target_word = ' ' + sentence_split[record_index].replace('*',"")
                    target_word = target_word.replace(".","")
                    if model in causal_lms:
                        probability = get_causal_lm_probability(preceding_context,target_word,model)
                        try:
                            assert len(probability)==1
                            probability_float = float(probability)
                            with open(out_file, 'a') as wf:
                                wf.write('{0};{1};{2};{3}\n'.format(cleaned_sentence,target_word,probability_float,-np.log2(probability_float)))
                        except:
                            print('"{}" is not in the dictionary. Not saving.'.format(target_word))
                            print(probability)
                    elif model in masked_lms:
                        probability = get_masked_lm_probability(cleaned_sentence,target_word,model)
                        try:
                            assert len(probability)==1
                            probability_float = float(probability)
                            with open(out_file, 'a') as wf:
                                wf.write('{0};{1};{2};{3}\n'.format(cleaned_sentence,target_word,probability_float,-np.log2(probability_float)))
                        except:
                            print('"{}" is not in the dictionary. Not saving.'.format(target_word))
                            print(probability)


def output_cosine_similarity(chosen_models,stimuli,out_dir):
    for model in chosen_models:

        model_name = model
        
        if model in causal_lms:
            tokenizer = AutoTokenizer.from_pretrained(model)
            model = AutoModelForCausalLM.from_pretrained(model).to(device)
        elif model in masked_lms:
            tokenizer = AutoTokenizer.from_pretrained(model)
            model = AutoModelForMaskedLM.from_pretrained(model).to(device)
            
            
        out_file = out_dir + '/' + stimuli.split('/')[-1].split('.')[0] + '.' + args.task + '.'+ model_name + '.output'
        with open(out_file, 'w') as wf:
            wf.write('Sentence;TargetWord;CosineSimilarity\n')
        with open(stimuli, 'r') as rf:
            for line in rf:
                sentence_split = line.split()
                cleaned_sentence = ' '.join(sentence_split).replace('*',"")
                if args.output_type == 'selected':
                    record_index = [i for (i,word) in enumerate(sentence_split) if '*' in word][0]
                    preceding_context = f' '.join(sentence_split[:record_index])
                    target_word = ' ' + sentence_split[record_index].replace('*',"")    
                    
                    preceding_context_idxs = tokenizer.encode(preceding_context)
                    preceding_context_embeddings = model.transformer.wte.weight[preceding_context_idxs]
                    preceding_context_embeddings_mean = torch.mean(preceding_context_embeddings,0)
                    
                    target_word_idxs = tokenizer.encode(target_word)
                    target_word_embeddings = model.transformer.wte.weight[target_word_idxs]
                    target_word_embedding_mean = torch.mean(target_word_embeddings,0)
                    
                    cos_sim_obj = torch.nn.CosineSimilarity(dim=0,eps=1e-100)
                    
                    
                    cos_sim = cos_sim_obj(preceding_context_embeddings_mean,target_word_embedding_mean)
                    cos_sim =  float(cos_sim.detach())
                    with open(out_file, 'a') as wf:
                        wf.write('{0};{1};{2}\n'.format(cleaned_sentence,target_word,cos_sim))

                        
                    
causal_lms = ['gpt2-large',
              'gpt2-medium',
              'gpt2',
              'gpt2-xl',
              'transfo-xl-wt103',
              'EleutherAI/gpt-neo-1.3B',
              'EleutherAI/gpt-neo-2.7B',
              'GroNLP/gpt2-small-dutch',
              'ml6team/gpt2-small-dutch-finetune-oscar',
              'ml6team/gpt2-medium-dutch-finetune-oscar',
              'openai-gpt',
              'xlnet-base-cased',
              'xlnet-large-cased',
              'distilgpt2',
              'microsoft/prophetnet-large-uncased'
              ]

masked_lms = ['roberta-large',
              'roberta-base-openai-detector',
              'roberta-base',
              'bert-base-cased',
              'bert-large-cased',
              'distilbert-base-cased',
              'GroNLP/bert-base-dutch-cased',
              'pdelobelle/robbert-v2-dutch-base',
              'Geotrend/bert-base-nl-cased',
              'bert-base-multilingual-cased',
              'xlm-roberta-large',
              'xlm-mlm-100-1280',
              'distilbert-base-cased',
              'distilroberta-base',
              'albert-base-v2',
              'albert-large-v2',
              'albert-xlarge-v2',
              'albert-xxlarge-v2',
              'allenai/longformer-large-4096',
              'allenai/longformer-base-4096',
              'microsoft/mpnet-base'
              ]



if args.model_list:
    with open(args.model_list, 'r') as f:
        chosen_models = f.read().splitlines()
elif args.model:
    chosen_models = [args.model]
# if args.model =='suite':
#     chosen_models = ['roberta-large',
#                      'bert-large-cased',
#                      'gpt2-large',
#                      'transfo-xl-wt103',
#                      'xlnet-large-cased',
# #                      'xlm-mlm-en-2048',
# #                      'xlm-roberta-large',
# #                      'distilroberta-base',
#                      'distilbert-base-cased',
#                      'roberta-large-openai-detector'
# #                      'roberta-base-openai-detector'
#                     #  'gpt2-xl'
#                     ]
# elif args.model =='suite2':
#     chosen_models = [#'roberta-large',
#                     #  'bert-large-cased',
#                     #  'gpt2-large',
#                     #  'transfo-xl-wt103',
#                     #  'xlnet-large-cased',
#                      'xlm-mlm-en-2048',
#                      'xlm-roberta-large',
#                      'distilroberta-base',
#                     #  'distilbert-base-cased',
#                     #  'roberta-large-openai-detector'
#                      'roberta-base-openai-detector',
#                      'gpt2-xl'
#                     ]
else:
    print('No model selected. Using default: distilbert-base-cased')

if args.task == 'surprisal': 
    output_surprisal_and_probability(chosen_models,args.stimuli,args.output_directory)
elif args.task == 'cosine_similarity':
    output_cosine_similarity(chosen_models,args.stimuli,args.output_directory)   
