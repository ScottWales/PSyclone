# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2017-2018, Science and Technology Facilities Council
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
# Authors R. W. Ford and A. R. Porter, STFC Daresbury Lab

''' This module contains tests for the multi-grid part of the Dynamo 0.3 API
    using pytest. '''

from __future__ import absolute_import
# Since this is a file containing tests which often have to get in and
# change the internal state of objects we disable pylint's warning
# about such accesses
# pylint: disable=protected-access

import os
import pytest
import fparser
import utils
from fparser import api as fpapi
from psyclone.dynamo0p3 import DynKernMetadata
from psyclone.parse import ParseError, parse
from psyclone.psyGen import PSyFactory

# constants
BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "test_files", "dynamo0p3")

API = "dynamo0.3"

RESTRICT_MDATA = '''
module restrict_mod
type, public, extends(kernel_type) :: restrict_kernel_type
   private
   type(arg_type) :: meta_args(2) = (/                                 &
       arg_type(GH_FIELD, GH_INC, ANY_SPACE_1, mesh_arg=GH_COARSE),    &
       arg_type(GH_FIELD, GH_READ,  ANY_SPACE_2, mesh_arg=GH_FINE   )  &
       /)
  integer :: iterates_over = CELLS
contains
  procedure, nopass :: restrict_kernel_code
end type restrict_kernel_type
contains
  subroutine restrict_kernel_code()
  end subroutine restrict_kernel_code
end module restrict_mod
'''


