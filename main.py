
from time import time

import numpy as np
import serial
import win32con
import win32gui
import win32ui
from PIL import Image

# open a serial connection
s = serial.Open('COM3', 188239)

import flash_detector as fd

model = fd.loadModel('./model/keras_model.h5')

def windowCapture():
  w = 1920 # set this
  h = 1080# set this
  hwnd = None
  wDC = win32gui.GetWindowDC(hwnd)
  dcObj=win32ui.CreateDCFromHandle(wDC)
  cDC=dcObj.CreateCompatibleDC()
  dataBitMap = win32ui.CreateBitmap()
  dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
  cDC.SelectObject(dataBitMap)
  cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

  signedIntsArray = dataBitMap.GetBitmapBits(True)
  img = np.fromstring(signedIntsArray, dtype='uint8')
  img.shape = (h, w, 4)

  # Free Resources
  dcObj.DeleteDC()
  cDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, wDC)
  win32gui.DeleteObject(dataBitMap.GetHandle())

  return img

loopTime = time()
while True:
  ss = windowCapture()
  ssWithoutAlpha = np.array(ss)[:,:,:3]
  ssToPILImg = Image.fromarray(ssWithoutAlpha)
  reshapedImg = fd.reshapeImage(ssToPILImg)
  prediction = fd.predict(model, reshapedImg)
  if not prediction:
    serial.write(b"on\n")
  else:
    serial.write(b"off\n")
