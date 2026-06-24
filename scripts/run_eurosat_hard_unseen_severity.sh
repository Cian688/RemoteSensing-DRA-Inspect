#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="configs/patchcore_remote_sensing.yaml"
OUTPUT_ROOT="outputs/remote_sensing/results/eurosat_hard_unseen_severity"
LOG_ROOT="logs/eurosat_hard_unseen_severity"
SEED=42
THRESHOLDS=(clean_fixed corruption_agnostic)
MEMORIES=(clean mixed)

declare -A MILD_SEVERITY=(
  [noise]="0.5"
  [blur]="0.6667"
  [light]="0.6"
  [lowres]="0.0"
  [jpeg]="0.3333"
)

declare -A SEVERE_SEVERITY=(
  [noise]="1.5"
  [blur]="1.6667"
  [light]="1.4"
  [lowres]="2.0"
  [jpeg]="1.5"
)

cd "${REPO_ROOT}"
mkdir -p "${OUTPUT_ROOT}" "${LOG_ROOT}"

run_protocol_block() {
  local setting="$1"
  local gpu_id="$2"
  local hard_protocol="$3"
  local normal_class="$4"
  local normal_tag="$5"
  local output_dir="${OUTPUT_ROOT}/${setting}"
  local log_dir="${LOG_ROOT}/${setting}"

  mkdir -p "${output_dir}" "${log_dir}"

  for degradation in noise blur light lowres jpeg; do
    local eval_severity=""
    if [[ "${setting}" == "mild" ]]; then
      eval_severity="${MILD_SEVERITY[${degradation}]}"
    else
      eval_severity="${SEVERE_SEVERITY[${degradation}]}"
    fi
    for memory_mode in "${MEMORIES[@]}"; do
      local log_path="${log_dir}/${normal_tag}_${hard_protocol}_${degradation}_${memory_mode}.log"
      echo "==> ${setting} | GPU${gpu_id} | ${hard_protocol} | ${degradation} | ${memory_mode} | eval_sev=${eval_severity}"
      python scripts/run_dra_remote_sensing.py \
        --config "${CONFIG_PATH}" \
        --dataset eurosat \
        --protocol hard \
        --hard_protocol "${hard_protocol}" \
        --normal_class "${normal_class}" \
        --degradation "${degradation}" \
        --memory_mode "${memory_mode}" \
        --enable_calibration \
        --threshold_protocols "${THRESHOLDS[@]}" \
        --seed "${SEED}" \
        --memory_severity 1.0 \
        --eval_severity "${eval_severity}" \
        --gpu "${gpu_id}" \
        --output_tag "${setting}" \
        --output_dir "${output_dir}" \
        2>&1 | tee "${log_path}"
    done
  done
}

for setting in mild severe; do
  run_protocol_block "${setting}" 1 "vegetation_forest" "Forest" "forest" &
  PID1=$!
  run_protocol_block "${setting}" 2 "urban_residential" "Residential" "residential" &
  PID2=$!
  run_protocol_block "${setting}" 3 "water_sealake" "SeaLake" "sealake" &
  PID3=$!
  wait "${PID1}" "${PID2}" "${PID3}"
  echo "Finished unseen-severity block: ${setting}."
done

echo "All EuroSAT-Hard unseen-severity runs finished."
