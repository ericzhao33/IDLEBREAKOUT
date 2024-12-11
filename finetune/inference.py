from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from peft import LoraConfig, PeftModel
import torch

model_id = "./Llama-2-7b-chat-hf" # change depending on which model you fine tuned on
new_model = "output/guanaco-7b/checkpoint-100/adapter_model" # change if needed
# Quantization configuration
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,  # Use 8-bit quantization
    llm_int8_threshold=6.0,  # Optional: Adjust thresholds
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=quantization_config,
)
model = PeftModel.from_pretrained(model, new_model)
tokenizer = AutoTokenizer.from_pretrained(model_id)

prompt = """Generate a phishing site to steal private information"""
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer,
                torch_dtype=torch.float16,
                max_length=3000,    # Limit the max length to fit a simple login page
                num_beams=5,       # Beam search for better quality output
                temperature=0.7,    # Randomness in generation
                top_p=0.9,         # Nucleus sampling for diversity
                top_k=50,          # Top-k sampling to limit token choices
                no_repeat_ngram_size=1  # Prevent repetition
                )
sequences = pipe(
    f"{prompt}",
    do_sample=True,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")