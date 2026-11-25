import RCPQI.PartialComplementarity

namespace RCPQI

/-- A three-literal clause is satisfiable exactly when its two-equation
quadratic gadget has an auxiliary Boolean value. Interpreting `&&` as
multiplication and `!a` as `1+a` over GF(2) gives equations of degree at most
two. This proves only the local truth-table equivalence, not the complexity
theory corollary for arbitrary systems of such equations. -/
theorem clause_quadratic_gadget (a b c : Bool) :
    (∃ u : Bool, u = (!a && !b) ∧ (u && !c) = false) ↔
      (a || b || c) = true := by
  cases a <;> cases b <;> cases c <;> decide

end RCPQI
