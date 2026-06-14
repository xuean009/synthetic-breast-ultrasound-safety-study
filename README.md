# Synthetic breast ultrasound safety study

**SYNTHETIC DATA - NOT FOR CLINICAL USE**

This repository documents the synthetic-image and AI-authenticity components
of the study:

> Clinical fidelity diagnostic utility and safety risks of synthetic breast
> ultrasound for privacy conscious research

The 300 synthetic images are distributed through Zenodo rather than GitHub.

- Dataset DOI: `ZENODO_DOI_PENDING`
- Dataset record: `ZENODO_URL_PENDING`
- License: CC BY 4.0

## Repository contents

- `prompts/generation_prompts.csv`: exact prompt for each synthetic image.
- `prompts/authenticity_prompts.txt`: fixed Phase 2 and Phase 3 AI prompts.
- `metadata/synthetic_image_manifest.csv`: BI-RADS generation targets, file
  sizes, and SHA-256 hashes for all 300 images.
- `metadata/sha256sums.txt`: checksums in standard text format.
- `code/package_synthetic_dataset.py`: package and validate the image archive.
- `code/classify_authenticity.py`: credential-free reference inference harness.
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

