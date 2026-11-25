import RCPQI.Partitioning

namespace RCPQI

/-- A selected partition contains a solution whenever a reliable oracle is used. -/
theorem recursive_step_correct
    {α : Type} (verify : Verifier α) (left right : Partition α)
    (hcover : Covers left right) (hexists : ∃ x, verify x) :
    ∃ x, selectedPartition verify left right x ∧ verify x :=
  reliable_selection_preserves_solution verify left right hcover hexists

/-- The decision process terminates after exactly the requested number of bits. -/
theorem recursive_decision_count (oracle : List Bool → Bool) (n : Nat) :
    (chooseBits oracle [] n).length = n := by
  simpa using chooseBits_length oracle [] n

/-- Conditional correctness: the oracle identifies which next bit matches the
target at every prefix along the true path. This assumes reliability, not low cost. -/
theorem chooseBits_correct_of_reliable_oracle
    (target : List Bool) (oracle : List Bool → Bool)
    (hreliable : ∀ (current suffix : List Bool) (next : Bool),
      target = current ++ next :: suffix →
      oracle (current ++ [false]) = (if next then false else true)) :
    ∀ (bits rest : List Bool), target = bits ++ rest →
      chooseBits oracle bits rest.length = target := by
  intro bits rest
  induction rest generalizing bits with
  | nil =>
      intro htarget
      simpa [chooseBits] using htarget.symm
  | cons next suffix ih =>
      intro htarget
      have hprobe := hreliable bits suffix next htarget
      have hselected : (if oracle (bits ++ [false]) then false else true) = next := by
        cases next <;> simp [hprobe]
      have hnew : target = (bits ++ [next]) ++ suffix := by
        simpa [List.append_assoc] using htarget
      simpa [chooseBits, hselected] using ih (bits ++ [next]) hnew

end RCPQI
