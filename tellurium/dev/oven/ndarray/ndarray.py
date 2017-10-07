"""
Some testing with ndarrays for storage
"""
import numpy as np
import tellurium as te

r = te.loada("""
model test()
    J0: S1 -> S2; k1*S1;
    S1=10.0; S2=0.0;
    k1=0.1;
end
""")
print(r)



N1 = 3
N2 = 4
N3 = 5

test = np.empty(shape=(N1, N2, N3), dtype=object)

for k in range(N1):
    r.reset()
    s = r.simulate(start=0, end=5, steps=5)
    test[k, 0, 0] = s




print(test)
print("*" * 80)
print(test[0,0,0])



