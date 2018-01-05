# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2017-2018, Science and Technology Facilities Council
#
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
# Author: A. R. Porter, STFC Daresbury Lab

''' Tests for the CLAW interface implemented in PSyclone '''

import os
import pytest
from psyclone.transformations import TransformationError


# constants
BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "test_files", "dynamo0p3")

# Whether or not we run tests that require the Claw compiler is picked-up
# from a command-line flag. (This is set-up in conftest.py.)
TEST_CLAW = pytest.config.getoption("--with-claw")


def _fake_check_call(args, env=None):  # pylint:disable=unused-argument
    '''
    Function to be used to monkeypatch the check_call() function of
    the subprocess module.
    :param list args: List of items from which to construct system call
    :raises: subprocess.CalledProcessError
    '''
    from subprocess import CalledProcessError
    raise CalledProcessError(1, " ".join(args))


def test_omni_fe_error(monkeypatch):
    ''' Check that we raise the expected exception if the Omni frontend
    fails '''
    from psyclone.claw import omni_frontend
    import subprocess
    monkeypatch.setattr(subprocess, "check_call", _fake_check_call)
    with pytest.raises(subprocess.CalledProcessError) as err:
        omni_frontend("some_file.f90", "some_file.xml", ".")
    assert "F_Front -I. some_file.f90 -o some_file.xml" in str(err)


def test_run_claw(monkeypatch):
    ''' Check the _run_claw() routine in the claw module '''
    from psyclone.claw import _run_claw
    import subprocess
    monkeypatch.setattr(subprocess, "check_call", _fake_check_call)
    with pytest.raises(subprocess.CalledProcessError) as err:
        _run_claw(["."], "some_file.xml", "some_file.f90", "some_script.py")
    output = str(err)
    print output
    assert "java -Xmx200m -Xms200m -cp" in str(err)
    assert "jython.jar claw.ClawX2T --config-path=" in output
    assert ("-M. -f some_file.f90 -o some_file.xml.tmp.xml -script "
            "some_script.py some_file.xml" in output)


def test_api_from_ast():
    ''' Test for the utility routine that gives us the name of the PSyclone
    API to which a kernel object belongs '''
    from psyclone.dynamo0p3 import DynKern
    from psyclone.gocean1p0 import GOKern
    from psyclone.claw import _api_from_ast
    dkern = DynKern()
    api = _api_from_ast(dkern)
    assert api == "dynamo0.3"

    gkern = GOKern()
    api = _api_from_ast(gkern)
    assert api == "gocean1.0"

    no_kern = "not a kernel"
    with pytest.raises(TransformationError) as err:
        _ = _api_from_ast(no_kern)
    assert "Cannot determine API for kernel" in str(err)


def test_trans(tmpdir, monkeypatch):
    ''' Tests for the trans() routine '''
    import subprocess
    from psyclone.parse import parse
    from psyclone.psyGen import PSyFactory
    from psyclone import claw
    _, invoke_info = parse(os.path.join(BASE_PATH, "1_single_invoke.f90"),
                           api="dynamo0.3")
    psy = PSyFactory("dynamo0.3", distributed_memory=False).create(invoke_info)
    invoke = psy.invokes.invoke_list[0]
    kern = invoke.schedule.children[0].children[0]
    orig_name = kern.name[:]
    script_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "claw_trans.py")
    # Change to the pytest-supplied tmp dir so that we don't mess up our
    # space with generated files
    _ = tmpdir.chdir()

    if not TEST_CLAW:
        # Monkeypatch subprocess.check_call() so that it does
        # nothing. This means that we don't actually run Omni or Claw.
        monkeypatch.setattr(subprocess, "check_call",
                            lambda args, env=None: None)
        with pytest.raises(TransformationError) as err:
            _ = claw.trans([kern], script_file)
        # Check that we've raised the correct error about not finding the
        # XML output of the Omni Frontend
        assert "XcodeML/F representation of kernel {0}".format(orig_name) in \
            str(err)
        # Since we're not running Omni, we don't generate any xml files so also
        # monkeypatch the kernel-renaming routine so that it does nothing.
        monkeypatch.setattr(claw, "_rename_kernel",
                            lambda xml, name, mode: name+"_claw0")
    new_names = claw.trans([kern], script_file)

    assert new_names[orig_name] == orig_name + "_claw"


