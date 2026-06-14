# Dataset card

## Safety notice

**SYNTHETIC DATA - NOT FOR CLINICAL USE**

These files are research material. They must not be used for diagnosis,
treatment decisions, clinical triage, or replacement of ultrasound
acquisition.

## Dataset

The release contains 300 text-generated, single-view breast ultrasound-style
images. Each image has a prespecified BI-RADS generation target, exact prompt,
file size, and SHA-256 checksum.

The images were generated with Gemini 3 Pro Image (Nano Banana Pro). No study
patient image was supplied as a generation input. Apart from prompt content,
the official API defaults were used. The API call dates remain to be reported
in the associated article.

The public reference harness targets Google's official Gemini API endpoint and
the `gemini-3-pro-image` model. Regeneration is stochastic and is not expected
to reproduce the deposited file hashes.

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
