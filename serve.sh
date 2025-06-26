export CUDA_VISIBLE_DEVICES=1,2
python -m vllm.entrypoints.openai.api_server \
  --model "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B" \
  --served-model-name "deepseek-r1-distill-qwen-32b" \
  --reasoning-parser deepseek_r1 \
  --trust-remote-code \
  --host="0.0.0.0" \
  --port=5000 \
  --tensor-parallel-size=2 \
  --gpu-memory-utilization 0.9 