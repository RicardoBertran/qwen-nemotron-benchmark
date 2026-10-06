const QUANT_PATTERN = /(Q\d(?:_[A-Z0-9]+)*)/i;

/**
 * Parse a GGUF-like filename.
 *
 * Examples:
 *   Qwen3.6-35B-A3B-Q4_K_M.gguf
 *   Nemotron-3.5-Lightning-30B-A3B-NVFP4.gguf
 *
 * @param {string} filename
 * @returns {{filename:string, name:string, paramsB:number|null, activeB:number|null, quant:string|null}}
 */
export function parseModelFilename(filename) {
  const base = filename.replace(/\.gguf$/i, "");

  const paramsMatch = base.match(/(?:^|[-_])(\d+(?:\.\d+)?)B(?:[-_]|$)/i);
  const activeMatch = base.match(/A(\d+(?:\.\d+)?)B/i);
  const quantMatch = base.match(QUANT_PATTERN);

  let name = base;

  if (paramsMatch) {
    name = name.replace(paramsMatch[0], "-");
  }

  if (activeMatch) {
    name = name.replace(activeMatch[0], "");
  }

  if (quantMatch) {
    name = name.replace(quantMatch[0], "");
  }

  name = name
    .replace(/[-_]{2,}/g, "-")
    .replace(/^[-_]+|[-_]+$/g, "")
    .trim();

  return {
    filename,
    name,
    paramsB: paramsMatch ? Number(paramsMatch[1]) : null,
    activeB: activeMatch ? Number(activeMatch[1]) : null,
    quant: quantMatch ? quantMatch[1].toUpperCase() : null
  };
}
