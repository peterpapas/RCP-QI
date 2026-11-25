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

/-- Under at most one true assignment, a complementing involution can act only
on the named assignment and its partner. In particular, a larger search type cannot
satisfy all these assumptions. This says nothing about discovering `T`. -/
theorem unique_complementing_universe_is_pair (f : α → Bool) (T : α → α)
    (hflip : ∀ y, f (T y) = !f y)
    (hinvolution : ∀ y, T (T y) = y)
    (winner : α)
    (hunique : ∀ y, f y = true → y = winner) :
    ∀ y, y = winner ∨ y = T winner := by
  intro y
  cases hy : f y with
  | true => exact Or.inl (hunique y hy)
  | false =>
      have hty : f (T y) = true := by simp [hflip, hy]
      have htw : T y = winner := hunique (T y) hty
      right
      calc
        y = T (T y) := (hinvolution y).symm
        _ = T winner := congrArg T htw

end RCPQI
