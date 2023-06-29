#Code to explore the possibility of encoding a message in Qubits using amplitudes.
#Findings: Very High error with close to no benefit

from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector, plot_bloch_multivector
from math import sqrt, pi
import numpy as np
import math
import string
import binascii

def createCircuit(statevector):
    num_qubits = int(len(statevector).bit_length() - 1)
    circuit = QuantumCircuit(num_qubits)
    circuit.initialize(statevector, range(num_qubits))
    return circuit
    
def stringToBinary(strin):
    string= strin
    binary = ""
    for char in string:
        binary += format(ord(char), '08b')  # Convert character to 8-bit binary string
    return binary
    
def encoder(input_string, a, b):
    binary= str(stringToBinary(input_string))
    lenBinary= len(binary)

    #print(binary)
    #print(len(binary))
    
    closest_power = closest_power_of_2(lenBinary)


    count1= binary.count('1')
    count0= binary.count('0')

    convention0= generate_list(count0, count1, lenBinary, a, b)[0]
    convention1= generate_list(count0, count1, lenBinary, a, b)[-1]

    #print("0: ", convention0)
    #print("1: ", convention1)

    statevector=[]
    for i in binary:
        if i== '0':
            statevector.append(convention0)
        else:
            statevector.append(convention1)

    while(is_power_of_two(len(statevector)) == False):
        statevector.append(0)

    return createCircuit(statevector), binary
    

def is_power_of_two(num):
    # Check if the number is positive
    if num <= 0:
        return False

    # Keep dividing the number by 2 until it becomes 1
    while num > 1:
        if num % 2 != 0:
            return False
        num /= 2

    return True

def closest_power_of_2(n):
    if n <= 0:
        return 0

    power = math.floor(math.log2(n))
    lower_power = 2 ** power
    upper_power = 2 ** (power + 1)

    if abs(n - lower_power) < abs(n - upper_power):
        return lower_power
    else:
        return upper_power


def generate_list(x, y, lenBinary, a, b):
    result = [a] * x + [b] * y
    if a != b:
        norm_factor = (x * a**2 + y * b**2)**0.5
        result = [num / norm_factor for num in result]
    return result

def verify_sum_of_squares(lst):
    sum_of_squares = sum(num**2 for num in lst)
    return sum_of_squares == 1

def calculate_mean(numbers):
    if len(numbers) == 0:
        return 0

    total_sum = sum(numbers)
    mean = total_sum / len(numbers)
    return mean

def decoder(circuit):
    qsim= Aer.get_backend("aer_simulator")
    dbinary=""
    circuit.measure_all()
    result= qsim.run(circuit, shots=10000).result()
    
    counts = result.get_counts(circuit)
    all_substates = [format(i, '0{}b'.format(circuit.num_qubits)) for i in range(2**circuit.num_qubits)]
    stateVector=[]
    stateVectorForMean=[]
    for substate in all_substates:
        count = counts.get(substate, 0)
        stateVector.append(count)
        if(count!=0):
            stateVectorForMean.append(count)


    


    '''
    sorted_keys = sorted(result.get_counts().keys(), key=int)

    stateVector=[]
    for i in sorted_keys:
        stateVector.append(result.get_counts()[i])
    '''
    
    mean= calculate_mean(stateVectorForMean)

    for num in stateVector:
        if num>=mean:
            dbinary+="1"
        else:
            dbinary+="0"
    
    #print(dbinary)
    #print(len(dbinary))
    return dbinary


qc, binary= encoder("Daniel", 2, 5)
dbinary= decoder(qc)
realDbinary=""

for i in range(0, len(binary)):
    realDbinary+=dbinary[i]


print(len(binary))
print(binascii.unhexlify('%x' % int(binary, 2)).decode('utf-8'))
print(binascii.unhexlify('%x' % int(realDbinary, 2)).decode('utf-8'))

percentage=0
for i in range(0, 99, 1):
    qc, binary= encoder("Daniel", 2, 5)
    dbinary= decoder(qc)
    realDbinary=""

    for i in range(0, len(binary)):
        realDbinary+=dbinary[i]

    if(binascii.unhexlify('%x' % int(binary, 2)).decode('utf-8') == binascii.unhexlify('%x' % int(realDbinary, 2)).decode('utf-8')):
        percentage+=1

print(percentage,"percent accurate")



