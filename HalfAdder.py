#To a execute a quantum half adder circuit


from qiskit import QuantumCircuit, Aer

#Start an Aer instance (Simulator)
qsim= Aer.get_backend("aer_simulator")

#A set function to change a qubit to our desired state
def set(qubit, desired):
    current=0
    qc.measure(qubit, current)
    if(current != desired):
        qc.x(qubit)

#Create the circuit and define inputs
#Uses 4 qubits. Q2 will hold the sum and Q3 will hold the carry
qc= QuantumCircuit(4, 2)
set(0, 1)
set(1, 1)

#Circuit Operation
#To find sum, perform XOR operation and store in Q2
#To perform carry, perform and operation and store in Q3
qc.cx(0, 2)
qc.cx(1, 2)
qc.ccx(0, 1, 3)

#Measure the qubits and draw the circuit
qc.measure([2,3], [0,1])
qc.draw()

#Running it through the simulator
job= qsim.run(qc)

result= job.result()
print("The result is: ", result.get_counts())

