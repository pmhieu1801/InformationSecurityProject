import cv2
import numpy as np

def bits_to_png_bytes(bits: np.ndarray) -> bytes:
    img_array = (1 - bits) * 255
    success, encoded = cv2.imencode('.png', img_array.astype(np.uint8))
    if not success:
        raise ValueError("Lỗi mã hóa PNG lossless.")
    return encoded.tobytes()

def png_bytes_to_bits(png_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(png_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Lỗi đọc bytes PNG.")
    return (img < 128).astype(np.uint8)