#!/bin/bash

MODEL_URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
MODEL_DIR="models"
MODEL_FILE="$MODEL_DIR/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# Ensure the directory exists
mkdir -p "$MODEL_DIR"

if [ -f "$MODEL_FILE" ]; then
    echo "✅ Model already downloaded: $MODEL_FILE"
else
    echo "⬇️  Downloading Mistral model..."
    curl -L "$MODEL_URL" -o "$MODEL_FILE"
    echo "✅ Download complete!"
fi