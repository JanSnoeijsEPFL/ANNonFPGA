#translating EDF files from database (full dataset for patient = 1)
#This file reduces the input resolution 
# This combines CNN + LSTM algorithm for EEG sequence classification  
import pyedflib
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
import os
#import pandas as pd
import re
import test_data_gen
import target_data_gen
from test_data_gen import get_data
from target_data_gen import get_sizes_train
from keras.layers import Dense, Activation, LSTM, Dropout, Bidirectional, TimeDistributed, Conv2D, MaxPooling2D, Flatten


#############################################################################
#TRAINING SET

np.random.seed(0)
#defining parameters
output = 1
#X=np.array(sigbufs
batch_size = 100 #(length)
batch_mod = 10000
dataset_size = 18
initial_file = 1


X, Y = list(), list()




#**********************CALLLING DATA GENERATOR FUNCTION ***********************
X, input_size, length = get_data(X, dataset_size, initial_file)
#******************************************************************************

# #Defining sizes for input/target data
# Y=np.zeros((dataset_size, batch_mod, output))
# #yhat=np.zeros((dataset_size, batch_mod, output))


# #***********************CALLING TARGET GENERATOR FUNCTION**********************
# file = 'chb01-summary.txt'
# Y = target_gen(output, batch_mod, dataset_size, batch_size, file)
# #******************************************************************************




   
# #RESHAPING ACCORDING TO NEW DATASET SIZE AND DATA SET SELECTION
# #DEFINING NEW SHAPES

# #inputs
input_size_new = 23
# #elements of each frame
batch_size_new = 400
# #time steps equivalent 
timesteps= 5
# #number of sequences
seq_number = 50
# #Re-defining dataset size for training
dataset_size = 18


#Defining sizes for input/target data
X_new=np.zeros((seq_number*dataset_size, timesteps, input_size_new, batch_size_new, 1))
#yhat=np.zeros((dataset_size, batch_mod, output))
Y_new=np.zeros((seq_number*dataset_size, output))



for m in range(0,dataset_size):
 if (m == 0 or  m == 1 or m == 2 or m == 3):
  if m == 0:
   initial_time = 0
  if m == 2:
   initial_time = 100000
  if m == 3:
   initial_time = 500000
  if m == 4:
   initial_time = 500000
 else:
  initial_time = 0
 print('initial time:', initial_time)
 for i in range(0,seq_number):
  for j in range(0,timesteps):
   initial = initial_time+(i*batch_size_new*timesteps)+j*batch_size_new
   final = initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new)
   #print(initial_time+(i*batch_size_new*timesteps)+j*batch_size_new)
   #print(initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new))
   X_new[seq_number*m+i,j,:,0:batch_size_new,0] =  X[m,0,0,0:input_size_new,initial:final,0] 


########################################################################################################
# #Adding extra training -
# file = 17

# initial_time = 200000

# for i in range(0,seq_number):
 # for j in range(0,timesteps):
  # initial = initial_time+(i*batch_size_new*timesteps)+j*batch_size_new
  # final = initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+j*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new))
  # X_new[seq_number*17+i,j,:,0:batch_size_new,0] =  X[file-1,0,0,0:input_size_new,initial:final,0]    
  
# initial_time = 300000

# for i in range(0,seq_number):
 # for j in range(0,timesteps):
  # initial = initial_time+(i*batch_size_new*timesteps)+j*batch_size_new
  # final = initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+j*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new))
  # X_new[seq_number*18+i,j,:,0:batch_size_new,0] =  X[file-1,0,0,0:input_size_new,initial:final,0]  


# initial_time = 100000

# for i in range(0,seq_number):
 # for j in range(0,timesteps):
  # initial = initial_time+(i*batch_size_new*timesteps)+j*batch_size_new
  # final = initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+j*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new))
  # X_new[seq_number*19+i,j,:,0:batch_size_new,0] =  X[file-1,0,0,0:input_size_new,initial:final,0]    
  
# initial_time = 0

# for i in range(0,seq_number):
 # for j in range(0,timesteps):
  # initial = initial_time+(i*batch_size_new*timesteps)+j*batch_size_new
  # final = initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+j*batch_size_new)
  # #print(initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new))
  # X_new[seq_number*20+i,j,:,0:batch_size_new,0] =  X[file-1,0,0,0:input_size_new,initial:final,0]    

   
   #####################################################################################################
   
 
max_value = np.amax(abs(X_new))
min_value = np.amin(abs(X_new))
# print('MAX VALUE', max_value)
X_new = X_new/max_value

Y_new[seq_number*0+46:seq_number*0+50,output-1] = 1
Y_new[seq_number*1+43:seq_number*1+50,output-1] = 1
Y_new[seq_number*2+5:seq_number*2+15,output-1] = 1
Y_new[seq_number*3+26:seq_number*3+34,output-1] = 1



# plt.plot(X[2,0,0,0,:,0])
# plt.plot(X[2,0,0,1,:,0])
# plt.show()
# plt.plot(X[3,0,0,0,:,0])
# plt.plot(X[3,0,0,1,:,0])
# plt.show()
#Assigning targets (manually)
#Y[0,2,:] = 1
#Y[3,2,:] = 1


model = Sequential()
model.add(TimeDistributed(Conv2D(2,(2,2), activation = 'relu'), input_shape=(None,input_size_new,batch_size_new,1)))
model.add(TimeDistributed(MaxPooling2D(pool_size=(2,2))))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(50))
model.add(Dense(output, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam')

print(model.summary())

model.fit(X_new,Y_new, epochs=50)
#Trying model
yhat = model.predict(X_new, verbose=0)
file1 = open("CNN_LSTM_dataset_train.txt", 'ab')
np.savetxt(file1, yhat, delimiter="," )
file1.close()

#########################################################################################################
#########################################################################################################

#Generating data test 1
test_files = 20

initial_file = 19
#Loading data test
X, input_size, length = get_data(X, test_files, initial_file)

# #Defining sizes for input/target data
X_test=np.zeros((seq_number*test_files, timesteps, input_size_new, batch_size_new, 1))

for m in range(0,test_files):
 if m == 15:
  initial_time = 600000
 elif m == 16:
  initial_time = 400000
 else:
  initial_time = 0
 print('initial time:', initial_time)
#initial_time = 400000
 for i in range(0,seq_number):
  for j in range(0,timesteps):
   initial = initial_time+(i*batch_size_new*timesteps)+j*batch_size_new
   final = initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new)
   #print(initial_time+(i*batch_size_new*timesteps)+j*batch_size_new)
   #print(initial_time+(i*batch_size_new*timesteps)+((j+1)*batch_size_new))
   X_test[seq_number*m+i,j,:,0:batch_size_new,0] =  X[m,0,0,0:input_size_new,initial:final,0] 
   #if  (m == 0 and i == 0):
 
   

   
max_value_2 = np.amax(abs(X_test))
min_value = np.amin(abs(X_test))
# print('MAX VALUE', max_value)
X_test = X_test/max_value_2


yhat_test = model.predict(X_test, verbose=0)
file2 = open("CNN_LSTM_dataset_test_17_dataset_onset_400batch_50_ouputs.txt", 'ab')
np.savetxt(file2, yhat_test, delimiter="," )
file2.close()

# ########################################################################################################
