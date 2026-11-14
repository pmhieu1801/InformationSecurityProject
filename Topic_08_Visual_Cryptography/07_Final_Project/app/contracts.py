from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
import numpy as np

class BioVaultAlgorithmError(Exception): pass
class InvalidImageFormatError(BioVaultAlgorithmError): pass
class InvalidSubpixelBlockError(BioVaultAlgorithmError): pass

@dataclass(frozen=True)
class SchemeSpec:
    scheme: str = "basis_matrix_xor"
    version: str = "1.0.0"
    expansion_m: int = 2

@dataclass
class SharePairData:
    s1_bits: np.ndarray
    s2_bits: np.ndarray
    p_shape: Tuple[int, int]
    share_shape: Tuple[int, int]
    spec: SchemeSpec = field(default_factory=SchemeSpec)

@dataclass
class VerifiedPair:
    pair_id: str
    s1_bits: np.ndarray
    s2_bits: np.ndarray
    p_shape: Tuple[int, int]
    metadata: Dict[str, Any] = field(default_factory=dict)