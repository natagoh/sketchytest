import os
import platform
import re

# graph loss over time
# parsing log file to extract loss data
if __name__ == '__main__':
	# find the log file
	cwd = os.getcwd()

	if platform.system() == 'Windows':
	    dst = os.path.join(cwd, 'experiments\\base_model')
	else:
	    dst = os.path.join(cwd, 'experiments/base_model')

	for f in os.listdir(dst):
		if f == 'train.log':
			log = os.path.join(dst, f) 


	train_loss = []
	eval_loss = []
	epochs = []
	f = open(log, 'r').read().split()

	# get epochs
	for j in range(0, len(f)):
		if f[j] == "Epoch":
			epochs.append(j)

	# extract loss
	for j in range(0, len(epochs)):
		# epoch index +1 = train
		# epoch index +2 = eval
		train_loss.append(f[epochs[j]+11])
		eval_loss.append(f[epochs[j]+22])

	print(train_loss)
	print(eval_loss)

			

