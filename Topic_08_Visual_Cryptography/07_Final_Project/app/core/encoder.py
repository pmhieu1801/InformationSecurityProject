import numpy as np
from app.core.basis import B0, B1, get_random_permutation_columns
from app.contracts import SharePairData, SchemeSpec

def generate(P: np.ndarray) -> SharePairData:
    """
    Takes a binary secret image P of size H x W (uint8 {0, 1}),
    and generates shares S1 and S2 using basis-matrix XOR with horizontal expansion m = 2.
    """
    if P.ndim != 2:
        raise ValueError("Input image P must be a 2D array (grayscale/binary).")
    
    H, W = P.shape
    s1_bits = np.zeros((H, 2 * W), dtype=np.uint8)
    s2_bits = np.zeros((H, 2 * W), dtype=np.uint8)

    for y in range(H):
        for x in range(W):
            pixel_val = P[y, x]
            base = B0 if pixel_val == 0 else B1
            permuted_basis = get_random_permutation_columns(base)
            
            s1_bits[y, 2 * x : 2 * x + 2] = permuted_basis[0, :]
            s2_bits[y, 2 * x : 2 * x + 2] = permuted_basis[1, :]

    return SharePairData(
        s1_bits=s1_bits,
        s2_bits=s2_bits,
        p_shape=(H, W),
        share_shape=(H, 2 * W),
        spec=SchemeSpec()
    )