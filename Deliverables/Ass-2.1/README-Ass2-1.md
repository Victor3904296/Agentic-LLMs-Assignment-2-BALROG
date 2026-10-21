# ALLM: Assignment 2 Exercise 1

Our results can be reproduced by following the steps listed in this document.
To run these models you need to use Linux or WSL, and make sure to use Python 3.10.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
balrog-post-install
```


## Cloud model
...
```bash
./script-cloud-2-1.sh
```

## Local model
To run the local model (llama-3.2-1B-Instruct) with a 256 and a 512 output
token limit. Run `./script-local-2-1.sh`, this loads the model on a local
server with a window size of 4096 and runs 2 evaluations on this model.

```bash
./script-local-2-1.sh
```


If you prefer to run the server and evaluation separately, use the code 
below in separate terminals, and set the `max-model-len` and `max_tokens` to the preferred value.

```bash
vllm serve meta-llama/Llama-3.2-1B-Instruct \
  --port 8080 \
  --max-model-len 4096 \
  --guided-decoding-backend lm-format-enforcer

python eval.py \
  envs.names=babyai-crafter \
  envs.env_kwargs.seed=12 \
  agent.type=naive \
  agent.max_image_history=0 \
  agent.max_text_history=8 \
  eval.num_workers=1 \
  eval.num_episodes.babyai=3 \
  eval.num_episodes.crafter=3 \
  client.client_name=vllm \
  client.generate_kwargs.max_tokens=512 \
  client.model_id=meta-llama/Llama-3.2-1B-Instruct \
  client.base_url=http://localhost:8080/v1
```
