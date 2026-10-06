import test from "node:test";
import assert from "node:assert/strict";
import { evaluateFit, rankModels, chooseModels } from "../src/planner.js";

test("evaluateFit marks a model compatible within the memory budget", () => {
  const model = {
    filename: "TinyCoder-7B-Q8_0.gguf",
    name: "TinyCoder",
    paramsB: 7,
    activeB: null,
    quant: "Q8_0"
  };

  const result = evaluateFit(model, {
    vramGiB: 8,
    ramGiB: 16,
    maxRamShare: 0.5,
    contextK: 64
  });

  assert.equal(result.compatible, true);
  assert.equal(result.reason, "fits");
});

test("evaluateFit rejects a model that exceeds the total budget", () => {
  const model = {
    filename: "Huge-70B-Q8_0.gguf",
    name: "Huge",
    paramsB: 70,
    activeB: null,
    quant: "Q8_0"
  };

  const result = evaluateFit(model, {
    vramGiB: 8,
    ramGiB: 8,
    maxRamShare: 0.25,
    contextK: 64
  });

  assert.equal(result.compatible, false);
  assert.equal(result.reason, "too-large");
});

test("rankModels prefers larger models first", () => {
  const ranked = rankModels([
    { filename: "A.gguf", paramsB: 7, estimatedGiB: 5, compatible: true },
    { filename: "B.gguf", paramsB: 13, estimatedGiB: 9, compatible: true }
  ]);

  assert.equal(ranked[0].filename, "B.gguf");
});

test("rankModels prefers smaller footprint when parameter counts tie", () => {
  const ranked = rankModels([
    { filename: "LargeFootprint.gguf", paramsB: 13, estimatedGiB: 9, compatible: true },
    { filename: "SmallFootprint.gguf", paramsB: 13, estimatedGiB: 7, compatible: true }
  ]);

  assert.equal(ranked[0].filename, "SmallFootprint.gguf");
});

test("rankModels uses filename as final deterministic tie-break", () => {
  const ranked = rankModels([
    { filename: "Zeta.gguf", paramsB: 13, estimatedGiB: 7, compatible: true },
    { filename: "Alpha.gguf", paramsB: 13, estimatedGiB: 7, compatible: true }
  ]);

  assert.equal(ranked[0].filename, "Alpha.gguf");
});

test("chooseModels parses, filters and ranks end to end", () => {
  const ranked = chooseModels(
    [
      "TinyCoder-7B-Q8_0.gguf",
      "Medium-13B-Q4_K_M.gguf"
    ],
    {
      vramGiB: 16,
      ramGiB: 32,
      maxRamShare: 0.5,
      contextK: 64
    }
  );

  assert.equal(ranked.length, 2);
  assert.equal(ranked[0].paramsB, 13);
});
