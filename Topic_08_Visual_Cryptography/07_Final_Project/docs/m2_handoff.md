# M2 Handoff Documentation: Algorithm & Reconstruction Module

- **Owner:** Member 2 (Mathematical & Algorithm Lead)
- **Phase:** Final MVP Integration

---

## 1. Overview of Delivered Modules
* **`app/core/basis.py`**: Defines basis matrices $B_0, B_1$ and secure random column permutation using `secrets`.
* **`app/core/encoder.py`**: Implements `generate(P)` returning `SharePairData` ($H \times 2W$ shares).
* **`app/core/decoder.py`**: Implements `reconstruct(VerifiedPair)` performing bitwise XOR and subpixel collapse with strict error checking (`InvalidSubpixelBlockError`).
* **`app/core/share_codec.py`**: Handles lossless PNG conversion (`bits_to_png_bytes` and `png_bytes_to_bits`).
* **`app/pages/reconstruct.py`**: Streamlit UI page for uploading share packages and decrypting upon successful verification.

---

## 2. API Usage Guide for Teammates

### For M1 (Preprocessing / Protect Flow):
Call the encoder directly after obtaining the binary secret image $P$:
```python
from app.core.encoder import generate

# P is numpy.ndarray of shape (H, W), dtype=uint8 {0, 1}
share_data = generate(P)
# Returns SharePairData containing s1_bits, s2_bits, p_shape, and spec