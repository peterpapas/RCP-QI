/-!
# A boundary between arithmetic and Boolean semantics

The integer polynomial expression `z² - z` vanishes on Boolean inputs but not
on all integers. These theorems concern expression evaluation, not a formal
polynomial ring, and suffice as a concrete counterexample to transferring a
lower bound for all-input polynomial identity to Boolean-input agreement.
-/

namespace RCPQI

def booleanKernelWitness (z : Int) : Int := z * z - z

theorem boolean_relation_vanishes (b : Bool) :
    booleanKernelWitness (if b then 1 else 0) = 0 := by
  cases b <;> decide

theorem boolean_relation_nonzero : booleanKernelWitness 2 ≠ 0 := by
  decide

end RCPQI
