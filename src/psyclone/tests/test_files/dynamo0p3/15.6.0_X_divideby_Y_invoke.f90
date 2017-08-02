! Author A. R. Porter STFC Daresbury Lab
! Modified I. Kavcic Met Office

program single_invoke

  ! Description: single point-wise operation (divide fields)
  ! specified in an invoke call
  use testkern, only: testkern_type
  use inf,      only: field_type
  implicit none
  type(field_type) :: f1, f2, f3

  call invoke( X_divideby_Y(f3, f1, f2) )

end program single_invoke
