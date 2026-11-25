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

/-- Once a total complementing transformation is supplied, one *classical*
verifier evaluation selects a witness. The cost of obtaining `T` is assumed. -/
theorem complementing_one_query_witness (f : α → Bool) (T : α → α)
    (hflip : ∀ y, f (T y) = !f y) (x : α) :
    f (if f x = true then x else T x) = true := by
  cases hx : f x <;> simp [hx, hflip]

/-- A verifier that factors through a quotient is constant on each fiber. -/
theorem factor_implies_fiber_constant
    (f : α → Bool) (g : β → Bool) (q : α → β)
    (hfactor : ∀ x, f x = g (q x))
    (x y : α) (hxy : q x = q y) : f x = f y := by
  rw [hfactor x, hfactor y, hxy]

/-- Conversely, a supplied section and fiber constancy construct the factor:
the quotient verifier is `g(y)=f(r(y))`. Discovering a useful quotient and
computing representatives are outside this theorem. -/
theorem fiber_constant_factors
    (f : α → Bool) (q : α → β) (r : β → α)
    (hsection : ∀ y, q (r y) = y)
    (hfiber : ∀ x y, q x = q y → f x = f y)
    (x : α) : f x = f (r (q x)) := by
  exact hfiber x (r (q x)) (hsection (q x)).symm

/-- With a computable quotient and section, existence in the original search
space and existence in the quotient have the same answer. This is a value-level
equivalence; it does not bound the circuit cost of `q` or `r`. -/
theorem quotient_existence_equivalence
    (f : α → Bool) (g : β → Bool) (q : α → β) (r : β → α)
    (hsection : ∀ y, q (r y) = y)
    (hfactor : ∀ x, f x = g (q x)) :
    (∃ x, f x = true) ↔ (∃ y, g y = true) := by
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨q x, (hfactor x).symm.trans hx⟩
  · rintro ⟨y, hy⟩
    refine ⟨r y, ?_⟩
    rw [hfactor (r y), hsection]
    exact hy

/-- Flipping a fresh gate bit preserves the verifier `b ∧ h(x)` exactly when
`h` has no satisfying input. For CNF `h`, this gives a direct reduction from
UNSAT to semantic certification of even a supplied one-bit transformation. -/
theorem gated_flip_preserving_iff_unsat (h : α → Bool) :
    (∀ p : α × Bool, ((!p.2) && h p.1) = (p.2 && h p.1)) ↔
      ∀ x, h x = false := by
  constructor
  · intro hpres x
    have hx := hpres (x, true)
    simpa using hx.symm
  · intro hzero p
    simp [hzero p.1]

end RCPQI
