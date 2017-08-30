! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2017, Science and Technology Facilities Council
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Modified I. Kavcic Met Office
!
!>@brief Meta-data for the Dynamo 0.3 built-in operations.
!>@details This meta-data is purely to provide psyclone with a
!!         specification of each operation. This specification is used
!!         for correctness checking as well as to enable optimisations
!!         of invokes containing calls to built-in operations.
!!         The actual implementation of these built-ins is
!!         generated by psyclone (hence the empty ..._code routines in
!!         this file).
module dynamo0p3_builtins_mod

! ------------------------------------------------------------------- !
! ============== Adding (scaled) fields ============================= !
! ------------------------------------------------------------------- !

  !> field3 = field1 + field2
  type, public, extends(kernel_type) :: X_plus_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_plus_Y_code
  end type X_plus_Y

  !> field1 = field1 + field2
  type, public, extends(kernel_type) :: inc_X_plus_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_plus_Y_code
  end type inc_X_plus_Y

  !> field3 = scalar*field1 + field2
  type, public, extends(kernel_type) :: aX_plus_Y
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: aX_plus_Y_code
  end type aX_plus_Y

  !> field1 = scalar*field1 + field2
  type, public, extends(kernel_type) :: inc_aX_plus_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_aX_plus_Y_code
  end type inc_aX_plus_Y

  !> field1 = field1 + scalar*field2
  type, public, extends(kernel_type) :: inc_X_plus_bY
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_plus_bY_code
  end type inc_X_plus_bY

  !> field3 = scalar1*field1 + scalar2*field2
  type, public, extends(kernel_type) :: aX_plus_bY
     private
     type(arg_type) :: meta_args(5) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: aX_plus_bY_code
  end type aX_plus_bY

  !> field1 = scalar1*field1 + scalar2*field2
  type, public, extends(kernel_type) :: inc_aX_plus_bY
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_aX_plus_bY_code
  end type inc_aX_plus_bY

! ------------------------------------------------------------------- !
! ============== Subtracting (scaled) fields ======================== !
! ------------------------------------------------------------------- !

  !> field3 = field1 - field2
  type, public, extends(kernel_type) :: X_minus_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_minus_Y_code
  end type X_minus_Y

  !> field1 = field1 - field2
  type, public, extends(kernel_type) :: inc_X_minus_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_minus_Y_code
  end type inc_X_minus_Y

  !> field3 = scalar*field1 - field2
  type, public, extends(kernel_type) :: aX_minus_Y
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: aX_minus_Y_code
  end type aX_minus_Y

  !> field3 = field1 - scalar*field2
  type, public, extends(kernel_type) :: X_minus_bY
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_minus_bY_code
  end type X_minus_bY

  !> field1 = field1 - scalar*field2
  type, public, extends(kernel_type) :: inc_X_minus_bY
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_minus_bY_code
  end type inc_X_minus_bY

! ------------------------------------------------------------------- !
! ============== Multiplying (scaled) fields ======================== !
! ------------------------------------------------------------------- !

  !> field3 = field1*field2
  type, public, extends(kernel_type) :: X_times_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_times_Y_code
  end type X_times_Y

  !> field1 = field1*field2
  type, public, extends(kernel_type) :: inc_X_times_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_times_Y_code
  end type inc_X_times_Y

  !> field1 = scalar*field1*field2
  type, public, extends(kernel_type) :: inc_aX_times_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_aX_times_Y_code
  end type inc_aX_times_Y

! ------------------------------------------------------------------- !
! ============== Scaling fields ===================================== !
! ------------------------------------------------------------------- !

  !> field2 = scalar*field1
  type, public, extends(kernel_type) :: a_times_X
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: a_times_X_code
  end type a_times_X

  !> field = scalar*field
  type, public, extends(kernel_type) :: inc_a_times_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_REAL,  GH_READ            ),                    &
          arg_type(GH_FIELD, GH_INC, ANY_SPACE_1)                     &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_a_times_X_code
  end type inc_a_times_X

! ------------------------------------------------------------------- !
! ============== Dividing (scaled) fields =========================== !
! ------------------------------------------------------------------- !

  !> field3 = field1/field2
  type, public, extends(kernel_type) :: X_divideby_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_divideby_Y_code
  end type X_divideby_Y

  !> field1 = field1/field2
  type, public, extends(kernel_type) :: inc_X_divideby_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_divideby_Y_code
  end type inc_X_divideby_Y

