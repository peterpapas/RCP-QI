import RCPQI.Definitions

namespace RCPQI

theorem at_least_one_partition
    {α : Type} (verify : Verifier α) (left right : Partition α)
    (hcover : Covers left right) (hexists : ∃ x, verify x) :
    ExistsIn verify left ∨ ExistsIn verify right := by
  rcases hexists with ⟨x, hx⟩
  rcases hcover x with hleft | hright
  · exact Or.inl ⟨x, hleft, hx⟩
  · exact Or.inr ⟨x, hright, hx⟩

theorem not_both_partitions_of_unique
    {α : Type} (verify : Verifier α) (left right : Partition α)
    (hdisjoint : Disjoint left right) (hunique : UniqueSolution verify) :
    ¬ (ExistsIn verify left ∧ ExistsIn verify right) := by
  intro hboth
  rcases hboth with ⟨⟨x, hleft, hx⟩, ⟨y, hright, hy⟩⟩
  rcases hunique with ⟨winner, _, hunique⟩
  have hxy : x = y := (hunique x hx).trans (hunique y hy).symm
  subst y
  exact hdisjoint x ⟨hleft, hright⟩

/-- Under a unique-solution promise, exactly one exhaustive disjoint half contains it. -/
theorem unique_solution_partition_complementarity
    {α : Type} (verify : Verifier α) (left right : Partition α)
    (hcover : Covers left right) (hdisjoint : Disjoint left right)
    (hunique : UniqueSolution verify) :
    ExactlyOne (ExistsIn verify left) (ExistsIn verify right) := by
  rcases hunique with ⟨winner, hw, huniq⟩
  constructor
  · exact at_least_one_partition verify left right hcover ⟨winner, hw⟩
  · exact not_both_partitions_of_unique verify left right hdisjoint ⟨winner, hw, huniq⟩

end RCPQI
