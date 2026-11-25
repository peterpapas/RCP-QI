import RCPQI.Complementarity

namespace RCPQI

/-- Binary children induced by any total Boolean partition label. -/
def leftOf {α : Type} (side : α → Bool) : Partition α :=
  fun x => side x = false

def rightOf {α : Type} (side : α → Bool) : Partition α :=
  fun x => side x = true

theorem binary_children_cover {α : Type} (side : α → Bool) :
    Covers (leftOf side) (rightOf side) := by
  intro x
  cases h : side x with
  | false => exact Or.inl h
  | true => exact Or.inr h

theorem binary_children_disjoint {α : Type} (side : α → Bool) :
    Disjoint (leftOf side) (rightOf side) := by
  intro x hboth
  have hfalse : side x = false := hboth.1
  have htrue : side x = true := hboth.2
  rw [hfalse] at htrue
  cases htrue

/-- A reliable existence decision chooses the left partition iff it has a solution. -/
def selectedPartition {α : Type} (verify : Verifier α)
    (left right : Partition α) : Partition α := by
  classical
  exact if ExistsIn verify left then left else right

theorem reliable_selection_preserves_solution
    {α : Type} (verify : Verifier α) (left right : Partition α)
    (hcover : Covers left right) (hexists : ∃ x, verify x) :
    ExistsIn verify (selectedPartition verify left right) := by
  classical
  by_cases hleft : ExistsIn verify left
  · simp [selectedPartition, hleft]
  · have hright : ExistsIn verify right :=
      (at_least_one_partition verify left right hcover hexists).resolve_left hleft
    simpa [selectedPartition, hleft] using hright

/-- A structurally recursive sequence of binary partition decisions. -/
def chooseBits (oracle : List Bool → Bool) (bits : List Bool) : Nat → List Bool
  | 0 => bits
  | n + 1 => chooseBits oracle
      (bits ++ [if oracle (bits ++ [false]) then false else true]) n

theorem chooseBits_length (oracle : List Bool → Bool) (bits : List Bool) (n : Nat) :
    (chooseBits oracle bits n).length = bits.length + n := by
  induction n generalizing bits with
  | zero => simp [chooseBits]
  | succ n ih =>
      simp [chooseBits, ih, Nat.add_comm, Nat.add_left_comm]

end RCPQI
