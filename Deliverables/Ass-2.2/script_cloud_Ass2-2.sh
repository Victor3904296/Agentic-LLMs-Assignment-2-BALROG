#!/bin/bash

source .venv/bin/activate

python eval.py \
  agent.type=custom \
  agent.max_image_history=0 \
  agent.max_text_history=8 \
  client.client_name=xai \
  client.base_url=https://openrouter.ai/api/v1 \
  client.model_id=anthropic/claude-haiku-5.5 \
  client.max_retries=5 \
  client.delay=5 \
  envs.names=babyai-crafter \
  envs.env_kwargs.seed=12 \
  eval.num_episodes.babyai=3 \
  eval.num_episodes.crafter=3 \
  eval.num_workers=4