def test_invalid_mesh_type():
    ''' Check that we raise an error if an unrecognised name is supplied
    for the mesh associated with a field argument '''
    fparser.logging.disable('CRITICAL')
    code = RESTRICT_MDATA.replace("GH_COARSE", "GH_RUBBISH", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    print str(excinfo)
    assert ("mesh_arg must be one of [\\'gh_coarse\\', "
            "\\'gh_fine\\'] but got gh_rubbish" in str(excinfo))


def test_invalid_mesh_specifier():
    ''' Check that we raise an error if "mesh_arg" is mis-spelt '''
    fparser.logging.disable('CRITICAL')
    code = RESTRICT_MDATA.replace("mesh_arg=GH_COARSE",
                                  "mesh_ar=GH_COARSE", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    print str(excinfo)
    assert ("mesh_ar=gh_coarse is not a valid mesh identifier" in
            str(excinfo))


def test_all_args_same_mesh_error():
    ''' Check that we reject a kernel if all arguments are specified
    as being on the same mesh (coarse or fine) '''
    fparser.logging.disable('CRITICAL')
    # Both on fine mesh
    code = RESTRICT_MDATA.replace("GH_COARSE", "GH_FINE", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    assert ("Inter-grid kernels in the Dynamo 0.3 API must have at least "
            "one field argument on each of the mesh types (['gh_coarse', "
            "'gh_fine']). However, kernel restrict_kernel_type has arguments "
            "only on ['gh_fine']" in str(excinfo))
    # Both on coarse mesh
    code = RESTRICT_MDATA.replace("GH_FINE", "GH_COARSE", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    assert ("Inter-grid kernels in the Dynamo 0.3 API must have at least "
            "one field argument on each of the mesh types (['gh_coarse', "
            "'gh_fine']). However, kernel restrict_kernel_type has arguments "
            "only on ['gh_coarse']" in str(excinfo))


def test_all_fields_have_mesh():
    ''' Check that we reject an inter-grid kernel if any of its field
    arguments are missing a mesh specifier '''
    # Add a field argument that is missing a mesh_arg specifier
    code = RESTRICT_MDATA.replace(
        "       arg_type(GH_FIELD, GH_READ,  ANY_SPACE_2, "
        "mesh_arg=GH_FINE   )  &",
        "       arg_type(GH_FIELD, GH_READ,  ANY_SPACE_2, "
        "mesh_arg=GH_FINE   ), &\n"
        "       arg_type(GH_FIELD, GH_READ,  ANY_SPACE_2) &\n", 1)
    code = code.replace("(2)", "(3)", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    assert ("Inter-grid kernels in the Dynamo 0.3 API must specify which "
            "mesh each field argument "
            "is on but kernel restrict_kernel_type has at least one field "
            "argument for which mesh_arg is missing." in str(excinfo))


def test_args_same_space_error():
    ''' Check that we reject a kernel if arguments on different meshes
    are specified as being on the same function space '''
    fparser.logging.disable('CRITICAL')
    code = RESTRICT_MDATA.replace("ANY_SPACE_2", "ANY_SPACE_1", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    assert ("inter-grid kernels must be on different function spaces if they "
            "are on different meshes. However kernel restrict_kernel_type "
            "has a field on function space(s) ['any_space_1'] on each of the "
            "mesh types ['gh_coarse', 'gh_fine']." in str(excinfo))


def test_only_field_args():
    ''' Check that we reject an inter-grid kernel if it has any arguments
    that are not fields '''
    fparser.logging.disable('CRITICAL')
    # Add a scalar argument to the kernel
    code = RESTRICT_MDATA.replace(
        "       arg_type(GH_FIELD, GH_READ,  ANY_SPACE_2, "
        "mesh_arg=GH_FINE   )  &",
        "       arg_type(GH_FIELD, GH_READ,  ANY_SPACE_2, "
        "mesh_arg=GH_FINE   ), &\n"
        "       arg_type(GH_REAL, GH_READ) &", 1)
    code = code.replace("(2)", "(3)", 1)
    print code
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    with pytest.raises(ParseError) as excinfo:
        _ = DynKernMetadata(ast, name=name)
    assert ("Inter-grid kernels in the Dynamo 0.3 API are only permitted to "
            "have field arguments but kernel restrict_kernel_type also has "
            "arguments of type ['gh_real']" in str(excinfo))


def test_field_vector():
    ''' Check that we accept an inter-grid kernel with field-vector
    arguments '''
    fparser.logging.disable('CRITICAL')
    # Change both of the arguments to be vectors
    code = RESTRICT_MDATA.replace("GH_FIELD,", "GH_FIELD*2,", 2)
    ast = fpapi.parse(code, ignore_comments=False)
    name = "restrict_kernel_type"
    dkm = DynKernMetadata(ast, name=name)
    for arg in dkm.arg_descriptors:
        assert arg.vector_size == 2
    # Change only one of the arguments to be a vector
    code = RESTRICT_MDATA.replace("GH_FIELD,", "GH_FIELD*3,", 1)
    ast = fpapi.parse(code, ignore_comments=False)
    dkm = DynKernMetadata(ast, name=name)
    assert dkm.arg_descriptors[0].vector_size == 3
    assert dkm.arg_descriptors[1].vector_size == 1


def test_field_prolong(tmpdir, f90, f90flags):
    ''' Check that we generate correct psy-layer code for an invoke
    containing a kernel that performs a prolongation operation '''
    _, invoke_info = parse(os.path.join(BASE_PATH,
                                        "22.0_intergrid_prolong.f90"),
                           api=API)
    for distmem in [False, True]:
        psy = PSyFactory(API, distributed_memory=distmem).create(invoke_info)
        gen_code = str(psy.gen)
        print gen_code

        if utils.TEST_COMPILE:
            assert utils.code_compiles(API, psy, tmpdir, f90, f90flags)

        expected = (
            "      USE prolong_kernel_mod, ONLY: prolong_kernel_code\n"
            "      USE mesh_map_mod, ONLY: mesh_map_type\n"
            "      USE mesh_mod, ONLY: mesh_type\n"
            "      TYPE(field_type), intent(inout) :: field1\n"
            "      TYPE(field_type), intent(in) :: field2\n"
            "      INTEGER cell\n")
        assert expected in gen_code

        expected = (
            "      INTEGER ncell_fine_field1, ncpc_field1_field2\n"
            "      INTEGER, pointer :: cell_map_field2(:,:) => null()\n"
            "      TYPE(mesh_map_type), pointer :: "
            "mmap_field1_field2 => null()\n"
            "      TYPE(mesh_type), pointer :: fine_mesh_field1 => null()\n"
            "      TYPE(mesh_type), pointer :: coarse_mesh_field2 => null()\n")
        assert expected in gen_code

        expected = (
            "      ! Look-up mesh objects and loop limits for inter-grid "
            "kernels\n"
            "      !\n"
            "      fine_mesh_field1 => field1%get_mesh()\n"
            "      coarse_mesh_field2 => field2%get_mesh()\n"
            "      mmap_field1_field2 => coarse_mesh_field2%get_mesh_map"
            "(fine_mesh_field1)\n"
            "      cell_map_field2 => mmap_field1_field2%get_whole_cell_map()\n")
        if distmem:
            expected += (
                "      ncell_fine_field1 = fine_mesh_field1%get_last_halo_cell("
                "depth=2)\n")
        else:
            expected += \
                "      ncell_fine_field1 = field1_proxy%vspace%get_ncell()\n"
        expected += (
            "      ncpc_field1_field2 = mmap_field1_field2%"
            "get_ntarget_cells_per_source_cell()\n")
        assert expected in gen_code

        if distmem:
            # We are writing to a continuous field on the fine mesh, we
            # only need to halo swap to depth one on the coarse.
            expected = (
                "      IF (field2_proxy%is_dirty(depth=1)) THEN\n"
                "        CALL field2_proxy%halo_exchange(depth=1)\n"
                "      END IF \n"
                "      !\n"
                "      DO cell=1,coarse_mesh_field2%get_last_halo_cell(1)\n")
            assert expected in gen_code
        else:
            assert "DO cell=1,field2_proxy%vspace%get_ncell()\n" in gen_code

        expected = (
            "        CALL prolong_kernel_code(nlayers, "
            "cell_map_field2(:,cell), ncpc_field1_field2, ncell_fine_field1, "
            "field1_proxy%data, field2_proxy%data, ndf_w1, undf_w1, map_w1, "
            "undf_w2, map_w2(:,cell))\n"
            "      END DO \n")
        assert expected in gen_code

        if distmem:
            set_dirty = "      CALL field1_proxy%set_dirty()\n"
            assert set_dirty in gen_code


def test_field_restrict(tmpdir, f90, f90flags):
    ''' Test that we generate correct code for an invoke containing a
    single restriction operation (read from find, write to coarse) '''
    _, invoke_info = parse(os.path.join(BASE_PATH,
                                        "22.1_intergrid_restrict.f90"),
                           api=API)
    for distmem in [False, True]:
        psy = PSyFactory(API, distributed_memory=distmem).create(invoke_info)
        output = str(psy.gen)
        print output

        if utils.TEST_COMPILE:
            assert utils.code_compiles(API, psy, tmpdir, f90, f90flags)

        defs = (
            "      USE restrict_kernel_mod, ONLY: restrict_kernel_code\n"
            "      USE mesh_map_mod, ONLY: mesh_map_type\n"
            "      USE mesh_mod, ONLY: mesh_type\n"
            "      TYPE(field_type), intent(inout) :: field1\n"
            "      TYPE(field_type), intent(in) :: field2\n")
        assert defs in output

        defs2 = (
            "      INTEGER nlayers\n"
            "      TYPE(field_proxy_type) field1_proxy, field2_proxy\n"
            "      INTEGER ncell_fine_field2, ncpc_field2_field1\n"
            "      INTEGER, pointer :: cell_map_field1(:,:) => null()\n"
            "      TYPE(mesh_map_type), pointer :: mmap_field2_field1 => "
            "null()\n"
            "      TYPE(mesh_type), pointer :: coarse_mesh_field1 => null()\n"
            "      TYPE(mesh_type), pointer :: fine_mesh_field2 => null()\n"
            "      INTEGER, pointer :: map_any_space_2_field2(:,:) => null(), "
            "map_any_space_1_field1(:,:) => null()\n")
        assert defs2 in output

        inits = (
            "      ! Look-up dofmaps for each function space\n"
            "      !\n"
            "      map_any_space_2_field2 => field2_proxy%vspace%"
            "get_whole_dofmap()\n"
            "      map_any_space_1_field1 => field1_proxy%vspace%"
            "get_whole_dofmap()\n"
            "      !\n"
            "      ! Look-up mesh objects and loop limits for inter-grid "
            "kernels\n"
            "      !\n"
            "      fine_mesh_field2 => field2%get_mesh()\n"
            "      coarse_mesh_field1 => field1%get_mesh()\n"
            "      mmap_field2_field1 => coarse_mesh_field1%get_mesh_map("
            "fine_mesh_field2)\n"
            "      cell_map_field1 => mmap_field2_field1%"
            "get_whole_cell_map()\n")
        if distmem:
            inits += ("      ncell_fine_field2 = fine_mesh_field2%"
                      "get_last_halo_cell(depth=2)\n")
        else:
            inits += ("      ncell_fine_field2 = field2_proxy%vspace%"
                      "get_ncell()\n")
        inits += (
            "      ncpc_field2_field1 = mmap_field2_field1%"
            "get_ntarget_cells_per_source_cell()\n"
            "      !\n")
        assert inits in output

        if distmem:
            # We write out to the L1 halo on the coarse mesh which means
            # we require up-to-date values out to the L2 halo on the fine.
            # Since we are incrementing the coarse field we also need
            # up-to-date values for it in the L1 halo.
            halo_exchs = (
                "      ! Call kernels and communication routines\n"
                "      !\n"
                "      IF (field1_proxy%is_dirty(depth=1)) THEN\n"
                "        CALL field1_proxy%halo_exchange(depth=1)\n"
                "      END IF \n"
                "      !\n"
                "      IF (field2_proxy%is_dirty(depth=2)) THEN\n"
                "        CALL field2_proxy%halo_exchange(depth=2)\n"
                "      END IF \n"
                "      !\n"
                "      DO cell=1,coarse_mesh_field1%get_last_halo_cell(1)\n")
            assert halo_exchs in output

        # We pass the whole dofmap for the fine mesh (we are reading from).
        # This is associated with the second kernel argument.
        kern_call = (
            "        !\n"
            "        CALL restrict_kernel_code(nlayers, "
            "cell_map_field1(:,cell), ncpc_field2_field1, ncell_fine_field2, "
            "field1_proxy%data, field2_proxy%data, "
            "undf_any_space_1_field1, map_any_space_1_field1(:,cell), "
            "ndf_any_space_2_field2, undf_any_space_2_field2, "
            "map_any_space_2_field2)\n"
            "      END DO \n"
            "      !\n")
        assert kern_call in output

        if distmem:
            set_dirty = "      CALL field1_proxy%set_dirty()\n"
            assert set_dirty in output
