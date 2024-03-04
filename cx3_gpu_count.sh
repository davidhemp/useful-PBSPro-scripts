#!/bin/bash
for i in {0..9}; do echo "cx3-10-${i} GPU count: $(ssh cx3-10-${i} 'nvidia-smi -L | wc -l')"; done
for i in {0..8}; do echo "cx3-11-${i} GPU count: $(ssh cx3-11-${i} 'nvidia-smi -L | wc -l')"; done
echo "cx3-8-12 GPU count: $(ssh cx3-8-12 'nvidia-smi -L | wc -l')"
