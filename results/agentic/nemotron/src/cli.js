import { chooseModels } from "./planner.js";
import { formatCandidate } from "./format.js";
import { readFile } from "node:fs/promises";

const hardware = {
  vramGiB: 28,
  ramGiB: 64,
  maxRamShare: 0.50,
  contextK: 64
};

const raw = await readFile(new URL("../data/models.json", import.meta.url), "utf8");
const filenames = JSON.parse(raw);

const ranked = chooseModels(filenames, hardware);

console.log("Compatible models:");
for (const model of ranked) {
  console.log(formatCandidate(model));
}
