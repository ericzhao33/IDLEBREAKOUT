# Finetune implementation

download weights for llama2-7b from huggingface here: <br>
https://huggingface.co/meta-llama/Llama-2-7b-hf <br>
https://huggingface.co/meta-llama/Llama-2-7b-chat-hf <br>
https://huggingface.co/codellama/CodeLlama-7b-hf <br>

## Runnnig

```bash
pip install -U -r requirements.txt
python qlora.py --model_name_or_path <path_or_name>
```
can run 
```bash
bash finetune.sh
```
to train with parameters in the file, make sure to change paths to wherever your local files are installed

code for training was obtained from https://github.com/artidoro/qlora
and from https://www.llama.com/docs/how-to-guides/fine-tuning/
