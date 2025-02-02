#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bloqade import move
import math
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

pi = math.pi
beta1 = 0.15524282950959892
alpha1 = 0.5550603400685824/pi
beta2 = 0.2858383611880559
alpha2 = 0.29250781484335187/pi


# In[2]:


@move.vmove
def E1(state: move.core.AtomState, target) -> move.core.AtomState:
    state = move.LocalRz(state, beta1 / 2, indices = target)
    state = move.GlobalCZ(state)
    state = move.LocalRz(state, -1 * beta1 / 2, indices = target)
    state = move.GlobalCZ(state)


# In[3]:


@move.vmove
def E2(state: move.core.AtomState, target) -> move.core.AtomState:
    state = move.LocalRz(state, beta2 / 2, indices = target)
    state = move.GlobalCZ(state)
    state = move.LocalRz(state, -1 * beta2 / 2, indices = target)
    state = move.GlobalCZ(state)


# In[4]:


@move.vmove
def local_hadamard(state: move.core.AtomState, indices) -> move.core.AtomState:
    state = move.LocalXY(atom_state=state,x_exponent=1.0 * pi,axis_phase_exponent=0.0,indices=indices)
    state = move.LocalXY(atom_state=state,x_exponent=-0.5 * pi,axis_phase_exponent=-0.5 * pi,indices=indices)
    return state


# In[5]:


