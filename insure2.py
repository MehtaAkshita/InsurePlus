# -*- coding: utf-8 -*-
"""Insure++.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iy-lN3o7VXh1wefku0D59at4tnCYujuV
"""

"""Import Systrem Dependecies"""
from keras import backend as K

import numpy as np 
import os,sys
from PIL import Image
import matplotlib.pyplot as plot
from optparse import OptionParser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import models
from keras import layers
from keras import optimizers


"""Utility Functions"""

def calclaim (cost,dmg,loc,sev):
  if(dmg==0 and sev==0):
    return 0.25
  cnt = 1
  if(loc == 1 ):
    cnt *= 2
  else:
    cnt *= 3

  if (sev == 0):
    cnt *= 0.5
  elif(sev==1):
    cnt *= 3
  else:
    cnt *= 7

  if (cost==0):
    cnt *= 1
  elif(cost==1):
    cnt *= 1.5
  else:
    cnt *= 4
  
  return cnt

def grayscale(picture):
    res= Image.new(picture.mode, picture.size)
    width, height = picture.size

    for i in range(0, width):
        for j in range(0, height):
            pixel=picture.getpixel((i,j))
            avg=int((pixel[0]+pixel[1]+pixel[2])/3)
            res.putpixel((i,j),(avg,avg,avg))
    #res.show()
    return res

def normalize(picture):
    width, height = picture.size
    normalized_array = []
    for j in range(0, height):
	    for i in range(0, width):
		    pixel = picture.getpixel((i,j))
		    normalized_array.append( pixel[0] / 255.0 )
    return np.array(normalized_array)

"""Deep Learning Utility Functions"""

def loadIsCar():
  model = load_model('C:/Users/Dell/Desktop/InsurePlus - Copy/car_detection_keras_CNN_model.h5')
  model._make_predict_function()
  return model

def isCar(imgpath,model):
  row,column = 100,100
  img = Image.open(imgpath)

  img = img.resize((row,column),Image.ANTIALIAS)
  gray_image = grayscale(img)

  X_test = normalize(gray_image)
  X_test = X_test.reshape(1, row, column, 1)  # (1, row, column) 3D input for CNN 

  classes = model.predict(X_test)
  maxVal = classes[0].max()
  indexVal = np.where(classes[0]==maxVal) # result is an array
  
  if (indexVal[0] == 0):
      return 1
  else: 
      return 0

def loadIsDamaged():
  image_size = 150
  #Load the VGG model
  vgg_conv = VGG16(weights = "C:/Users/Dell/Desktop/InsurePlus - Copy/vggwt.h5",include_top=False, input_shape=(image_size, image_size, 3))

  # Freeze the layers except the last 4 layers
  for layer in vgg_conv.layers[:-4]:
      layer.trainable = False

  # Create the model
  model = models.Sequential()
  
  # Add the vgg convolutional base model
  model.add(vgg_conv)
  
  # Add new layers
  model.add(layers.Flatten())
  model.add(layers.Dense(1024, activation='relu'))
  model.add(layers.Dropout(0.5))
  model.add(layers.Dense(2, activation='softmax'))
  
  # Show a summary of the model. Check the number of trainable parameters
  #model.summary()

  model.load_weights('dmgornot_weights.h5')
  return model

def isDamaged(imgpath,model):
  image_size = 150 
  img = Image.open(imgpath).resize((image_size,image_size))
  img_arr = np.expand_dims(img_to_array(img), axis=0)

  image = preprocess_input(img_arr)
  prediction = model.predict(image)

  maxval = prediction.max()
  if(maxval == prediction[0][0]):
    return 1
  else:
    return 0