! ------------------------------------------------------------------- !
! ============== Raising field to a scalar ========================== !
! ------------------------------------------------------------------- !

  !> field =  field**scalar (real scalar)
  type, public, extends(kernel_type) :: inc_X_powreal_a
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC, ANY_SPACE_1),                    &
          arg_type(GH_REAL,  GH_READ            )                     &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_powreal_a_code
  end type inc_X_powreal_a

! ------------------------------------------------------------------- !
! ============== Setting field elements to a value  ================= !
! ------------------------------------------------------------------- !

  !> field = scalar
  type, public, extends(kernel_type) :: setval_c
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              )                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: setval_c_code
  end type setval_c

  !> field2 = field1
  type, public, extends(kernel_type) :: setval_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: setval_X_code
  end type setval_X

! ------------------------------------------------------------------- !
! ============== Inner product of fields ============================ !
! ------------------------------------------------------------------- !

  !> innprod = innprod + field1(i,j,..)*field2(i,j,...)
  type, public, extends(kernel_type) :: X_innerproduct_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_REAL,  GH_SUM              ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_innerproduct_Y_code
  end type X_innerproduct_Y

  !> innprod = innprod + field(i,j,..)*field(i,j,...)
  type, public, extends(kernel_type) :: X_innerproduct_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_REAL,  GH_SUM              ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_innerproduct_X_code
  end type X_innerproduct_X

! ------------------------------------------------------------------- !
! ============== Sum field elements ================================= !
! ------------------------------------------------------------------- !
  !> sumfld = SUM(field(:,:,...))
  type, public, extends(kernel_type) :: sum_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_REAL,  GH_SUM              ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: sum_X_code
  end type sum_X

contains

  ! Adding (scaled) fields
  subroutine X_plus_Y_code()
  end subroutine X_plus_Y_code

  subroutine inc_X_plus_Y_code()
  end subroutine inc_X_plus_Y_code

  subroutine aX_plus_Y_code()
  end subroutine aX_plus_Y_code

  subroutine inc_aX_plus_Y_code()
  end subroutine inc_aX_plus_Y_code

  subroutine inc_X_plus_bY_code()
  end subroutine inc_X_plus_bY_code

  subroutine aX_plus_bY_code()
  end subroutine aX_plus_bY_code

  subroutine inc_aX_plus_bY_code()
  end subroutine inc_aX_plus_bY_code

  ! Subtracting (scaled) fields
  subroutine X_minus_Y_code()
  end subroutine X_minus_Y_code

  subroutine inc_X_minus_Y_code()
  end subroutine inc_X_minus_Y_code

  subroutine aX_minus_Y_code()
  end subroutine aX_minus_Y_code

  subroutine X_minus_bY_code()
  end subroutine X_minus_bY_code

  subroutine inc_X_minus_bY_code()
  end subroutine inc_X_minus_bY_code

  ! Multiplying (scaled) fields
  subroutine X_times_Y_code()
  end subroutine X_times_Y_code

  subroutine inc_X_times_Y_code()
  end subroutine inc_X_times_Y_code

  subroutine inc_aX_times_Y_code()
  end subroutine inc_aX_times_Y_code

  ! Multiplying fields by a scalar (scaling fields)
  subroutine a_times_X_code()
  end subroutine a_times_X_code

  subroutine inc_a_times_X_code()
  end subroutine inc_a_times_X_code
  ! Dividing (scaled) fields
  subroutine X_divideby_Y_code()
  end subroutine X_divideby_Y_code

  subroutine inc_X_divideby_Y_code()
  end subroutine inc_X_divideby_Y_code

  ! Raising field to a scalar
  subroutine inc_X_powreal_a_code()
  end subroutine inc_X_powreal_a_code

  ! Setting field elements to scalar or other field's values
  subroutine setval_c_code()
  end subroutine setval_c_code

  subroutine setval_X_code()
  end subroutine setval_X_code

  ! Inner product of fields
  subroutine X_innerproduct_Y_code()
  end subroutine X_innerproduct_Y_code

  subroutine X_innerproduct_X_code()
  end subroutine X_innerproduct_X_code

  ! Sum values of a field
  subroutine sum_X_code()
  end subroutine sum_X_code

end module dynamo0p3_builtins_mod
