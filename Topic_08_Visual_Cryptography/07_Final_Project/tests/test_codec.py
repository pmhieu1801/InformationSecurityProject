import numpy as np
import pytest
from app.core.share_codec import bits_to_png_bytes, png_bytes_to_bits

def test_png_codec_roundtrip():
    # Create a random binary bit array
    original_bits = np.random.randint(0, 2, size=(64, 128), dtype=np.uint8)
    
    # Convert to PNG bytes and back
    png_bytes = bits_to_png_bytes(original_bits)
    recovered_bits = png_bytes_to_bits(png_bytes)
    
    # Ensure zero bit loss (lossless round-trip)
    np.testing.assert_array_equal(original_bits, recovered_bits)