def loadDmgLoc():
  image_size = 150
  #Load the VGG model
  vgg_conv = VGG16(weights = "C:/Users/Dell/Desktop/InsurePlus - Copy/vggwt.h5",include_top=False, input_shape=(image_size, image_size, 3))

  # Freeze the layers except the last 4 layers
  for layer in vgg_conv.layers[:-4]:
      layer.trainable = False

  # Create the model
  model = models.Sequential()
  
  # Add the vgg convolutional base model
  model.add(vgg_conv)
  
  # Add new layers
  model.add(layers.Flatten())
  model.add(layers.Dense(1024, activation='relu'))
  model.add(layers.Dropout(0.5))
  model.add(layers.Dense(3, activation='softmax'))
  
  # Show a summary of the model. Check the number of trainable parameters
  #model.summary()

  model.load_weights('C:/Users/Dell/Desktop/InsurePlus - Copy/dmgloc_weights.h5')
  return model

def dmgLoc(imgpath,model):
  image_size = 150
  img = Image.open(imgpath).resize((image_size,image_size))
  img_arr = np.expand_dims(img_to_array(img), axis=0)

  image = preprocess_input(img_arr)
  prediction = model.predict(image)

  maxval = prediction.max()
  if(maxval == prediction[0][0]):
    return 0
  elif(maxval == prediction[0][1]):
    return 1
  else:
    return 2

def loadDmgSev():
  image_size = 150
  #Load the VGG model
  vgg_conv = VGG16(weights = "C:/Users/Dell/Desktop/InsurePlus - Copy/vggwt.h5",include_top=False, input_shape=(image_size, image_size, 3))

  # Freeze the layers except the last 4 layers
  for layer in vgg_conv.layers[:-4]:
      layer.trainable = False

  # Create the model
  model = models.Sequential()
  
  # Add the vgg convolutional base model
  model.add(vgg_conv)
  
  # Add new layers
  model.add(layers.Flatten())
  model.add(layers.Dense(1024, activation='relu'))
  model.add(layers.Dropout(0.5))
  model.add(layers.Dense(3, activation='softmax'))
  
  # Show a summary of the model. Check the number of trainable parameters
  #model.summary()

  model.load_weights('C:/Users/Dell/Desktop/InsurePlus - Copy/dmgsev_weights.h5')
  return model

def dmgSev(imgpath,model):
  image_size = 150
  img = Image.open(imgpath).resize((image_size,image_size))
  img_arr = np.expand_dims(img_to_array(img), axis=0)

  image = preprocess_input(img_arr)
  prediction = model.predict(image)

  maxval = prediction.max()
  if(maxval == prediction[0][0]):
    return 0
  elif(maxval == prediction[0][1]):
    return 1
  else:
    return 2

"""Loading Various models"""
def loadImg(path):
  K.clear_session()
  global model0
  global model1
  global model2
  global model3

  path = "C:/Users/Dell/Desktop/InsurePlus - Copy/static/"+path
  model0 = loadIsCar()
  model0._make_predict_function()
  model1 = loadIsDamaged()
  model1._make_predict_function()
  model2 = loadDmgLoc ()
  model2._make_predict_function()
  model3 = loadDmgSev ()
  model3._make_predict_function()

  print("All models loaded sucessfully")

  #path = 'car.jpg'
def imgup(path): 
  K.clear_session()

  path = "C:/Users/Dell/Desktop/InsurePlus - Copy/static/"+path
  image = mpimg.imread(path)
  #plt.imshow(image)
  #plt.show()
  cost = 1 # 0 cheap; 1 moderate; 2 costly
  car = (isCar(path,model0))
  dmg = (isDamaged(path,model1))
  loc = (dmgLoc(path,model2))
  sev = (dmgSev(path,model3))
  a=  "is car:"+str(car)+"  "+"cost:"+str(cost)+"  "+"is damaged:"+str(dmg)+"  "+"damage loc:"+str(loc)+"  "+"sev:"+str(sev)
  est = calclaim(cost,dmg,loc,sev)*1000
  b =  str("₹"+str(est))
  # b =  str("Estimated cost to repair your car is ₹"+str(est))

  K.clear_session()
  return b

##loadImg('car.jpg')
