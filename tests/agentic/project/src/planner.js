import { parseModelFilename } from "./parseModel.js";
import { estimateRuntimeGiB } from "./memory.js";

/**
 * Check whether a model fits within the configured memory budget.
 *
 * @param {{filename:string, paramsB:number|null, quant:string|null}} model
 * @param {{vramGiB:number, ramGiB:number, maxRamShare?:number, contextK?:number}} hardware
 */
export function evaluateFit(model, hardware) {
  if (model.paramsB == null || model.quant == null) {
    return {
      ...model,
      compatible: false,
      reason: "unparseable",
      estimatedGiB: null
    };
  }

  const maxRamShare = hardware.maxRamShare ?? 0.50;
  const contextK = hardware.contextK ?? 64;

  const estimatedGiB = estimateRuntimeGiB(model, { contextK });

  const totalBudgetGiB =
    hardware.vramGiB + hardware.ramGiB * maxRamShare;

  return {
    ...model,
    compatible: estimatedGiB <= totalBudgetGiB,
    reason: estimatedGiB <= totalBudgetGiB ? "fits" : "too-large",
    estimatedGiB
  };
}

/**
 * Rank compatible models.
 *
 * Ranking rules:
 * 1. Larger total parameter count is preferred.
 * 2. If total parameter count is equal, smaller estimated runtime footprint wins.
 * 3. If still tied, filename alphabetical order wins.
 */
export function rankModels(models) {
  return [...models]
    .filter((m) => m.compatible)
    .sort((a, b) => {
      if (a.paramsB !== b.paramsB) {
        return b.paramsB - a.paramsB;
      }

      if (a.estimatedGiB !== b.estimatedGiB) {
        return b.estimatedGiB - a.estimatedGiB;
      }

      return a.filename.localeCompare(b.filename);
    });
}

/**
 * End-to-end helper.
 */
export function chooseModels(filenames, hardware) {
  const parsed = filenames.map(parseModelFilename);
  const evaluated = parsed.map((m) => evaluateFit(m, hardware));
  return rankModels(evaluated);
}
