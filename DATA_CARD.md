# Dataset card

## Safety notice

**SYNTHETIC DATA - NOT FOR CLINICAL USE**

These files are research material. They must not be used for diagnosis,
treatment decisions, clinical triage, or replacement of ultrasound
acquisition.

## Dataset

The release contains 300 text-generated, single-view breast ultrasound-style
images. Each image has a prespecified BI-RADS generation target, base prompt,
file size, and SHA-256 checksum.

The images were generated between 26 and 30 April 2026 with Nano Banana Pro
through an asynchronous image-generation gateway (gateway model designation
`Nano_Banana_2_2K_0`). No study patient image was supplied as a generation
input. Historical requests supplied the base prompt, an appended 16:9
aspect-ratio instruction and JPEG output. No seed or temperature parameter was
supplied.

The public Google Gemini script is a separate reference harness requested for
future regeneration experiments. It targets Google's official Gemini API
endpoint and the `gemini-3-pro-image` model, but it is not the historical
gateway used to create the deposited files. Regeneration is stochastic and is
not expected to reproduce the deposited file hashes.

## Intended use

- Synthetic-image fidelity and provenance research.
- Authenticity-detection research.
- Research-only AI method development.
- Dataset governance and reader-education research.

## Prohibited or discouraged use

- Clinical diagnosis, treatment, or patient management.
- Presentation of synthetic files as authentic clinical examinations.
- Removal of provenance labels or safety notices.
- Claims that BI-RADS generation targets are pathology ground truth.

## Privacy and governance limitations

The release does not claim differential privacy or protection against
membership inference, re-identification, or training-data memorisation. The
generator training corpus was proprietary and unavailable for audit. Privacy
assurance therefore depends on provenance documentation, persistent synthetic
labels, versioned hashes, release governance, and downstream use controls.

## Provenance

The data card documents the generation process, intended research-only use,
known privacy limitations, prohibited clinical use, provenance labels, and
recommended citation and reporting requirements.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).
