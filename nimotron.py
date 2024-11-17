# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:37:23 2024

@author: vamsi
"""

import nemo
from nemo_text_processing import NLP
from nemo_text_processing.serve import query_nemo_llm

def parse_with_nemo_llm(prompt, search_results, 
                         nemo_api_key: str,  # Your NVIDIA NeMo API Key
                         nemo_model_name: str = "llama-13b",  # Choose an available NeMo LLM model
                         max_tokens: int = 100, 
                         temperature: float = 0.5):
    """
    Use NVIDIA NeMo LLM to parse search results and extract information.
    """
    if not nemo_api_key:
        print("NVIDIA NeMo API key not found. Please check your credentials.")
        return "Error: Missing NVIDIA NeMo API key."
    
    # Format the content to send to the NeMo LLM
    formatted_content = f"{prompt}\n\nWeb Search Results:\n" + "\n".join(search_results)
    
    try:
        # Initialize NeMo NLP
        nlp = NLP(api_key=nemo_api_key)
        
        # Query NeMo LLM with the formatted content
        response = query_nemo_llm(
            nlp=nlp, 
            query=formatted_content, 
            model_name=nemo_model_name, 
            max_tokens=max_tokens, 
            temperature=temperature
        )
        
        # Extract the response content
        response_content = response['generated_text'].strip()
        
        return response_content
    
    except Exception as e:
        print(f"Error with NVIDIA NeMo API: {e}")
        return "Error in extraction."

# Example usage
nemo_api_key = "YOUR_NEMO_API_KEY_HERE"
prompt = "Your Prompt Here"
search_results = ["Result 1", "Result 2", "Result 3"]

extracted_info = parse_with_nemo_llm(prompt, search_results, nemo_api_key)
print(extracted_info)
