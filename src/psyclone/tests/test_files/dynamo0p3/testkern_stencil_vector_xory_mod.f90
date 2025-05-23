! BSD 3-Clause License
!
! Copyright (c) 2019-2025, Science and Technology Facilities Council
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
! Author R. W. Ford, STFC Daresbury Lab
! Modified I. Kavcic, Met Office

module testkern_stencil_vector_xory_mod

  use argument_mod
  use fs_continuity_mod
  use kernel_mod
  use constants_mod

  implicit none

  type, extends(kernel_type) :: testkern_stencil_vector_xory_type
     type(arg_type), dimension(2) :: meta_args =                         &
          (/ arg_type(gh_field*3, gh_real, gh_inc,  w0),                 &
             arg_type(gh_field*4, gh_real, gh_read, w3, stencil(xory1d)) &
           /)
     integer :: operates_on = cell_column
   contains
     procedure, nopass :: code => testkern_stencil_vector_xory_code
  end type testkern_stencil_vector_xory_type

contains

  subroutine testkern_stencil_vector_xory_code(           &
                      nlayers, fld1_v1, fld1_v2, fld1_v3, &
                      fld2_v1, fld2_v2, fld2_v3, fld2_v4, &
                      fld2_st_size, fld2_direction,       &
                      fld2_st_dofmap,                     &
                      ndf_w0, undf_w0, map_w0,            &
                      ndf_w3, undf_w3, map_w3)

    implicit none

    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf_w0
    integer(kind=i_def), intent(in) :: ndf_w3
    integer(kind=i_def), intent(in) :: undf_w0, undf_w3
    integer(kind=i_def), intent(in) :: fld2_st_size
    integer(kind=i_def), intent(in) :: fld2_direction
    integer(kind=i_def), intent(in), dimension(ndf_w0) :: map_w0
    integer(kind=i_def), intent(in), dimension(ndf_w3) :: map_w3
    integer(kind=i_def), intent(in), dimension(ndf_w3,fld2_st_size) :: fld2_st_dofmap
    real(kind=r_def), intent(inout), dimension(undf_w0) :: fld1_v1
    real(kind=r_def), intent(inout), dimension(undf_w0) :: fld1_v2
    real(kind=r_def), intent(inout), dimension(undf_w0) :: fld1_v3
    real(kind=r_def), intent(in), dimension(undf_w3)    :: fld2_v1
    real(kind=r_def), intent(in), dimension(undf_w3)    :: fld2_v2
    real(kind=r_def), intent(in), dimension(undf_w3)    :: fld2_v3
    real(kind=r_def), intent(in), dimension(undf_w3)    :: fld2_v4

  end subroutine testkern_stencil_vector_xory_code

end module testkern_stencil_vector_xory_mod
