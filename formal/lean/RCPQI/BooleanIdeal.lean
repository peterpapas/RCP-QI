namespace RCPQI

/-- The one-variable Boolean-ideal generator, evaluated over the integers. -/
def booleanIdealGenerator (z : Int) : Int := z * z - z

/-- Evaluation at a Boolean point annihilates the ideal generator. -/
theorem booleanIdealGenerator_on_bool (b : Bool) :
    booleanIdealGenerator (if b then 1 else 0) = 0 := by
  cases b <;> decide

/-- One-variable multilinear interpolation from its two Boolean values. -/
def interpolateBool (f : Bool → Int) (z : Int) : Int :=
  f false * (1 - z) + f true * z

theorem interpolateBool_on_bool (f : Bool → Int) (b : Bool) :
    interpolateBool f (if b then 1 else 0) = f b := by
  cases b <;> simp [interpolateBool]

/-- Adding an arbitrary multiple of the ideal generator preserves Boolean evaluation. -/
theorem ideal_multiple_same_bool (p h : Int → Int) (b : Bool) :
    p (if b then 1 else 0) +
        booleanIdealGenerator (if b then 1 else 0) * h (if b then 1 else 0) =
      p (if b then 1 else 0) := by
  simp [booleanIdealGenerator_on_bool]

/-- Integer encoding of a Boolean coordinate. -/
def boolCoordinate (b : Bool) : Int := if b then 1 else 0

/-- Shannon interpolation of a table on an `n`-coordinate Boolean cube. -/
def interpolateCube : (n : Nat) → (List Bool → Int) → List Int → Int
  | 0, f, _ => f []
  | _ + 1, _, [] => 0
  | n + 1, f, z :: zs =>
      (1 - z) * interpolateCube n (fun bs => f (false :: bs)) zs +
        z * interpolateCube n (fun bs => f (true :: bs)) zs

/-- The recursive multilinear expression agrees with its table at all Boolean points. -/
theorem interpolateCube_on_bool (n : Nat) (f : List Bool → Int) (bs : List Bool)
    (h : bs.length = n) :
    interpolateCube n f (bs.map boolCoordinate) = f bs := by
  induction n generalizing f bs with
  | zero =>
      cases bs with
      | nil => simp [interpolateCube]
      | cons _ _ => simp at h
  | succ n ih =>
      cases bs with
      | nil => simp at h
      | cons b rest =>
          have hr : rest.length = n := by simpa using h
          cases b
          · simp [interpolateCube, boolCoordinate, ih, hr]
          · simp [interpolateCube, boolCoordinate, ih, hr]

end RCPQI
