import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps


def loadModel(filePath):
  return load_model(filePath)

def reshapeImage(image):
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.ANTIALIAS)
  imageArray = np.asarray(image)
  normalizedImageArray = (imageArray.astype(np.float32)/127.0) - 1
  data = np.ndarray(shape=(1, 224, 224, 3))
  data[0] = normalizedImageArray
  return data

def predict(model, data):
  prediction = model.predict(data)
  flash = prediction[0][0]
  noFlash = prediction[0][1]
  if flash >= noFlash:
    return 0
  return 1
