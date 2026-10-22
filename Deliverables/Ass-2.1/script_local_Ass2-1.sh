#!/bin/bash

# Activate environment
source .venv/bin/activate

echo "=== Step 1: Starting vLLM Server ==="
vllm serve meta-llama/Llama-3.2-1B-Instruct \
  --port 8080 \
  --max-model-len 4096 \
  --guided-decoding-backend lm-format-enforcer > app.log 2>&1 &
SERVER_PID=$!

# Ensure the server is killed when scripts stops
trap "kill $SERVER_PID 2>/dev/null" EXIT

echo "=== Step 2: Waiting for vLLM to finish initialization ==="
# Wait for successful response
until curl -s http://localhost:8080/v1/models > /dev/null; do
    sleep 15
    echo "Model is still loading..."
done

echo "=== Server is ready! ==="

echo "=== Step 3: Start evaluation of model with 256 token limit ==="
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
  client.generate_kwargs.max_tokens=256 \
  client.model_id=meta-llama/Llama-3.2-1B-Instruct \
  client.base_url=http://localhost:8080/v1

echo "=== Step 4: Start evaluation of model with 512 token limit ==="
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

echo "=== Evaluations complete! Shutting down server. ==="