# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2023-2025, Science and Technology Facilities Council.
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
#
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
# Author: R. W. Ford, STFC Daresbury Laboratory

'''Module containing tests for the product2loop transformation.'''

import pytest

from psyclone.psyir.nodes import Reference, Literal
from psyclone.psyir.symbols import (
    REAL_TYPE, DataSymbol, INTEGER_TYPE, ScalarType)
from psyclone.psyir.transformations import (
    Product2LoopTrans, TransformationError)
from psyclone.tests.utilities import Compile


def test_initialise():
    '''Test that we can create an instance of the transformation and that
    _INTRINSIC_NAME is set up as expected.

    '''
    trans = Product2LoopTrans()
    assert isinstance(trans, Product2LoopTrans)
    assert trans._INTRINSIC_NAME == "PRODUCT"


def test_loop_body():
    '''Test that the _loop_body method works as expected.'''
    trans = Product2LoopTrans()
    lhs = Reference(DataSymbol("i", REAL_TYPE))
    rhs = Literal("1.0", REAL_TYPE)
    result = trans._loop_body(lhs, rhs)
    assert "i * 1.0" in result.debug_string()


@pytest.mark.parametrize("name,precision,one", [
    (ScalarType.Intrinsic.REAL, ScalarType.Precision.UNDEFINED, "1.0"),
    (ScalarType.Intrinsic.INTEGER, ScalarType.Precision.UNDEFINED, "1"),
    (ScalarType.Intrinsic.REAL, DataSymbol("r_def", INTEGER_TYPE),
     "1.0_r_def")])
def test_init_var(name, precision, one):
    '''Test that the _init_var method works as expected. Test with real,
    integer and with a specified precision.

    '''
    trans = Product2LoopTrans()
    datatype = ScalarType(name, precision)
    var_symbol = DataSymbol("var", datatype)
    result = trans._init_var(var_symbol)
    assert result.debug_string() == one


def test_str():
    '''Test that the str method, implemented in the parent class, works
    as expected.

    '''
    trans = Product2LoopTrans()
    assert str(trans) == ("Convert the PSyIR PRODUCT intrinsic to equivalent "
                          "PSyIR code.")


def test_name():
    '''Test that the name method, implemented in the parent class, works
    as expected.

    '''
    trans = Product2LoopTrans()
    assert trans.name == "Product2LoopTrans"


def test_validate():
    '''Test that the validate method, implemented in the parent class,
    works as expected.

    '''
    trans = Product2LoopTrans()
    with pytest.raises(TransformationError) as info:
        trans.validate(None)
    assert ("Error in Product2LoopTrans transformation. The supplied node "
            "argument is not an intrinsic, found 'NoneType'."
            in str(info.value))


def test_apply(fortran_reader, fortran_writer, tmpdir):
    '''Test that the apply method, implemented in the parent class, works
    as expected.

    '''
    code = (
        "subroutine product_test(array,n,m)\n"
        "  integer :: n, m\n"
        "  real :: array(10,20)\n"
        "  real :: result\n"
        "  result = product(array)\n"
        "end subroutine\n")
    expected = (
        "  result = 1.0\n"
        "  do idx = 1, 20, 1\n"
        "    do idx_1 = 1, 10, 1\n"
        "      result = result * array(idx_1,idx)\n"
        "    enddo\n"
        "  enddo\n")
    psyir = fortran_reader.psyir_from_source(code)
    # FileContainer/Routine/Assignment/IntrinsicCall
    intrinsic_node = psyir.children[0].children[0].children[1]
    trans = Product2LoopTrans()
    trans.apply(intrinsic_node)
    result = fortran_writer(psyir)
    assert expected in result
    assert Compile(tmpdir).string_compiles(result)
