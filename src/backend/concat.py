import numpy as np 


def concat(v1, v2, i):
	combined = np.zeros(i+len(v2))
	combined[:len(v1)] = v1
	combined[i:-1] += v2
	combined[i:len(v1)] /= 2
	return combined



