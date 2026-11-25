import RCPQI.Structural

namespace RCPQI

/-- A supplied local complement law and a point in its domain give a classical
witness after one value of `f`. Finding a point in the domain and certifying
the law are not part of this theorem. The partner need not lie in the domain. -/
theorem local_complementing_witness (domain : α → Prop)
    (f : α → Bool) (T : α → α)
    (hflip : ∀ y, domain y → f (T y) = !f y)
    (x : α) (hx : domain x) :
    f (if f x = true then x else T x) = true := by
  cases hvalue : f x <;> simp [hvalue, hflip x hx]

/-- If `T` complements one constraint but preserves a residual verifier,
one residual witness can be converted into a full witness classically. This
does not construct the residual witness or bound its search cost. -/
theorem constraint_complement_residual_witness
    (constraint residual : α → Bool) (T : α → α)
    (hflip : ∀ y, constraint (T y) = !constraint y)
    (hpreserve : ∀ y, residual (T y) = residual y)
    (x : α) (hx : residual x = true) :
    (constraint (if constraint x = true then x else T x) &&
      residual (if constraint x = true then x else T x)) = true := by
  cases hc : constraint x <;> simp [hc, hflip x, hpreserve x, hx]

/-- The fresh-bit instance `F(x,b)=b ∧ H(x)` has a solution exactly when
the residual problem `H` does. A flip of the fresh bit complements one
individual constraint, but it does not solve the residual problem. -/
theorem gated_residual_existence_equivalence (h : α → Bool) :
    (∃ p : α × Bool, (p.2 && h p.1) = true) ↔
      ∃ x, h x = true := by
  constructor
  · rintro ⟨⟨x, b⟩, hp⟩
    cases b with
    | false => simp at hp
    | true => exact ⟨x, by simpa using hp⟩
  · rintro ⟨x, hx⟩
    exact ⟨(x, true), by simpa using hx⟩

end RCPQI
