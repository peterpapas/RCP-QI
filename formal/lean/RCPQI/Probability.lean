import RCPQI.Complexity
import Init.Data.Rat

namespace RCPQI

/-- V2 algebra, conditional on one marked state and equal probability on
each of the remaining `N-1` states. `q` is the probability of a half with
`N/2` states containing the marked state. No quantum circuit is modelled. -/
theorem grover_half_relation (N p u q : Rat)
    (hnorm : p + (N - 1) * u = 1)
    (hhalf : q = p + (N / 2 - 1) * u) :
    2 * (N - 1) * q = N - 2 + N * p := by
  grind +ring

/-- V1 numerator identity for the standard *one-iteration* amplitudes:
marked amplitude `(3N-4)/N^(3/2)` and every unmarked amplitude
`(N-4)/N^(3/2)`. This does not prove the amplitude formulas themselves. -/
theorem one_iteration_half_numerator (N p u q : Rat)
    (hp : N ^ 3 * p = (3 * N - 4) ^ 2)
    (hu : N ^ 3 * u = (N - 4) ^ 2)
    (hhalf : q = p + (N / 2 - 1) * u) :
    2 * N ^ 3 * q = N ^ 3 + 8 * N ^ 2 - 16 * N := by
  grind +ring

theorem one_iteration_half_formula (N p u q : Rat)
    (hN : N ≠ 0)
    (hp : N ^ 3 * p = (3 * N - 4) ^ 2)
    (hu : N ^ 3 * u = (N - 4) ^ 2)
    (hhalf : q = p + (N / 2 - 1) * u) :
    q = 1 / 2 + 4 / N - 8 / N ^ 2 := by
  have hnum := one_iteration_half_numerator N p u q hp hu hhalf
  grind +ring

end RCPQI
