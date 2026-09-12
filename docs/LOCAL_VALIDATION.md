# Independent validation status

Base: 6a03298066e1a4846a20cd4229e2ee811a49c440, user fork of zhengyidong135/nnunet.
This is an HVM derivative, not a newly validated official nnU-Net distribution.

The unsafe batch header replacement path is disabled. The callable copy operation
only accepts matching 3D grids, refuses different grids and existing output files,
and saves the source image without replacing its header from the target.

Synthetic tests now cover NIfTI round-trip values, dtype, affine, translated-target
rejection with no output, and source/output byte preservation on overwrite attempts.
These are bounded geometric and synthetic I/O checks, not full imaging validation.

Before any model evaluation:

1. Pin environment, model-weight hash/license/source, dataset version and label mapping.
2. Confirm approved data location; no patient identifiers in Git or general cloud.
3. Define patient-level training/validation/test split and check overlap with HVM/model training.
4. Specify baseline, held-out external cohort, metrics (including structure-level failures),
   and blinded expert visual QA before looking at test results.
5. Validate NIfTI IO, voxel spacing/orientation, qform/sform consistency and explicit registration.
6. Run inference and quantitative evaluation only after those inputs are available.

No weights or datasets downloaded. No GPU training/inference run. No clinical-use claim.
