import streamlit as st
import json
from app.contracts import VerifiedPair
from app.core.decoder import reconstruct
from app.core.share_codec import png_bytes_to_bits

st.title("Image Reconstruction Lab")
st.write("Tải lên gói share (.bvshare) và nhập token để khôi phục ảnh sinh trắc học.")

uploaded_file = st.file_uploader("Tải gói S1 (.bvshare hoặc JSON)", type=["json", "bvshare"])
token_input = st.text_input("Nhập Access Token", type="password")

if st.button("Khôi phục ảnh"):
    if uploaded_file and token_input:
        try:
            data = json.load(uploaded_file)
            s1_bits = png_bytes_to_bits(bytes.fromb64(data["s1_png_base64"]))
            # (Mock gọi verify từ M3 hoặc tích hợp thực tế tại đây)
            verified = VerifiedPair(
                pair_id=data.get("pair_id", "mock_id"),
                s1_bits=s1_bits,
                s2_bits=np.zeros_like(s1_bits), # Sẽ lấy từ vault server của M3 khi ghép module
                p_shape=tuple(data["p_shape"])
            )
            # Thực thi reconstruct
            p_hat = reconstruct(verified)
            st.success("Khôi phục thành công!")
            st.image((1 - p_hat) * 255, caption="Ảnh khôi phục P_hat", use_column_width=True)
        except Exception as e:
            st.error(f"Lỗi khôi phục: {e}")
    else:
            st.warning("Vui lòng tải lên file share và nhập token hợp lệ.")