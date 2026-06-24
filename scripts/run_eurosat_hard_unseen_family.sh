#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="configs/patchcore_remote_sensing.yaml"
OUTPUT_ROOT="outputs/remote_sensing/results/eurosat_hard_unseen_family"
LOG_ROOT="logs/eurosat_hard_unseen_family"
SEED=42
THRESHOLDS=(clean_fixed corruption_agnostic)
MEMORIES=(clean mixed)
FAMILIES=(haze cloudveil)

cd "${REPO_ROOT}"
mkdir -p "${OUTPUT_ROOT}" "${LOG_ROOT}"

run_family_block() {
  local family="$1"
  local gpu_id="$2"
  local hard_protocol="$3"
  local normal_class="$4"
  local normal_tag="$5"
  local output_dir="${OUTPUT_ROOT}/${family}"
  local log_dir="${LOG_ROOT}/${family}"

  mkdir -p "${output_dir}" "${log_dir}"

  for memory_mode in "${MEMORIES[@]}"; do
    local log_path="${log_dir}/${normal_tag}_${hard_protocol}_${memory_mode}.log"
    echo "==> ${family} | GPU${gpu_id} | ${hard_protocol} | ${memory_mode}"
    python scripts/run_dra_remote_sensing.py \
      --config "${CONFIG_PATH}" \
      --dataset eurosat \
      --protocol hard \
      --hard_protocol "${hard_protocol}" \
      --normal_class "${normal_class}" \
      --degradation "${family}" \
      --memory_mode "${memory_mode}" \
      --enable_calibration \
      --threshold_protocols "${THRESHOLDS[@]}" \
      --seed "${SEED}" \
      --gpu "${gpu_id}" \
      --memory_severity 1.0 \
      --eval_severity 1.0 \
      --output_tag "${family}" \
      --output_dir "${output_dir}" \
      2>&1 | tee "${log_path}"
  done
}

for family in "${FAMILIES[@]}"; do
  run_family_block "${family}" 1 "vegetation_forest" "Forest" "forest" &
  PID1=$!
  run_family_block "${family}" 2 "urban_residential" "Residential" "residential" &
  PID2=$!
  run_family_block "${family}" 3 "water_sealake" "SeaLake" "sealake" &
  PID3=$!
  wait "${PID1}" "${PID2}" "${PID3}"
  echo "Finished unseen-family block: ${family}."
done

echo "All EuroSAT-Hard unseen-family runs finished."
