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

hD = local_hadamard([13])
h69G = local_hadamard([6, 9, 16])

@move.vmove
def main():
    q = move.NewQubitRegister(7)

    state = move.Init(qubits=[q[0],q[2],q[3],q[5],q[1],q[4],q[6]], indices=[0, 1, 2, 3, 4, 5, 6])

    state.gate[[2, 3, 4, 5, 9, 12, 13]] = move.Move(state.storage[[0, 1, 2, 3, 4, 5, 6]])

    # hadamard all but the input 6 @ 13
    state = global_hadamard(state)
    state = hD(state)
    state = move.GlobalCZ(atom_state=state)
    
    state.gate[[8, 12, 14, 16]] = move.Move(state.gate[[2, 5, 12, 13]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[6, 13]] = move.Move(state.gate[[9, 16]])
    state = move.GlobalCZ(atom_state=state)

    # hadamard 6 @ 13
    state = hD(state)
    
    state.gate[[7, 10]] = move.Move(state.gate[[12, 14]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[0, 2, 7]] = move.Move(state.gate[[7, 10, 13]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[5, 6, 16]] = move.Move(state.gate[[2, 3, 6]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[9, 12]] = move.Move(state.gate[[4, 7]])
    state = move.GlobalCZ(atom_state=state)

    # hadamard all but 1, 2, 3 @ 16, 6, 9 respectively
    state = global_hadamard(state)
    state = h69G(state)
    
    move.Execute(state)

aggressive.Fold(move.vmove)(main)

with open("assets/qasm/5.qasm") as f:qasm = f.read()

from iquhack_scoring import MoveScorer
analysis = MoveScorer(main,expected_qasm = qasm)

score = analysis.score()
print(score)
