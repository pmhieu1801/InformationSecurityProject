# Algorithm Specification: BioVault (Basis-Matrix XOR Scheme)

- **Module Owner:** Member 2 (Mathematical & Algorithm Lead)
- **Scheme Version:** `1.0.0-xor-m2`
- **Cryptographic Scheme:** $(2,2)$ Visual Cryptography Scheme (VCS) via Basis-Matrix XOR and Subpixel Collapse.

---

## 1. Binary Secret Image Convention ($P$)
* **Spatial Dimensions:** $H \times W$ (Height $\times$ Width).
* **Data Type:** `numpy.ndarray` with `dtype = np.uint8`.
* **Value Domain:** Strictly binary $\{0, 1\}$:
  * `0`: White pixel (background).
  * `1`: Black pixel (biometric foreground pattern: fingerprint, face, or iris).

---

## 2. Basis Matrices & Pixel Expansion ($m = 2$)
The system uses a horizontal pixel expansion factor of $m = 2$. Each original secret pixel $P[i, j]$ is expanded into a $1 \times 2$ subpixel block in each share.

* **White Pixel ($P = 0$):**
  $$B_0 = \begin{bmatrix} 1 & 0 \\ 1 & 0 \end{bmatrix}$$
* **Black Pixel ($P = 1$):**
  $$B_1 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$

---

## 3. Share Generation Workflow ($S_1, S_2$)
1. **Basis Selection:** For each secret pixel $P[i, j]$, select basis matrix $B_0$ if $P[i, j] = 0$, or $B_1$ if $P[i, j] = 1$.
2. **Column Permutation:** Apply a uniform, independent random column permutation to the selected basis matrix using Python's cryptographically secure `secrets` module (`secrets.randbelow(2)`):
   * Probability $0.5$: Keep standard column order `[0, 1]`.
   * Probability $0.5$: Swap columns to `[1, 0]`.
3. **Row Distribution:** 
   * **Row 0** of the permuted basis is assigned to Share 1: `S1[i, 2*j : 2*j + 2]`.
   * **Row 1** of the permuted basis is assigned to Share 2: `S2[i, 2*j : 2*j + 2]`.
4. **Share Dimensions:** The resulting shares ($S_1$ and $S_2$) have dimensions $H \times 2W$, with `dtype = np.uint8` and values in $\{0, 1\}$.

---

## 4. Reconstruction & Subpixel Collapse Rule
1. **Input Validation:** Both $S_1$ and $S_2$ must have identical shapes ($H \times 2W$), where $2W$ is even, `dtype = np.uint8`, and binary values.
2. **Bitwise XOR Operation:**
   $$\text{XOR\_Result} = S_1 \oplus S_2 \quad (\text{Dimensions: } H \times 2W)$$
3. **Subpixel Collapse ($1 \times 2$ Blocks):** Inspect each $1 \times 2$ block in $\text{XOR\_Result}$ at positions $(i, 2j)$ and $(i, 2j+1)$:
   * Block `[0, 0]` $\rightarrow \hat{P}[i, j] = 0$ (White).
   * Block `[1, 1]` $\rightarrow \hat{P}[i, j] = 1$ (Black).
   * Any other block (`[0, 1]` or `[1, 0]`) $\rightarrow$ **Raise `InvalidSubpixelBlockError`** (indicates share corruption, phase shift, or tampering).
4. **Accuracy:** Under authentic, unmodified shares, the pixel error rate relative to the original binary image $P$ is $0$ ($\hat{P} \equiv P$).

---

## 5. Lossless PNG Codec & Security Limits
* **Lossless PNG Encoding:** Binary bits are mapped to standard grayscale pixel intensities (`0` $\to$ white `255`, `1` $\to$ black `0`) to guarantee lossless round-trip integrity without bit degradation.
* **Security Properties & Limitations:**
  * **1-Share Uniformity:** An isolated share exhibits a uniform $50\%$ probability distribution across subpixel patterns regardless of the underlying secret pixel value, resulting in zero mutual information ($I(P; S_1) = 0$).
  * **Compromise:** Simultaneous exposure of both shares fully reveals the secret image $P$.
  * **Integrity Enforcement:** Because raw XOR does not natively detect tampering if both shares are maliciously altered in tandem, the application strictly relies on M3's HMAC-SHA256 signature verification and authorization checks prior to executing the decoder.