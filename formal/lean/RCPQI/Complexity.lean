import RCPQI.Correctness

namespace RCPQI

/-- For a power-of-two search space, one binary choice per bit is `log2 N` decisions.
This counts decisions only, not the cost of making them. -/
theorem balanced_partition_logarithmic_steps (oracle : List Bool → Bool) (n : Nat) :
    (chooseBits oracle [] n).length = (2 ^ n).log2 := by
  rw [recursive_decision_count, Nat.log2_two_pow]

/-- Sum of the costs of all `n` partition decisions, with no free-oracle assumption. -/
def totalCost (oracleCost : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => totalCost oracleCost n + oracleCost (n + 1)

theorem totalCost_of_bounded_oracle
    (oracleCost : Nat → Nat) (c n : Nat)
    (hbound : ∀ k, oracleCost k ≤ c) :
    totalCost oracleCost n ≤ n * c := by
  induction n with
  | zero => simp [totalCost]
  | succ n ih =>
      calc
        totalCost oracleCost (n + 1)
            = totalCost oracleCost n + oracleCost (n + 1) := rfl
        _ ≤ n * c + c := Nat.add_le_add ih (hbound (n + 1))
        _ = (n + 1) * c := by simp [Nat.add_mul]

end RCPQI
