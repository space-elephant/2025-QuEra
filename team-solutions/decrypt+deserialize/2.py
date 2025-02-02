#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bloqade import move
import math
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi


# In[2]:


@move.vmove
def global_hadamard(state: move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalXY(atom_state = state,x_exponent = 0.25 * pi, axis_phase_exponent = 0.5 * pi)
    state = move.GlobalRz(atom_state = state, phi = pi)
    state = move.GlobalXY(atom_state = state,x_exponent = -0.25 * pi, axis_phase_exponent = 0.5 * pi)
    return state


# In[3]:


@move.vmove
def main():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    state.gate[[0, 1]] = move.Move(state.storage[[1, 2]])
    state = move.LocalXY(atom_state=state,x_exponent= 0.25 * pi,axis_phase_exponent=0.0,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.25 * pi,axis_phase_exponent=0.0,indices=[1])
    state = move.GlobalCZ(atom_state = state)
    state.storage[[1]] = move.Move(state.gate[[0]])
    state.gate[[0]] = move.Move(state.storage[[0]])
    state = move.LocalXY(atom_state=state,x_exponent= 0.125 * pi,axis_phase_exponent=0.0,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.125 * pi,axis_phase_exponent=0.0,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state.storage[[2]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalXY(atom_state=state,x_exponent= 0.25 * pi,axis_phase_exponent=0.0,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = move.LocalXY(atom_state=state,x_exponent= -0.25 * pi,axis_phase_exponent=0.0,indices=[1])
    state = move.GlobalCZ(atom_state=state)
    state = global_hadamard(state)
    move.Execute(state)


# In[4]:


expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


h q[2];

// Operation: CRz(0.5π)(q(1), q(2))
cx q[1],q[2];
u3(0,pi*1.25,pi*0.5) q[2];
cx q[1],q[2];
u3(0,pi*1.75,pi*0.5) q[2];

// Operation: CRz(0.25π)(q(0), q(2))
cx q[0],q[2];
u3(0,pi*1.375,pi*0.5) q[2];
cx q[0],q[2];
u3(0,pi*1.625,pi*0.5) q[2];

h q[1];

// Operation: CRz(0.5π)(q(0), q(1))
cx q[0],q[1];
u3(0,pi*1.25,pi*0.5) q[1];
cx q[0],q[1];
u3(0,pi*1.75,pi*0.5) q[1];

h q[0];

"""
aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)


# In[ ]:




