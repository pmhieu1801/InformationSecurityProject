import secrets
import numpy as np

B0 = np.array([[1, 0], [1, 0]], dtype=np.uint8)
B1 = np.array([[1, 0], [0, 1]], dtype=np.uint8)

def get_random_permutation_columns(basis_matrix: np.ndarray) -> np.ndarray:
    col_perm = basis_matrix.copy()
    if secrets.randbelow(2) == 1:
        col_perm = col_perm[:, [1, 0]]
    return col_perm

#### 4. File `app/core/encoder.py` (Hàm `generate(P)`)
import numpy as np
from app.core.basis import B0, B1, get_random_permutation_columns
from app.contracts import SharePairData, SchemeSpec

def generate(P: np.ndarray) -> SharePairData:
    if P.ndim != 2:
        raise ValueError("Ảnh đầu vào P phải là ảnh 2 chiều.")
    H, W = P.shape
    s1_bits = np.zeros((H, 2 * W), dtype=np.uint8)
    s2_bits = np.zeros((H, 2 * W), dtype=np.uint8)

    for y in range(H):
        for x in range(W):
            base = B0 if P[y, x] == 0 else B1
            permuted = get_random_permutation_columns(base)
            s1_bits[y, 2 * x : 2 * x + 2] = permuted[0, :]
            s2_bits[y, 2 * x : 2 * x + 2] = permuted[1, :]

    return SharePairData(
        s1_bits=s1_bits, s2_bits=s2_bits,
        p_shape=(H, W), share_shape=(H, 2 * W),
        spec=SchemeSpec()
    )


#### 5. File `app/core/decoder.py` (Hàm `reconstruct()`)

import numpy as np
from app.contracts import VerifiedPair, InvalidSubpixelBlockError, InvalidImageFormatError

def reconstruct(verified_pair: VerifiedPair) -> np.ndarray:
    s1, s2 = verified_pair.s1_bits, verified_pair.s2_bits
    if s1.shape != s2.shape:
        raise InvalidImageFormatError("Kích thước S1 và S2 không khớp.")
    H, W_share = s1.shape
    if W_share % 2 != 0:
        raise InvalidImageFormatError("Chiều rộng share phải là số chẵn.")
    
    W = W_share // 2
    p_hat = np.zeros((H, W), dtype=np.uint8)
    xor_result = np.bitwise_xor(s1, s2)

    for y in range(H):
        for x in range(W):
            block = tuple(xor_result[y, 2 * x : 2 * x + 2])
            if block == (0, 0):
                p_hat[y, x] = 0
            elif block == (1, 1):
                p_hat[y, x] = 1
            else:
                raise InvalidSubpixelBlockError(f"Block subpixel không hợp lệ: {block}")
    return p_hat