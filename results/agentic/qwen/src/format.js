export function formatGiB(value) {
  return `${value.toFixed(2)} GiB`;
}

export function formatCandidate(model) {
  const status = model.compatible ? "OK" : "NO";
  const size = model.estimatedGiB == null ? "n/a" : formatGiB(model.estimatedGiB);
  return `${status} | ${model.filename} | ${size}`;
}
