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

end RCPQI
