# Synthetic breast ultrasound safety study

**SYNTHETIC DATA - NOT FOR CLINICAL USE**

This repository documents the synthetic-image and AI-authenticity components
of the study:

> Clinical fidelity diagnostic utility and safety risks of synthetic breast
> ultrasound for privacy conscious research

The 300 synthetic images are distributed through Zenodo rather than GitHub.

- Dataset DOI: [`10.5281/zenodo.20684589`](https://doi.org/10.5281/zenodo.20684589)
- Dataset record: https://zenodo.org/records/20684589
- License: CC BY 4.0

## Repository contents

- `prompts/generation_prompts.csv`: base prompt for each synthetic image; the
  historical request appended a 16:9 aspect-ratio instruction.
- `prompts/authenticity_prompts.txt`: fixed Phase 2 and Phase 3 AI prompts.
- `metadata/synthetic_image_manifest.csv`: BI-RADS generation targets, file
  sizes, and SHA-256 hashes for all 300 images.
- `metadata/sha256sums.txt`: checksums in standard text format.
- `code/generate_images_gemini.py`: separate reference regeneration harness
  using the official Google Gemini API endpoint for Nano Banana Pro.
- `code/package_synthetic_dataset.py`: package and validate the image archive.
- `code/classify_authenticity.py`: environment-configured authenticity
  inference harness reproducing the historical request settings.
- `code/validate_public_repository.py`: privacy and integrity checks.

Authentic clinical images, original survey files, reader-level data,
manuscripts, submission documents, and non-AI figure programs are deliberately
excluded from this repository.

## Download and verify

Download `synthetic_breast_ultrasound_images.zip` from the Zenodo record, then:

```bash
python code/package_synthetic_dataset.py verify \
  --archive synthetic_breast_ultrasound_images.zip \
  --manifest metadata/synthetic_image_manifest.csv
```

## Reference generation call

The deposited images were generated between 26 and 30 April 2026 through an
asynchronous gateway using model designation `Nano_Banana_2_2K_0`. Historical
requests supplied the base prompt, an appended 16:9 aspect-ratio instruction
and JPEG output. No study-patient image was supplied.

The separate reference harness uses Google's official Gemini API:

```text
https://generativelanguage.googleapis.com/v1/models/gemini-3-pro-image:generateContent
```

Set `GEMINI_API_KEY`, then run:

```bash
python code/generate_images_gemini.py \
  --prompts prompts/generation_prompts.csv \
  --output-dir regenerated_images
```

The reference harness sends only prompt content in addition to the model
identifier. It does not reproduce the historical gateway request and is not
expected to reproduce the deposited file hashes.

## AI authenticity request

The historical Phase 2 and Phase 3 model calls used an OpenAI-compatible
gateway with model identifier `gpt-5.5` on 29 May and 10 June 2026,
respectively. Requests set `temperature=0`, `max_tokens=512` and image detail
to `high`. The public classifier reads its endpoint and credentials from
environment variables.

## Label interpretation

The `target_birads` field is the BI-RADS category specified before image
generation. It is not pathology ground truth and does not establish clinical
correctness.

## Privacy boundary

Study-patient images were not supplied as generation inputs. This is a
privacy-conscious release, not a formal privacy guarantee. Membership
inference, re-identification, training-data memorisation, and formal privacy
attacks were not evaluated.

## Citation

Use the dataset DOI shown above and the metadata in `CITATION.cff`.
