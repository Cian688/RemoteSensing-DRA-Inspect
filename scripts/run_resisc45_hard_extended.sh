#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="configs/patchcore_remote_sensing.yaml"
OUTPUT_DIR="outputs/remote_sensing/results/resisc45_hard_extended"
LOG_DIR="logs/resisc45_hard_extended"
SEED=42
THRESHOLDS=(clean_fixed corruption_agnostic)
DEGRADATIONS=(noise blur light lowres jpeg)
MEMORIES=(clean mixed)

cd "${REPO_ROOT}"
mkdir -p "${OUTPUT_DIR}" "${LOG_DIR}"

run_protocol_block() {
  local gpu_id="$1"
  local hard_protocol="$2"
  local normal_class="$3"
  local normal_tag="$4"

  for degradation in "${DEGRADATIONS[@]}"; do
    for memory_mode in "${MEMORIES[@]}"; do
      local log_path="${LOG_DIR}/${normal_tag}_${hard_protocol}_${degradation}_${memory_mode}.log"
      echo "==> GPU${gpu_id} | ${hard_protocol} | ${degradation} | ${memory_mode}"
      python scripts/run_dra_remote_sensing.py \
        --config "${CONFIG_PATH}" \
        --dataset resisc45 \
        --protocol hard \
        --hard_protocol "${hard_protocol}" \
        --normal_class "${normal_class}" \
        --degradation "${degradation}" \
        --memory_mode "${memory_mode}" \
        --enable_calibration \
        --threshold_protocols "${THRESHOLDS[@]}" \
        --seed "${SEED}" \
        --gpu "${gpu_id}" \
        --output_dir "${OUTPUT_DIR}" \
        2>&1 | tee "${log_path}"
    done
  done
}

run_protocol_block 1 "urban_dense" "dense_residential" "dense_residential" &
PID1=$!
run_protocol_block 2 "vegetation_forest" "forest" "forest" &
PID2=$!
run_protocol_block 3 "infrastructure_airport" "airport" "airport" &
PID3=$!

wait "${PID1}" "${PID2}" "${PID3}"
echo "All NWPU-RESISC45 hard extended runs finished."
