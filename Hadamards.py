#Code to play around with sandwiching different gates using Hadamard

from qiskit import QuantumCircuit, assemble, Aer, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from math import sqrt, pi

#Start an Aer instance (Simulator)
sim= Aer.get_backend("aer_simulator")

#Creating a quantum circuit
qc= QuantumCircuit(1, 1)
qc.h(0)
print("Sandwiching Gates with Hadamard\n")

print("---------Menu---------")
print("1: X\n2: Y\n3: Z\n4: P\n5: S\n6: T\n7: U")
choice= int(input("Enter your choice:"))

if(choice==1):
    print("X Gate selected")
    qc.x(0)
elif(choice==2):
    print("Y Gate selected")
    qc.y(0)
elif(choice==3):
    print("Z Gate selected")
    qc.z(0)
elif(choice==4):
    print("P Gate selected")
    phase= float(input("Enter the desired phase: Should be a fraction to be multiplied by pi: "))
    qc.p(pi*phase, 0)
elif(choice==5):
    print("S Gate selected")
    qc.s(0)
elif(choice==6):
    print("T Gate selected")
    qc.t(0)
elif(choice==7):
    print("U Gate selected")
    theta= float(input("Enter theta value: Should be a fraction to be multiplied by pi: "))
    phi= float(input("Enter phi value: Should be a fraction to be multiplied by pi: "))
    lamda= float(input("Enter lamda value: Should be a fraction to be multiplied by pi: "))
    qc.u(theta*pi, phi*pi, lamda*pi, 0)



qc.h(0)
qc.save_statevector()


#Running a job on the simulator and storing results
result = sim.run(transpile(qc, sim)).result()

#Different attributes of the result include:
counts= result.get_counts()
stateVector= result.get_statevector()

plot_bloch_multivector(stateVector)



