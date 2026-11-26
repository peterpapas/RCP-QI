namespace RCPQI

/-- Diagonal sign of the *literal* Boolean phase oracle. -/
def phaseSign (b : Bool) : Int := if b then -1 else 1

theorem phaseSign_eq_iff (a b : Bool) : phaseSign a = phaseSign b ↔ a = b := by
  cases a <;> cases b <;> decide

/-- Literal diagonal entries coincide exactly for pointwise-equal verifiers. -/
theorem phaseEntries_eq_iff {X : Type} (f g : X → Bool) :
    (∀ x, phaseSign (f x) = phaseSign (g x)) ↔ f = g := by
  constructor
  · intro h
    funext x
    exact (phaseSign_eq_iff (f x) (g x)).mp (h x)
  · intro h x
    rw [h]

/-- Complementing every verifier output changes every literal sign. -/
theorem phaseSign_complement (b : Bool) : phaseSign (!b) = -phaseSign b := by
  cases b <;> decide

end RCPQI
