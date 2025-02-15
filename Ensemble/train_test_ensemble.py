import cv2
import numpy as np
import sys
import pickle
import importlib
import time
import glob
import tensorflow as tf
import os, os.path
import gc
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings("ignore")
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

normal_directory = sys.argv[1]
corrupted_directory = sys.argv[2]
train = (sys.argv[3] == "train")


print("Running on {} Mode".format("training" if train else "testing"))

###This is for testing the LR
#normal_directory = "/home/IPAMNET/pdavarmanesh/Documents/images/HELDOUT_TEST/normal_test/"
#corrupted_directory = "/home/IPAMNET/pdavarmanesh/Documents/images/HELDOUT_TEST/glitched_test/"
####
###This is for training the LR
#normal_directory = "/home/IPAMNET/pdavarmanesh/Documents/images/train_stage_2/normal/"
#corrupted_directory = "/home/IPAMNET/pdavarmanesh/Documents/images/train_stage_2/glitched/"
###

glitches = ["random_patch", "radial_dotted_line", "stuttering", "shape", "line_pixelation",     "shader", "morse_code", "parallel_lines", "dotted_line",
              "triangulation","discoloration", "screen_tearing"] ##random patch, radial must come first.screen tearing must come last

normal_list = []
corrupted_list = []
true_labels = []

print('loading the images...')


normal = np.array([cv2.imread(img) for img in glob.glob(normal_directory + "/*.png")])
n_normal = len(normal)
for i in range(0,len(normal),150): ####1649
    normal_list.append(list(normal[i:i+150])) 
del normal
gc.collect()
true_labels.extend(np.zeros(n_normal))####1649



##for training
if train:
    n_corrupted = 0
    for i, glitch in enumerate(glitches[:-1]):
        with open(corrupted_directory + glitch + '/X.pkl', 'rb') as file:
            print(glitch)
            corrupted_images = pickle.load(file)
            corrupted_list.append(np.array(corrupted_images[:150]))
            n_corrupted += 150
            print(glitch, i+1)
            true_labels = np.append(true_labels, np.ones(150)*(i+1))
    ST = ([cv2.imread(img) for img in glob.glob(corrupted_directory + 'screen_tearing' + "/*.png")])
    true_labels = np.append(true_labels, np.ones(150)*12)
    corrupted_list.append(np.array(ST[:150]))
    n_corrupted += 150
    del ST
    gc.collect()
###

###for testing
if not train:
    corrupted = [cv2.imread(img) for img in glob.glob(corrupted_directory + "/*.png")]
    n_corrupted = len(corrupted)
    for i in range(0,len(corrupted),150): 
        corrupted_list.append(list(corrupted[i:i+150])) 
    del corrupted
    gc.collect()
    true_labels.extend(np.ones(n_corrupted))

###




print('Extracted {} normal emages and {} corrupted images'.format(n_normal, n_corrupted))


print("loaded the images...")
ens_pred = np.zeros( (len(glitches),len(true_labels) ))

gbl = globals()
glitches = glitches[2:] #because random patch, radial use discoloration, dotted respectively so we no longer need the random patch model.

for i, glitch in enumerate(glitches):
    print('testing for ', glitch)
    start = time.time()
    filename =  glitch + "_test." +  glitch + "_test"
    gbl[filename] = importlib.import_module(filename)
    pred = np.array([])
    for images in normal_list:
         pred = np.append(pred, gbl[filename].test(np.array(images)) )
    for images in corrupted_list:
         pred = np.append(pred, gbl[filename].test(np.array(images)) )
         print(pred.shape)
        
    
    ens_pred[i] = pred
    
    print('tested ', glitch, ' which predicted ', np.sum(pred) , 'in {} minutes'.format((time.time()-start)/60))
    true_labels = np.array(true_labels)
    print(true_labels.shape, pred.shape)
    print(confusion_matrix(true_labels, pred))
    
    labels = (true_labels == (i+3)) * 1 #b/c i starts at 0, glitch labels start at 1, we're skipping radial dotted lines
    print(confusion_matrix(labels, pred))
    
## Uncomment this section to produce images of false postives and false negatives
"""
    idx = np.arange(1650)
    print(len(idx), len(pred), len(labels))
    false_neg_idx = idx[(pred[:1650] - labels[:1650]) == -1]
    false_pos_idx = idx[(pred[:1650]  - labels[:1650] ) == 1]
 
  
    print(np.sum(labels))
    print(len(false_neg_idx))
    print(len(false_pos_idx))
  
      
    for idx in false_pos_idx[:50]:
        cv2.imwrite('false_positives/'+ glitch + "_"+ str(idx) +'.jpg', normal_list[idx // 150][idx % 150])

 """ 

np.save("ens_pred.npy", ens_pred)
print("saved the result")  

true_labels = (true_labels != 0) * 1.0
ens_pred = np.transpose(ens_pred)
###for training
if train:
    X_train, X_test, y_train, y_test = train_test_split(ens_pred, true_labels, test_size=0.25, random_state=42)
    start = time.time()
    LR = LogisticRegression(solver = 'lbfgs', multi_class = 'auto', max_iter = 1000)
    LR.fit(X_train, y_train)
    print('LR training time: ', time.time() - start)
    y_pred = LR.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print("Accuracy of the model is: ", accuracy_score(y_test, y_pred))
    pickle_filename = "final_LR.pkl"
    with open(pickle_filename, 'wb') as file:
        pickle.dump(LR, file)
    print("saved the model")

 ###


###for testing
if not train:
    model_f = "final_LR.pkl"
    model=pickle.load(open(model_f,'rb'))
    pred = model.predict(ens_pred)
    print("performance on the heldout test set:")
    print(classification_report(true_labels, pred))
    print(confusion_matrix(true_labels, pred))
    print("Accuracy of the model is: ", accuracy_score(true_labels, pred))

###




