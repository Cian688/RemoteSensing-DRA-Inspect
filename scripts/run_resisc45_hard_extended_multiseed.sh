#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="configs/patchcore_remote_sensing.yaml"
OUTPUT_ROOT="outputs/remote_sensing/results/resisc45_hard_extended_multiseed"
LOG_ROOT="logs/resisc45_hard_extended_multiseed"
SEEDS=(42 43 45)
THRESHOLDS=(clean_fixed corruption_agnostic)
DEGRADATIONS=(noise blur light lowres jpeg)
MEMORIES=(clean mixed)

cd "${REPO_ROOT}"
mkdir -p "${OUTPUT_ROOT}" "${LOG_ROOT}"

run_protocol_block() {
  local seed="$1"
  local gpu_id="$2"
  local hard_protocol="$3"
  local normal_class="$4"
  local normal_tag="$5"
  local output_dir="${OUTPUT_ROOT}/seed_${seed}"
  local log_dir="${LOG_ROOT}/seed_${seed}"

  mkdir -p "${output_dir}" "${log_dir}"

  for degradation in "${DEGRADATIONS[@]}"; do
    for memory_mode in "${MEMORIES[@]}"; do
      local log_path="${log_dir}/${normal_tag}_${hard_protocol}_${degradation}_${memory_mode}.log"
      echo "==> seed=${seed} | GPU${gpu_id} | ${hard_protocol} | ${degradation} | ${memory_mode}"
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
        --seed "${seed}" \
        --gpu "${gpu_id}" \
        --output_dir "${output_dir}" \
        2>&1 | tee "${log_path}"
    done
  done
}

for seed in "${SEEDS[@]}"; do
  run_protocol_block "${seed}" 1 "urban_dense" "dense_residential" "dense_residential" &
  PID1=$!
  run_protocol_block "${seed}" 2 "vegetation_forest" "forest" "forest" &
  PID2=$!
  run_protocol_block "${seed}" 3 "infrastructure_airport" "airport" "airport" &
  PID3=$!
  wait "${PID1}" "${PID2}" "${PID3}"
  echo "Finished NWPU-Hard extended multiseed block for seed=${seed}."
done

echo "All NWPU-RESISC45 hard extended multiseed runs finished."
