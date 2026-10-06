import test from "node:test";
import assert from "node:assert/strict";
import { estimateWeightGiB, estimateRuntimeGiB } from "../src/memory.js";

const GiB = 1024 ** 3;

test("converts Q4_K_M weight bytes to GiB", () => {
  const expected = (35 * 1_000_000_000 * 0.56) / GiB;
  const actual = estimateWeightGiB(35, "Q4_K_M");

  assert.ok(Math.abs(actual - expected) < 1e-9);
});

test("runtime estimate includes context-scaled KV cache and overhead", () => {
  const expectedWeights = (7 * 1_000_000_000 * 1.0) / GiB;
  const expected = expectedWeights + 3.0 + 1.0;

  const actual = estimateRuntimeGiB(
    { paramsB: 7, quant: "Q8_0" },
    { contextK: 128, kvGiBPer64K: 1.5, overheadGiB: 1.0 }
  );

  assert.ok(Math.abs(actual - expected) < 1e-9);
});

test("rejects unsupported quantization", () => {
  assert.throws(
    () => estimateWeightGiB(30, "UNKNOWN"),
    /Unsupported quantization/
  );
});
