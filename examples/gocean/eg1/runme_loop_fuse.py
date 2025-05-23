# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2017-2025, Science and Technology Facilities Council.
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
# Authors: R. W. Ford, A. R. Porter and S. Siso, STFC Daresbury Lab

'''A simple test script showing loop-fusion with PSyclone.
In order to use it you must first install PSyclone like so:

 >>> pip install --user psyclone

(or see the Getting Going section in the User Guide). Once PSyclone
is installed this script may be run by doing:

 >>> python runme_loop_fuse.py

This should generate a lot of output, ending with generated
Fortran. In subroutine invoke_0 you will see the loop-fused code:

 >>>    SUBROUTINE invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
 >>>    ...
 >>>      DO j=2,jstop
 >>>        DO i=2,istop+1
 >>>          CALL compute_cu_code(i, j, cu_fld%data, p_fld%data, u_fld%data)
 >>>          CALL compute_cv_code(i, j, cv_fld%data, p_fld%data, v_fld%data)
 >>>          CALL compute_z_code(i, j, z_fld%data, p_fld%data, u_fld%data, \
 >>>                              v_fld%data, p_fld%grid%dx, p_fld%grid%dy)
 >>>          CALL compute_h_code(i, j, h_fld%data, p_fld%data, u_fld%data, \
 >>>                              v_fld%data)
 >>>        END DO
 >>>      END DO
 >>>    END SUBROUTINE invoke_0

'''

from psyclone.parse.algorithm import parse
from psyclone.psyGen import PSyFactory, TransInfo
from psyclone.psyir.backend.fortran import FortranWriter

API = "gocean"
_, INVOKEINFO = parse("shallow_alg.f90", api=API)
PSY = PSyFactory(API, distributed_memory=False).create(INVOKEINFO)

# Print the vanilla, generated Fortran
writer = FortranWriter()
print(writer(PSY.container))

print(PSY.invokes.names)
SCHEDULE = PSY.invokes.get('invoke_0').schedule
print(SCHEDULE.view())

TRANS_INFO = TransInfo()
print(TRANS_INFO.list)
FUSE_TRANS = TRANS_INFO.get_trans_name('LoopFuseTrans')

# fuse all outer loops
FUSE_TRANS.apply(SCHEDULE.children[0],
                 SCHEDULE.children[1])
FUSE_TRANS.apply(SCHEDULE.children[0],
                 SCHEDULE.children[1])
FUSE_TRANS.apply(SCHEDULE.children[0],
                 SCHEDULE.children[1])
print(SCHEDULE.view())

# fuse all inner loops
FUSE_TRANS.apply(SCHEDULE.children[0].loop_body[0],
                 SCHEDULE.children[0].loop_body[1])
FUSE_TRANS.apply(SCHEDULE.children[0].loop_body[0],
                 SCHEDULE.children[0].loop_body[1])
FUSE_TRANS.apply(SCHEDULE.children[0].loop_body[0],
                 SCHEDULE.children[0].loop_body[1])
print(SCHEDULE.view())

print(writer(PSY.container))
