import numpy as np
from app.contracts import VerifiedPair, InvalidSubpixelBlockError, InvalidImageFormatError

def reconstruct(verified_pair: VerifiedPair) -> np.ndarray:
    """
    Performs bitwise XOR on S1 and S2, then collapses subpixel blocks (m = 2) to recover P_hat.
    """
    s1 = verified_pair.s1_bits
    s2 = verified_pair.s2_bits
    H, W_share = s1.shape

    if s1.shape != s2.shape:
        raise InvalidImageFormatError("Dimensions of S1 and S2 do not match.")

    if W_share % 2 != 0:
        raise InvalidImageFormatError("Share width must be an even number (m = 2 expansion).")

    W = W_share // 2
    p_hat = np.zeros((H, W), dtype=np.uint8)
    xor_result = np.bitwise_xor(s1, s2)

    for y in range(H):
        for x in range(W):
            block = tuple(xor_result[y, 2 * x : 2 * x + 2])
            
            if block == (0, 0):
                p_hat[y, x] = 0  # White
            elif block == (1, 1):
                p_hat[y, x] = 1  # Black
            else:
                raise InvalidSubpixelBlockError(
                    f"Invalid subpixel block detected {block} at position ({y}, {x}). "
                    "The shares might have been tampered with or mismatch."
                )

    return p_hat