#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="configs/patchcore_remote_sensing.yaml"
RESULT_ROOT="outputs/remote_sensing/results"
LOG_ROOT="logs/eurosat_hard_coreset_sensitivity"
SEED=42
THRESHOLDS=(clean_fixed corruption_agnostic)
DEGRADATIONS=(noise blur light lowres jpeg)
MEMORIES=(clean mixed)

cd "${REPO_ROOT}"
mkdir -p "${LOG_ROOT}"

if [[ "$#" -gt 0 ]]; then
  RATIOS=("$@")
else
  RATIOS=("0.01")
fi

ratio_tag() {
  python - "$1" <<'PY'
import sys
value = float(sys.argv[1])
print(f"core{int(round(value * 100)):03d}")
PY
}

ratio_output_dir() {
  local ratio="$1"
  local tag
  tag="$(ratio_tag "${ratio}")"
  if [[ "${tag}" == "core010" ]]; then
    echo "${RESULT_ROOT}/eurosat_hard_main"
  else
    echo "${RESULT_ROOT}/eurosat_hard_${tag}"
  fi
}

ratio_output_tag() {
  local ratio="$1"
  local tag
  tag="$(ratio_tag "${ratio}")"
  if [[ "${tag}" == "core010" ]]; then
    echo ""
  else
    echo "${tag}"
  fi
}

run_protocol_block() {
  local ratio="$1"
  local gpu_id="$2"
  local hard_protocol="$3"
  local normal_class="$4"
  local normal_tag="$5"
  local output_dir="$6"
  local output_tag="$7"
  local ratio_tag_name
  ratio_tag_name="$(ratio_tag "${ratio}")"
  local log_dir="${LOG_ROOT}/${ratio_tag_name}"

  mkdir -p "${output_dir}" "${log_dir}"

  for degradation in "${DEGRADATIONS[@]}"; do
    for memory_mode in "${MEMORIES[@]}"; do
      local log_path="${log_dir}/${normal_tag}_${hard_protocol}_${degradation}_${memory_mode}.log"
      echo "==> ${ratio_tag_name} | GPU${gpu_id} | ${hard_protocol} | ${degradation} | ${memory_mode}"
      if [[ -n "${output_tag}" ]]; then
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
          --coreset_sampling_ratio "${ratio}" \
          --gpu "${gpu_id}" \
          --output_tag "${output_tag}" \
          --output_dir "${output_dir}" \
          2>&1 | tee "${log_path}"
      else
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
          --coreset_sampling_ratio "${ratio}" \
          --gpu "${gpu_id}" \
          --output_dir "${output_dir}" \
          2>&1 | tee "${log_path}"
      fi
    done
  done
}

for ratio in "${RATIOS[@]}"; do
  tag="$(ratio_tag "${ratio}")"
  output_dir="$(ratio_output_dir "${ratio}")"
  output_tag="$(ratio_output_tag "${ratio}")"

  run_protocol_block "${ratio}" 1 "vegetation_forest" "Forest" "forest" "${output_dir}" "${output_tag}" &
  PID1=$!
  run_protocol_block "${ratio}" 2 "urban_residential" "Residential" "residential" "${output_dir}" "${output_tag}" &
  PID2=$!
  run_protocol_block "${ratio}" 3 "water_sealake" "SeaLake" "sealake" "${output_dir}" "${output_tag}" &
  PID3=$!

  wait "${PID1}" "${PID2}" "${PID3}"
  echo "Finished EuroSAT-Hard coreset runs for ${tag}."

  python scripts/summarize_eurosat_hard_main.py \
    --input_dir "${output_dir}" \
    --output_csv "${output_dir}/final_summary.csv" \
    --output_md "${output_dir}/final_summary.md"

  python scripts/profile_remote_sensing_runtime_memory.py \
    --config "${CONFIG_PATH}" \
    --eurosat_result_dir "${output_dir}" \
    --resisc45_result_dir "${RESULT_ROOT}/resisc45_hard_extended" \
    --output_csv "${output_dir}/runtime_profile.csv" \
    --output_md "${output_dir}/runtime_profile.md"
done

python scripts/summarize_eurosat_hard_coreset_sensitivity.py

echo "All requested EuroSAT-Hard coreset sensitivity runs finished."
