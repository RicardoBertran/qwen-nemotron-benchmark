# Local Model Planner

Small CLI/library for choosing a local GGUF model for a machine with limited VRAM/RAM.

## What it does

Given a list of model filenames and hardware limits, it:

1. parses GGUF-style filenames,
2. estimates the memory footprint,
3. checks whether each model can run,
4. ranks compatible models.

## Run tests

```bash
npm test
```

## Run the demo

```bash
npm start
```

The tests are the specification. Do not modify them.
