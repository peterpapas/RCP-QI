import RCPQI.Complementarity

namespace RCPQI

/-- A supplied complementing transformation makes each paired truth value
opposite. This assumes the transformation law; deriving it from CNF is outside
the theorem. -/
theorem complementing_pair (f : α → Bool) (T : α → α)
    (hflip : ∀ x, f (T x) = !f x) (x : α) :
    (f x = true ∧ f (T x) = false) ∨
    (f x = false ∧ f (T x) = true) := by
  cases h : f x <;> simp [hflip, h]

/-- The complement law is incompatible with a fixed point of `T`. -/
theorem complementing_no_fixed_points (f : α → Bool) (T : α → α)
    (hflip : ∀ x, f (T x) = !f x) (x : α) : T x ≠ x := by
  intro hfixed
  have h := hflip x
  rw [hfixed] at h
  cases hvalue : f x <;> simp [hvalue] at h

/-- A supplied symmetry preserves verifier values. It may reduce a quotient
search classically; this theorem establishes no efficient way to discover it. -/
theorem preserving_pair (f : α → Bool) (T : α → α)
    (hinvariant : ∀ x, f (T x) = f x) (x : α) :
    f (T x) = f x := hinvariant x

end RCPQI
