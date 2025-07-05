#!/bin/bash

echo "🚀 Starting continuous smolagent coding agent loop..."
echo "Press Ctrl+C to stop the loop"
echo ""

while true; do
    echo "=== Starting new iteration $(date) ==="
    echo ""
    
    python smolagent_coding_agent.py
    
    echo ""
    echo "=== Iteration completed. Starting next iteration in 5 seconds... ==="
    echo "Press Ctrl+C to stop"
    echo ""
    sleep 5
done
