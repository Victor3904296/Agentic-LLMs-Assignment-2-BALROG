<p align="center">
  <a href="https://balrogai.com">
    <img src="docs/imgs/balrog_banner.png" width="50%" alt="BALROG Agent" />
  </a>
</p>

---

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
...
```

## Local model
To run the local model (llama-3.2-1B-Instruct) you need 2 separate terminals, since one will handle the hosting of the model and the other will evaluate that model.

1st Terminal:
```bash
source .venv/bin/activate

vllm serve meta-llama/Llama-3.2-1B-Instruct \
  --port 8080 \
  --max-model-len 4096 \
  --guided-decoding-backend lm-format-enforcer
```
This loads the model with a reduced context window and starts a local server.

2nd Terminal:
```bash
source .venv/bin/activate

python eval.py \
  envs.names=babyai-crafter-babaisai \
  envs.env_kwargs.seed=12 \
  agent.type=naive \
  agent.max_image_history=0 \
  agent.max_text_history=8 \
  eval.num_workers=1 \
  eval.num_episodes.babyai=3 \
  eval.num_episodes.crafter=3 \
  eval.num_episodes.babaisai=3 \
  client.client_name=vllm \
  client.model_id=meta-llama/Llama-3.2-1B-Instruct \
  client.base_url=http://localhost:8080/v1
```
This runs the evaluation of the model on BabyAI, Crafter and BabaIsAI, each with 3 repetitions.


