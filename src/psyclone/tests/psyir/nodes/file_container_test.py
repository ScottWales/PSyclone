# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2021-2025, Science and Technology Facilities Council.
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
# Author R. W. Ford, STFC Daresbury Lab
# Modified S. Siso, STFC Daresbury Lab
# -----------------------------------------------------------------------------

''' Performs py.test tests on the FileContainer PSyIR node. '''

import pytest
from psyclone.alg_gen import NoInvokesError
from psyclone.psyir.nodes import Routine, FileContainer, Container
from psyclone.psyir.symbols import SymbolTable, DataSymbol, REAL_SINGLE_TYPE
from psyclone.psyir.backend.fortran import FortranWriter
from psyclone.psyir.nodes.node import colored
from psyclone.tests.utilities import get_invoke


def test_file_container_init():
    '''Test that a FileContainer can be created and that its name is
    stored.

    '''
    file_container = FileContainer("test")
    assert isinstance(file_container, FileContainer)
    assert isinstance(file_container, Container)
    assert file_container.name == "test"


def test_file_container_node_str():
    '''Test that a FileContainer instance outputs the expected text for the
    view method.

    '''
    file_container = FileContainer("test")
    coloredtext = colored("FileContainer", FileContainer._colour)
    assert coloredtext+"[test]" in file_container.node_str()


def test_file_container_str():
    '''Test that the 'str' of a FileContainer instance gives the expected
    output.

    '''
    file_container = FileContainer("test")
    assert "FileContainer[name='test']\n" in str(file_container)


def test_file_container_create():
    '''Test that the create method in the Container class correctly
    creates a FileContainer instance.

    '''
    symbol_table = SymbolTable()
    symbol_table.add(DataSymbol("tmp", REAL_SINGLE_TYPE))
    module = Container.create("mod_1", symbol_table, [])
    program = Routine.create("prog_1", SymbolTable(), [], is_program=True)
    file_container = FileContainer.create(
        "container_name", SymbolTable(), [module, program])
    assert isinstance(file_container, FileContainer)
    result = FortranWriter().filecontainer_node(file_container)
    assert result == (
        "module mod_1\n"
        "  implicit none\n"
        "  real, public :: tmp\n"
        "  public\n\n"
        "  contains\n\n"
        "end module mod_1\n"
        "program prog_1\n\n\n"
        "end program prog_1\n")


def test_invokes_property(capsys):
    ''' Test that the invokes property can find the associated Invokes object
    in order to emulate legacy trans scripts that received a PSy object as
    input.
    '''
    _, invoke = get_invoke("1_single_invoke.f90", "lfric", idx=0)

    # Get a psykal FileContainer
    filecontainer = invoke.schedule.root

    # This can be used as if it were a PSy
    assert len(filecontainer.invokes.invoke_list) == 1
    assert "invoke_0_testkern_type" in filecontainer.invokes.names

    # The deprecation warning message was printed
    captured = capsys.readouterr()
    assert ("Deprecation warning: PSyclone script uses the legacy "
            "transformation signature 'def trans(psy)', please update the "
            "script to receive the root psyir node as argument."
            in captured.err)

    # If produces an error if it doesn't come from a generated PSy-layer
    filecontainer = FileContainer("test")
    with pytest.raises(NoInvokesError) as err:
        _ = filecontainer.invokes
    assert ("No InvokeSchedule found in 'test', does it come from a "
            "PSyKAl file that conforms to the GOcean or LFRic API?"
            in str(err.value))
