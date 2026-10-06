const BYTES_PER_PARAM = {
  Q2_K: 0.34,
  Q3_K_M: 0.45,
  Q4_0: 0.50,
  Q4_K_M: 0.56,
  Q5_K_M: 0.68,
  Q6_K: 0.82,
  Q8_0: 1.00,
  F16: 2.00,
  NVFP4: 0.50
};

/**
 * Estimate model weight memory in GiB.
 * This is deliberately approximate; the tests define the expected formula.
 *
 * @param {number} paramsB billions of parameters
 * @param {string} quant
 */
export function estimateWeightGiB(paramsB, quant) {
  if (!Number.isFinite(paramsB) || paramsB <= 0) {
    throw new Error("paramsB must be a positive number");
  }

  const bytesPerParam = BYTES_PER_PARAM[quant];

  if (!bytesPerParam) {
    throw new Error(`Unsupported quantization: ${quant}`);
  }

  const bytes = paramsB * 1_000_000_000 * bytesPerParam;

  // convert bytes to GiB
  return bytes / 1_000_000_000;
}

/**
 * Estimate total runtime footprint.
 *
 * @param {{paramsB:number, quant:string}} model
 * @param {{contextK:number, kvGiBPer64K:number, overheadGiB:number}} options
 */
export function estimateRuntimeGiB(model, options = {}) {
  const {
    contextK = 64,
    kvGiBPer64K = 1.5,
    overheadGiB = 1.0
  } = options;

  const weights = estimateWeightGiB(model.paramsB, model.quant);
  const kv = kvGiBPer64K * (contextK / 64);

  return weights + kv + overheadGiB;
}
