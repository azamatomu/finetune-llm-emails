import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from runpod.serverless import start

# Check if CUDA is available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load fine-tuned model and tokenizer
model_path = 'model/mistral-7b-it-emails/'
loaded_model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto')
loaded_tokenizer = AutoTokenizer.from_pretrained(model_path)


def batch_inference(prompt: str) -> str:
    """Perform batch inference using the loaded model and tokenizer."""
    logger.info(f'Received prompt: {prompt}.')

    prompt_wrapper = lambda text: f'[INST]{text}[/INST]'

    with torch.no_grad():
        input_ids = loaded_tokenizer(prompt_wrapper(prompt), 
        	return_tensors="pt", 
        	max_length=512, 
        	truncation=True,
        	return_attention_mask=False).to(device)
        generated_ids = loaded_model.generate(**input_ids, max_length=4096-512, 
        	num_return_sequences=1, do_sample=True)
        decoded_text = loaded_tokenizer.batch_decode(generated_ids, 
        	skip_special_tokens=True)[0]

        answer_only_text = decoded_text.split('[/INST]')[-1]
        logger.info(f'Generated response: {answer_only_text}.')

        return answer_only_text


def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    prompt = job_input.get('prompt')

    if not prompt:
        raise Exception("No instances found")

    # prompts = [value['prompt'] for value in instances]
    completion = batch_inference(prompt)
    return completion



if __name__ == "__main__":
    from runpod.serverless import start

    start({"handler": handler})
