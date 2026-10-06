import test from "node:test";
import assert from "node:assert/strict";
import { parseModelFilename } from "../src/parseModel.js";

test("parses Q4_K_M exactly", () => {
  const result = parseModelFilename("Qwen3.6-35B-A3B-Q4_K_M.gguf");

  assert.equal(result.paramsB, 35);
  assert.equal(result.activeB, 3);
  assert.equal(result.quant, "Q4_K_M");
});

test("parses Q8_0 exactly", () => {
  const result = parseModelFilename("TinyCoder-7B-Q8_0.gguf");

  assert.equal(result.paramsB, 7);
  assert.equal(result.quant, "Q8_0");
});

test("does not invent a Q quantization for NVFP4", () => {
  const result = parseModelFilename("Nemotron-3.5-Lightning-30B-A3B-NVFP4.gguf");

  assert.equal(result.paramsB, 30);
  assert.equal(result.activeB, 3);
  assert.equal(result.quant, null);
});