def test_rename_kern(tmpdir):
    ''' Check that _rename_kernel() works as it should '''
    import shutil
    from psyclone.claw import _rename_kernel
    # We use a copy of an XML file we prepared earlier so as not to have
    # to rely on Omni being installed
    xml_file = os.path.join(BASE_PATH, "testkern.xml")
    oldpwd = tmpdir.chdir()
    shutil.copy(xml_file, str(tmpdir))
    xml_file = os.path.join(str(tmpdir), "testkern.xml")
    new_base_name = _rename_kernel(xml_file, "next_sshu", "keep")
    assert new_base_name == "next_sshu_claw0"
    # Create a fake renamed kernel file
    with open("next_sshu_claw0_mod.f90", "w") as ffile:
        ffile.write("Hello")
    # Check that we get a different kernel name if "keep" is specified
    new_base_name = _rename_kernel(xml_file, "next_sshu", "keep")
    assert new_base_name == "next_sshu_claw1"
    new_base_name = _rename_kernel(xml_file, "next_sshu", "overwrite")
    assert new_base_name == "next_sshu_claw0"
    with pytest.raises(TransformationError) as err:
        _ = _rename_kernel(xml_file, "next_sshu", "abort")
    assert "next_sshu_claw0_mod.f90 already exists and renaming mode is" \
        in str(err)

    # Now check the transformed XCodeML
    new_kern_name = new_base_name + "_code"
    new_kern_type_name = new_base_name + "_type"
    new_mod_name = new_base_name + "_mod"

    from xml.dom import minidom
    with open(xml_file, "r") as xfile:
        xml_doc = minidom.parse(xfile)
        # Kernel is a type-bound procedure in the meta-data
        procs = xml_doc.getElementsByTagName("typeBoundProcedure")
        proc_name_list = []
        for proc in procs:
            bindings = proc.getElementsByTagName("binding")
            names = bindings[0].getElementsByTagName("name")
            proc_name_list.append(names[0].firstChild.data)
        assert new_kern_name in proc_name_list
        # Global symbols
        gsymbols = xml_doc.getElementsByTagName("globalSymbols")
        gids = gsymbols[0].getElementsByTagName("id")
        for gid in gids:
            if gid.getAttribute("sclass") == "ffunc":
                names = gid.getElementsByTagName("name")
                assert names[0].firstChild.data == new_mod_name
        # Global declarations
        gdeclns = xml_doc.getElementsByTagName("globalDeclarations")
        modefs = gdeclns[0].getElementsByTagName("FmoduleDefinition")
        assert modefs[0].getAttribute("name") == new_mod_name
        symbols = modefs[0].getElementsByTagName("symbols")
        symbol_ids = symbols[0].getElementsByTagName("id")
        found_ftype = False
        for sid in symbol_ids:
            class_attr = sid.getAttribute("sclass")
            if class_attr == "ftype_name":
                # The symbol table may hold more than one ftype (because it
                # includes symbols from use'd modules too) so
                # we can only be sure once we've seen them all
                names = sid.getElementsByTagName("name")
                if names[0].firstChild.data == new_kern_type_name:
                    found_ftype = True
            elif class_attr == "ffunc":
                names = sid.getElementsByTagName("name")
                assert names[0].firstChild.data == new_kern_name
        assert found_ftype
        # Function/routine definitions
        func_list = xml_doc.getElementsByTagName("FfunctionDefinition")
        names = func_list[0].getElementsByTagName("name")
        assert names[0].firstChild.data == new_kern_name
        sym_list = func_list[0].getElementsByTagName("id")
        for sym in sym_list:
            if sym.getAttribute("sclass") == "ffunc":
                names = sym.getElementsByTagName("name")
                assert names[0].firstChild.data == new_kern_name
