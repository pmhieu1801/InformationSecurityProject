import time
import os
import csv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from app.core.encoder import generate
from app.core.decoder import reconstruct
from app.contracts import VerifiedPair

def run_benchmark():
    print("=== BioVault M2 Algorithm Benchmark ===")
    dimensions = [(64, 64), (128, 128), (256, 256), (512, 512)]
    results = []

    os.makedirs("evidence/algorithm", exist_ok=True)

    for h, w in dimensions:
        P = np.random.randint(0, 2, size=(h, w), dtype=np.uint8)
        
        # Measure Generation Time
        start_gen = time.time()
        share_data = generate(P)
        gen_time = time.time() - start_gen
        
        verified = VerifiedPair(
            pair_id=f"bm_{h}x{w}",
            s1_bits=share_data.s1_bits,
            s2_bits=share_data.s2_bits,
            p_shape=P.shape
        )
        
        # Measure Reconstruction Time
        start_dec = time.time()
        p_hat = reconstruct(verified)
        dec_time = time.time() - start_dec
        
        # Calculate Pixel Error
        pixel_error = int(np.sum(P != p_hat))
        
        results.append({
            "Resolution": f"{h}x{w}",
            "Gen_Time_sec": round(gen_time, 5),
            "Dec_Time_sec": round(dec_time, 5),
            "Pixel_Error": pixel_error,
            "Share_Shape": f"{h}x{w*2}"
        })
        print(f"Res: {h}x{w} | Gen: {gen_time:.4f}s | Dec: {dec_time:.4f}s | Error: {pixel_error}")

    # Export to CSV
    csv_path = "evidence/algorithm/benchmark_results.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Resolution", "Gen_Time_sec", "Dec_Time_sec", "Pixel_Error", "Share_Shape"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Benchmark results successfully saved to {csv_path}")

if __name__ == "__main__":
    run_benchmark()