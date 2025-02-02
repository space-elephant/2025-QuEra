#!/usr/bin/env python
# coding: utf-8

# In[1]:




# In[ ]:


from bloqade import move
from kirin.passes import aggressive
from math import pi

def local_hadamard(indices):
    @move.vmove
    def convert(state:move.core.AtomState) -> move.core.AtomState:
        state = move.LocalXY(atom_state=state,x_exponent=1.0 * pi,axis_phase_exponent=0.0,indices=indices)
        state = move.LocalXY(atom_state=state,x_exponent=-0.5 * pi,axis_phase_exponent=-0.5 * pi,indices=indices)
        return state
    return convert

@move.vmove
def global_hadamard(state:move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalXY(atom_state=state,x_exponent=1.0 * pi,axis_phase_exponent=0.0)
    state = move.GlobalXY(atom_state=state,x_exponent=-0.5 * pi,axis_phase_exponent=-0.5 * pi)
    return state

h59 = local_hadamard([5, 9])
h37B = local_hadamard([3, 7, 11])

@move.vmove
def main():
    q = move.NewQubitRegister(9)

    state = move.Init(qubits=[q[3],q[1],q[2],q[0],q[4],q[5],q[6],q[7],q[8]], indices=[0, 1, 2, 3, 4, 5, 6, 7, 8])

    # first two CX gates, plus shifting
    state.gate[[5, 8, 9]] = move.Move(state.storage[[0, 3, 6]])
    state = h59(state)
    state = move.GlobalCZ(atom_state=state)
    state.gate[[4]] = move.Move(state.gate[[8]])
    state = move.GlobalCZ(atom_state=state)
    state = h59(state)
    state.gate[[1]] = move.Move(state.gate[[4]])

    # explicit hadamard, plus setup for CZ as CX
    state.gate[[0, 2, 4, 6, 8, 10]] = move.Move(state.storage[[1, 2, 4, 5, 7, 8]])
    state = global_hadamard(state)

    # the global CZ operations
    state = move.GlobalCZ(atom_state=state)
    state.gate[[3, 7, 11]] = move.Move(state.gate[[1, 5, 9]])
    state = move.GlobalCZ(atom_state=state)

    # hadamard all but those that were the control bits earlier
    state = global_hadamard(state)
    state = h37B(state)
    
    move.Execute(state)

aggressive.Fold(move.vmove)(main)

with open("assets/qasm/4.qasm") as f:qasm = f.read()

from iquhack_scoring import MoveScorer
analysis = MoveScorer(main,expected_qasm = qasm)

score = analysis.score()
print(score)
