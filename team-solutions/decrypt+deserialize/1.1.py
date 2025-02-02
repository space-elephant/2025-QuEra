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
        #state = move.LocalXY(atom_state=state,x_exponent=1.0 * pi,axis_phase_exponent=0.0,indices=indices)
        state = move.LocalXY(atom_state=state,x_exponent=-0.5 * pi,axis_phase_exponent=-0.5 * pi,indices=indices)
        state = move.LocalRz(atom_state=state,phi=1.0 * pi,indices=indices)
        return state
    return convert

h2 = local_hadamard([2])

@move.vmove
def main():
    q = move.NewQubitRegister(3)

    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0, 1, 2])

    state.gate[[0, 1, 3]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state.gate[[2]] = move.Move(state.gate[[1]])

    state = h2(state)
    state = move.GlobalCZ(atom_state=state)
    state = h2(state)
    
    move.Execute(state)

aggressive.Fold(move.vmove)(main)

with open("assets/qasm/1.1.qasm") as f:qasm = f.read()

from iquhack_scoring import MoveScorer
analysis = MoveScorer(main,expected_qasm = qasm)

score = analysis.score()
print(score)

