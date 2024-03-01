import runpod

import os
import google.protobuf
from os.path import dirname

# from flask import Flask, request, jsonify

import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

device = "cuda" if torch.cuda.is_available() else "cpu"

# Download the fine-tuned model files and copy into 'mistral-7b-it-emails' folder
model_path = f'model/mistral-7b-it-emails/'
loaded_model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto')
loaded_tokenizer = AutoTokenizer.from_pretrained(model_path)


prompt_wrapper = lambda text: f'[INST]{text}[/INST]'

def batch_inference(prompt: str) -> str:
    # res: [str] = []
    # for p in prompt:
    with torch.no_grad():
        input_ids = loaded_tokenizer(prompt_wrapper(prompt), 
        	return_tensors="pt", 
        	max_length=512, 
        	truncation=True,
        	return_attention_mask=False).to(device)
        generated_ids = loaded_model.generate(**input_ids, max_length=4096-512, 
        	num_return_sequences=1, do_sample=True)
        generated_text = loaded_tokenizer.batch_decode(generated_ids, 
        	skip_special_tokens=True)[0]
        # res.append(generated_text)
        # return res
        return generated_text


def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    prompt = job_input.get('prompt')

    if not prompt:
        raise Exception("No instances found")

    # prompts = [value['prompt'] for value in instances]
    completion = batch_inference(prompt)
    return completion



runpod.serverless.start({"handler": handler})
