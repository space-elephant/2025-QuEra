#!/usr/bin/env python
# coding: utf-8

# In[1]:




# In[ ]:


from bloqade import move
from kirin.passes import aggressive
from math import pi

def local_e(indices):
    @move.vmove
    def convert(state:move.core.AtomState) -> move.core.AtomState:
        state = move.LocalXY(atom_state=state,x_exponent=0.25 * pi,axis_phase_exponent=0.0,indices=indices)
        return state
    return convert

def local_anti_e(indices):
    @move.vmove
    def convert(state:move.core.AtomState) -> move.core.AtomState:
        state = move.LocalXY(atom_state=state,x_exponent=-0.25 * pi,axis_phase_exponent=0.0,indices=indices)
        return state
    return convert

def local_t(indices):
    @move.vmove
    def convert(state:move.core.AtomState) -> move.core.AtomState:
        state = move.LocalRz(atom_state=state,phi=0.25 * pi,indices=indices)
        return state
    return convert

def local_hadamard(indices):
    @move.vmove
    def convert(state:move.core.AtomState) -> move.core.AtomState:
        state = move.LocalXY(atom_state=state,x_exponent=1.0 * pi,axis_phase_exponent=0.0,indices=indices)
        state = move.LocalXY(atom_state=state,x_exponent=-0.5 * pi,axis_phase_exponent=-0.5 * pi,indices=indices)
        return state
    return convert

e1 = local_e([1])
anti_e3 = local_anti_e([3])
anti_e2 = local_anti_e([2])
t2 = local_t([2])
h3 = local_hadamard([3])

@move.vmove
def main():
    q = move.NewQubitRegister(3)

    # bit 0, 2 control bit 1
    state = move.Init(qubits=[q[0],q[2],q[1]], indices=[0, 1, 2])

    # edit bit 1
    state.gate[[0, 2, 3]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = anti_e2(state)
    state.gate[[1]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(atom_state=state)
    state = e1(state)
    state.gate[[2]] = move.Move(state.gate[[1]])
    state.gate[[0, 2, 3]] = move.Move(state.storage[[0, 1, 2]])
    state = move.GlobalCZ(atom_state=state)
    state = anti_e2(state)
    state.gate[[1]] = move.Move(state.gate[[2]])
    state = move.GlobalCZ(atom_state=state)
    state = e1(state)

    # work with bits 0 and 2
    state.gate[[2]] = move.Move(state.gate[[0]])
    
    # T, H on bit 2
    state = move.LocalXY(atom_state=state,x_exponent=0.5 * pi,axis_phase_exponent=-0.5 * pi,indices=[3])
    state = move.LocalXY(atom_state=state,x_exponent=-0.75 * pi,axis_phase_exponent=0.0 * pi,indices=[3])
    
    state = move.GlobalCZ(atom_state=state)
    state = anti_e3(state)
    state = t2(state)
    state = move.GlobalCZ(atom_state=state)
    state = h3(state)
    
    move.Execute(state)

aggressive.Fold(move.vmove)(main)

with open("assets/qasm/1.2.qasm") as f:qasm = f.read()

from iquhack_scoring import MoveScorer
analysis = MoveScorer(main,expected_qasm = qasm)

score = analysis.score()
print(score)
