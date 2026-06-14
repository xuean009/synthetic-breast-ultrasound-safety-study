# Data dictionary

## `metadata/synthetic_image_manifest.csv`

- `synthetic_id`: stable public identifier.
- `filename`: filename in the Zenodo image archive.
- `target_birads`: prespecified BI-RADS generation target.
- `generation_prompt`: exact text prompt used to request the image.
- `sha256`: SHA-256 checksum of the deposited file.
- `bytes`: file size in bytes.

## `prompts/generation_prompts.csv`

- `synthetic_id`: stable public identifier.
- `filename`: expected output filename.
- `target_birads`: prespecified generation target.
- `generation_prompt`: exact generation prompt.

The BI-RADS field is a generation target, not pathology ground truth.

