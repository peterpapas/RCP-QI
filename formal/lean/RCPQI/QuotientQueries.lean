namespace RCPQI

def queryTranscript {X : Type} (f : X → Bool) (xs : List X) : List Bool := xs.map f

/-- A known representative map simulates each quotient query with one original query. -/
theorem quotient_transcript_to_original {X Y : Type}
    (f : X → Bool) (representative : Y → X) (ys : List Y) :
    queryTranscript (fun y => f (representative y)) ys =
      queryTranscript f (ys.map representative) := by
  simp [queryTranscript, List.map_map, Function.comp_def]

/-- Fiber constancy permits the reverse one-for-one simulation on fixed query lists. -/
theorem original_transcript_to_quotient {X Y : Type}
    (f : X → Bool) (quotient : X → Y) (representative : Y → X)
    (fiber : ∀ x, f x = f (representative (quotient x))) (xs : List X) :
    queryTranscript f xs =
      queryTranscript (fun y => f (representative y)) (xs.map quotient) := by
  induction xs with
  | nil => rfl
  | cons x rest ih =>
      simp only [queryTranscript, List.map_cons] at ih ⊢
      rw [fiber x, ih]

end RCPQI
