import numpy as np
import pytest
from app.core.encoder import generate
from app.core.decoder import reconstruct
from app.contracts import VerifiedPair, InvalidSubpixelBlockError

def test_encoder_decoder_roundtrip():
    # Test with a simple 2x2 binary matrix
    P = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    
    share_data = generate(P)
    assert share_data.share_shape == (2, 4)
    
    verified = VerifiedPair(
        pair_id="test_id",
        s1_bits=share_data.s1_bits,
        s2_bits=share_data.s2_bits,
        p_shape=share_data.p_shape
    )
    
    p_hat = reconstruct(verified)
    # Pixel error must be 0
    np.testing.assert_array_equal(P, p_hat)

def test_invalid_subpixel_block():
    # Tạo XOR ra block không hợp lệ ([1, 0] hoặc [0, 1])
    s1 = np.array([[1, 0, 0, 0]], dtype=np.uint8)
    s2 = np.array([[1, 0, 1, 0]], dtype=np.uint8) # XOR ra [0, 0, 1, 0] -> block thứ 2 là [1, 0] (không hợp lệ)
    
    verified = VerifiedPair(
        pair_id="test_error",
        s1_bits=s1,
        s2_bits=s2,
        p_shape=(1, 2)
    )
    
    with pytest.raises(InvalidSubpixelBlockError):
        reconstruct(verified)