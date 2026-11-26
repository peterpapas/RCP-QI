namespace RCPQI

/-- A signed propositional variable; `positive = true` denotes the positive literal. -/
structure SignedLiteral where
  index : Nat
  positive : Bool
  deriving DecidableEq

abbrev SignedClause := List SignedLiteral
abbrev SignedCNF := List SignedClause
abbrev BinaryAssignment := Nat → Bool
abbrev BinaryPrefix := List (Nat × Bool)

def literalValue (a : BinaryAssignment) (l : SignedLiteral) : Bool :=
  if l.positive then a l.index else !a l.index

def clauseValue (a : BinaryAssignment) (c : SignedClause) : Bool :=
  c.any (literalValue a)

def satisfiesCNF (f : SignedCNF) (a : BinaryAssignment) : Prop :=
  ∀ c, c ∈ f → clauseValue a c = true

def extendsPrefix (p : BinaryPrefix) (a : BinaryAssignment) : Prop :=
  ∀ i b, (i, b) ∈ p → a i = b

/-- A leaf conflict can be checked by comparing every clause literal to the prefix. -/
def clauseConflicts (p : BinaryPrefix) (c : SignedClause) : Prop :=
  ∀ l, l ∈ c → (l.index, !l.positive) ∈ p

/-- Executable leaf check: each literal must be falsified by a prefix pair. -/
def checkClauseConflict (p : BinaryPrefix) (c : SignedClause) : Bool :=
  c.all (fun l => (l.index, !l.positive) ∈ p)

theorem checkClauseConflict_correct (p : BinaryPrefix) (c : SignedClause) :
    checkClauseConflict p c = true ↔ clauseConflicts p c := by
  simp [checkClauseConflict, clauseConflicts, List.all_eq_true]

theorem literal_false_of_prefix (p : BinaryPrefix) (a : BinaryAssignment)
    (hp : extendsPrefix p a) (l : SignedLiteral)
    (hl : (l.index, !l.positive) ∈ p) : literalValue a l = false := by
  have hbit := hp l.index (!l.positive) hl
  cases l.positive <;> simp [literalValue, hbit]

theorem clause_false_of_conflict (p : BinaryPrefix) (a : BinaryAssignment)
    (hp : extendsPrefix p a) (c : SignedClause)
    (hc : clauseConflicts p c) : clauseValue a c = false := by
  induction c with
  | nil => rfl
  | cons l rest ih =>
      have hfirst : literalValue a l = false :=
        literal_false_of_prefix p a hp l (hc l (by simp))
      have hrest : clauseConflicts p rest := by
        intro l' hl'
        exact hc l' (by simp [hl'])
      change (literalValue a l || clauseValue a rest) = false
      simp [hfirst, ih hrest]

/-- A restricted search tree: both branches are explored, and every leaf
contains an original clause falsified by its prefix. No opaque oracle call,
learned clause, or quantum operation is part of this certificate. -/
inductive ConflictTree (f : SignedCNF) : BinaryPrefix → Type where
  | leaf (p : BinaryPrefix) (c : SignedClause)
      (hin : c ∈ f) (hconflict : clauseConflicts p c) : ConflictTree f p
  | branch (p : BinaryPrefix) (i : Nat)
      (zero : ConflictTree f ((i, false) :: p))
      (one : ConflictTree f ((i, true) :: p)) : ConflictTree f p

/-- A verified conflict tree rejects every extension of its root prefix. -/
theorem conflictTree_sound {f : SignedCNF} {p : BinaryPrefix}
    (t : ConflictTree f p) :
    ∀ a, extendsPrefix p a → ¬ satisfiesCNF f a := by
  induction t with
  | leaf p c hin hconflict =>
      intro a hp hs
      have hfalse := clause_false_of_conflict p a hp c hconflict
      have htrue := hs c hin
      rw [hfalse] at htrue
      contradiction
  | branch p i zero one ihzero ihone =>
      intro a hp
      cases hbit : a i with
      | false =>
          exact ihzero a (by
            intro j b hmem
            simp only [List.mem_cons, Prod.mk.injEq] at hmem
            rcases hmem with hfirst | hrest
            · rcases hfirst with ⟨hji, hbf⟩
              subst j
              subst b
              exact hbit
            · exact hp j b hrest)
      | true =>
          exact ihone a (by
            intro j b hmem
            simp only [List.mem_cons, Prod.mk.injEq] at hmem
            rcases hmem with hfirst | hrest
            · rcases hfirst with ⟨hji, hbf⟩
              subst j
              subst b
              exact hbit
            · exact hp j b hrest)

/-- A complete certified conflict tree at the empty prefix refutes the CNF. -/
theorem conflictTree_root_unsat {f : SignedCNF}
    (t : ConflictTree f []) (a : BinaryAssignment) : ¬ satisfiesCNF f a := by
  apply conflictTree_sound t a
  intro i b hmem
  simp at hmem

end RCPQI
