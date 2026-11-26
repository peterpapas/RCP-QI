namespace RCPQI

/-- Alice's positive unit clauses and Bob's negative unit clauses, indexed by `i`. -/
def satisfiesDistributedUnits {n : Nat} (alice bob witness : Fin n → Bool) : Prop :=
  ∀ i, (alice i = true → witness i = true) ∧
    (bob i = true → witness i = false)

/-- The distributed unit-CNF is satisfiable exactly when the private sets are disjoint.
The communication lower bound for set disjointness is an external theorem. -/
theorem distributed_units_sat_iff_disjoint {n : Nat} (alice bob : Fin n → Bool) :
    (∃ witness, satisfiesDistributedUnits alice bob witness) ↔
      ∀ i, ¬ (alice i = true ∧ bob i = true) := by
  constructor
  · rintro ⟨witness, hw⟩ i ⟨ha, hb⟩
    have htrue := (hw i).1 ha
    have hfalse := (hw i).2 hb
    rw [htrue] at hfalse
    contradiction
  · intro hdisjoint
    refine ⟨alice, ?_⟩
    intro i
    constructor
    · intro ha
      exact ha
    · intro hb
      cases ha : alice i with
      | false => rfl
      | true => exact False.elim ((hdisjoint i) ⟨ha, hb⟩)

end RCPQI
