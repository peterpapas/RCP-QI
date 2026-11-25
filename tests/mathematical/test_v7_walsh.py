"""Independent matrix check of the V7 unique-marker Walsh derivation."""

import numpy as np
import pytest
from scipy.linalg import hadamard


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_one_walsh_sample_cannot_locate_unique_marker(n: int) -> None:
    size = 1 << n
    transform = hadamard(size, dtype=float) / size
    expected = np.full(size, 4 / size**2)
    expected[0] = (1 - 2 / size) ** 2
    for marked in (0, 1, size // 2, size - 1):
        phases = np.ones(size)
        phases[marked] = -1
        measured = np.square(transform @ phases)
        np.testing.assert_allclose(measured, expected, atol=1e-14)
