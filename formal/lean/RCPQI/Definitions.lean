namespace RCPQI

/-- An `n`-bit candidate. This is a finite type with `2^n` inhabitants. -/
abbrev Candidate (n : Nat) := Fin (2 ^ n)

/-- The problem verifier, left abstract from any implementation. -/
abbrev Verifier (α : Type) := α → Prop

/-- A partition is a predicate on candidates; no candidate list is materialized. -/
abbrev Partition (α : Type) := α → Prop

/-- There is a valid candidate inside a partition. -/
def ExistsIn {α : Type} (verify : Verifier α) (part : Partition α) : Prop :=
  ∃ x, part x ∧ verify x

/-- Two partitions jointly include every candidate. -/
def Covers {α : Type} (left right : Partition α) : Prop :=
  ∀ x, left x ∨ right x

/-- No candidate belongs to both partitions. -/
def Disjoint {α : Type} (left right : Partition α) : Prop :=
  ∀ x, ¬ (left x ∧ right x)

/-- Exactly one candidate satisfies the verifier. -/
def UniqueSolution {α : Type} (verify : Verifier α) : Prop :=
  ∃ winner, verify winner ∧ ∀ x, verify x → x = winner

/-- Logical exclusive-or, stated without any computational complexity claim. -/
def ExactlyOne (p q : Prop) : Prop :=
  (p ∨ q) ∧ ¬ (p ∧ q)

end RCPQI
