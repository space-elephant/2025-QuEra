from iquhack_scoring import MoveScorer
from bloqade import move


def test_score():

    @move.vmove
    def qourier():
        q = move.NewQubitRegister(8)
        qubits = [q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]]
        indices = [0, 1, 2, 3, 4, 5, 6, 7]

        state = move.Init(qubits=qubits, indices=indices)

        state.gate[[0, 1]] = move.Move(state.storage[[0, 1]])
        state = move.core.GlobalCZ(state)

        state.gate[[2]] = move.Move(state.gate[[1]])
        state.gate[[1, 3]] = move.Move(state.storage[[2, 3]])
        state = move.GlobalCZ(state)

        state.gate[[4, 6]] = move.Move(state.gate[[1, 3]])
        state.gate[[1, 3, 5, 7]] = move.Move(state.storage[[4, 5, 6, 7]])
        state = move.GlobalCZ(state)

        move.Execute(state)

    expected_qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";

    qreg q[8];

    cz q[0], q[1];
    // first gate
    cz q[0], q[2];
    cz q[1], q[3];
    // second gate
    cz q[0], q[4];
    cz q[1], q[5];
    cz q[2], q[6];
    cz q[3], q[7];
    // third gate

    """
    print(MoveScorer(qourier, expected_qasm=expected_qasm).score())
