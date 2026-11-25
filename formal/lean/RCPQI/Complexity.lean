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

/-- A lower bound on each decision's *charged* cost gives a lower bound on
the sum. This is conditional and is not a generic SAT/quantum lower bound. -/
theorem totalCost_of_minimum_oracle
    (oracleCost : Nat → Nat) (c n : Nat)
    (hminimum : ∀ k, 0 < k → c ≤ oracleCost k) :
    n * c ≤ totalCost oracleCost n := by
  induction n with
  | zero => simp [totalCost]
  | succ n ih =>
      calc
        (n + 1) * c = n * c + c := by simp [Nat.add_mul]
        _ ≤ totalCost oracleCost n + oracleCost (n + 1) :=
          Nat.add_le_add ih (hminimum (n + 1) (Nat.zero_lt_succ n))
        _ = totalCost oracleCost (n + 1) := rfl

/-- The specified SAT self-reduction checks the root once and then asks one
existence question per chosen bit. This counts calls, not their relative cost. -/
theorem root_plus_recursive_call_count (oracle : List Bool → Bool) (n : Nat) :
    1 + (chooseBits oracle [] n).length = n + 1 := by
  rw [recursive_decision_count]
  omega

end RCPQI
