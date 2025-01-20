#!/g/data/hh5/public/apps/miniconda3/envs/analysis3/bin/python
## Scott Wales 2025

from psyclone.psyir.nodes import *
from psyclone.domain.common.algorithm import *

# Mapping of (module, routine) to modifications to make
lower_variables = {}

# Create the lookup table key for a routine
def routine_key(routine):
    return (routine.symbol.interface.container_symbol.name, routine.symbol.name)

# Modify arguments on the psy layer
def trans_psycall(psyir: FileContainer) -> None:
    # Variables to lower
    lower = ["neighbours", "born", "die"]

    # Save initial values of lowered variables
    initial = {}
    for assign in psyir.walk(Assignment):
        if assign.lhs.name in lower:
            initial[assign.lhs.name] = assign.rhs.copy()

    # Find the invokes
    for call in psyir.walk(Call):
        symbol_table = call.ancestor(Routine).symbol_table

        # Pop any of the arguments we want to lower
        to_detach = []
        for i,c in enumerate(call.children[1:]):
            if c.name in lower:
                to_detach.append((i,c,initial[c.name]))
        [c[1].detach() for c in to_detach]

        # Append arguments
        to_append = ['grid']
        to_append = [symbol_table.lookup(s) for s in to_append]
        call.children.extend([Reference(s) for s in to_append])

        lower_variables[routine_key(call.routine)] = {
                'to_detach': to_detach,
                'to_append': to_append,
                }


def trans(psyir: FileContainer) -> None:
    for routine in psyir.walk(Routine):
        process_kernel(routine)


def process_kernel(routine):
    key = (routine.parent.name, routine.name)
    
    if key in lower_variables:
        for i,c,initial in lower_variables[key]['to_detach'][::-1]:
            symbol = routine.symbol_table.pop_argument(i)
            assign = Assignment().create(Reference(symbol), initial)
            routine.children.insert(0, assign)

        for s in lower_variables[key]['to_append']:
            routine.symbol_table.append_argument(s)