@move.vmove
def global_hadamard(state: move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalXY(state, 0.25 * pi, 0.5 * pi)
    state = move.GlobalRz(state, pi)
    state = move.GlobalXY( state, -0.25 * pi, 0.5 * pi)
    return state


# In[6]:


def Rot2(state: move.core.AtomState, target) -> move.core.AtomState:
    state = move.LocalRz(state, alpha2, indices = target)


# In[7]:


def Rot1(state: move.core.AtomState, target) -> move.core.AtomState:
    state = move.LocalRz(state, alpha1, indices = target)


# In[11]:


@move.vmove
def main():
    q = move.NewQubitRegister(4)
    state = move.Init(qubits=[q[0],q[1],q[2], q[3]], indices=[0,1,2,3])
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    local_hadamard(state, [0])
    E1(state, [1])
    state.storage[[2]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[3]])
    E1(state, [1])
    state.storage[[3]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    E1(state, [1])
    local_hadamard(state, [[0, 1]])
    Rot1(state, [0])
    state.gate[[2]] = move.Move(state.gate[[1]])
    state.gate[[3]] = move.Move(state.storage[[2]])
    E1(state, [3])
    state.gate[[4]] = move.Move(state.gate[[3]])
    state.gate[3] = move.Move(state.storage[3])
    E1(state, [3])
    global_hadamard(state)
    local_hadamard(state, [3])
    state.gate[5] = move.Move(state.gate[3])
    state.gate[1] = move.Move(state.gate[2])
    Rot1(state, [1])
    E1(state, [1, 5])
    local_hadamard(state, [1, 4])
    Rot1(state, [4,5])
    state.gate[2] = move.Move(state.gate[1])
    state.gate[1] = move.Move(state.gate[5])
    state.gate[3] = move.Move(state.gate[4])
    E1(state, [1, 3])
    state.gate[5] = move.Move(state.gate[1])
    state.gate[1] = move.Move(state.gate[3])
    state.gate[4] = move.Move(state.gate[2])
    E1(state, [1,5])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 4]])
    state.gate[4] = move.Move(state.gate[1])
    E1(state, [5])
    global_hadamard(state)
    local_hadamard(state, [5])
    state = move.globalXY(state, alpha1)
    global_hadamard(state)
    state.storage[[2,3]] = move.Move(state.gate[4,5])

    #part 2
    state.gate[[0, 1]] = move.Move(state.storage[[0, 2]])
    local_hadamard(state, [0])
    E2(state, [1])
    state.storage[[2]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[3]])
    E2(state, [1])
    state.storage[[3]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    E2(state, [1])
    local_hadamard(state, [[0, 1]])
    Rot2(state, [0])
    state.gate[2] = move.Move(state.gate[1])
    state.gate[3] = move.Move(state.storage[2])
    E2(state, [3])
    state.gate[4] = move.Move(state.gate[3])
    state.gate[3] = move.Move(state.storage[3])
    E2(state, [3])
    global_hadamard(state)
    local_hadamard(state, [3])
    state.gate[5] = move.Move(state.gate[3])
    state.gate[1] = move.Move(state.gate[2])
    Rot2(state, [1])
    E2(state, [1, 5])
    local_hadamard(state, [1, 4])
    Rot2(state, [4,5])
    state.gate[2] = move.Move(state.gate[1])
    state.gate[1] = move.Move(state.gate[5])
    state.gate[3] = move.Move(state.gate[4])
    E2(state, [1, 3])
    state.gate[5] = move.Move(state.gate[1])
    state.gate[1] = move.Move(state.gate[3])
    state.gate[4] = move.Move(state.gate[2])
    E2(state, [1,5])
    state.storage[[0, 1]] = move.Move(state.gate[[0, 4]])
    state.gate[4] = move.Move(state.gate[1])
    E2(state, [5])
    global_hadamard(state)
    local_hadamard(state, [5])
    state = move.globalXY(state, alpha2)
    global_hadamard(state)
    move.Execute(state)


# In[ ]:


expected_qasm = """
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3)]
qreg q[4];


h q[0];
h q[1];
h q[2];
h q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[1];
sx q[0];
cx q[0],q[1];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
sxdg q[1];
s q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[1];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[0];
cx q[0],q[3];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[3];
cx q[3],q[0];
sxdg q[3];
s q[3];
cx q[0],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[0];
u3(pi*0.5,0,pi*0.75) q[2];
sx q[0];
cx q[0],q[2];
rx(pi*0.4223785852) q[0];
ry(pi*0.5) q[2];
cx q[2],q[0];
sxdg q[2];
s q[2];
cx q[0],q[2];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[0];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[2];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[1];
u3(pi*0.5,0,pi*0.75) q[2];
sx q[1];
cx q[1],q[2];
rx(pi*0.4223785852) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
sxdg q[2];
s q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[1];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[2];

rx(pi*0.1766811937) q[0];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[1];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[1];
cx q[1],q[3];
rx(pi*0.4223785852) q[1];
ry(pi*0.5) q[3];
cx q[3],q[1];
sxdg q[3];
s q[3];
cx q[1],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[1];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

// Gate: CZ**0.15524282950959892
u3(pi*0.5,0,pi*0.25) q[2];
u3(pi*0.5,0,pi*0.75) q[3];
sx q[2];
cx q[2],q[3];
rx(pi*0.4223785852) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
sxdg q[3];
s q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.8276214148,pi*1.0) q[2];
u3(pi*0.5,pi*0.3276214148,pi*1.0) q[3];

rx(pi*0.1766811937) q[1];
rx(pi*0.1766811937) q[2];
rx(pi*0.1766811937) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[1];
sx q[0];
cx q[0],q[1];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
sxdg q[1];
s q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[1];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[0];
cx q[0],q[3];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[3];
cx q[3],q[0];
sxdg q[3];
s q[3];
cx q[0],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[0];
u3(pi*0.5,pi*1.0,pi*1.25) q[2];
sx q[0];
cx q[0],q[2];
rx(pi*0.3570808194) q[0];
ry(pi*0.5) q[2];
cx q[2],q[0];
sxdg q[2];
s q[2];
cx q[0],q[2];
u3(pi*0.5,pi*0.3929191806,0) q[0];
u3(pi*0.5,pi*1.8929191806,0) q[2];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[2];
sx q[1];
cx q[1],q[2];
rx(pi*0.3570808194) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
sxdg q[2];
s q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.3929191806,0) q[1];
u3(pi*0.5,pi*1.8929191806,0) q[2];

rx(pi*0.0931081293) q[0];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[1];
cx q[1],q[3];
rx(pi*0.3570808194) q[1];
ry(pi*0.5) q[3];
cx q[3],q[1];
sxdg q[3];
s q[3];
cx q[1],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[1];
u3(pi*0.5,pi*1.8929191806,0) q[3];

// Gate: CZ**0.2858383611880559
u3(pi*0.5,pi*1.0,pi*0.75) q[2];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
sx q[2];
cx q[2],q[3];
rx(pi*0.3570808194) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
sxdg q[3];
s q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.3929191806,0) q[2];
u3(pi*0.5,pi*1.8929191806,0) q[3];

rx(pi*0.0931081293) q[1];
rx(pi*0.0931081293) q[2];
rx(pi*0.0931081293) q[3];

"""
aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm)
score = scorer.score()
print(score)

