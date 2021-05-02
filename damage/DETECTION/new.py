# import the necessary packages====================================================================
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
import numpy as np
import colorsys
import argparse
import imutils
import random
import cv2
import os
import json
import sys
import time
from PIL import Image
from makeJSON import jsonmaker
#//////////////////////////////////////////////////////////////////////////////////////////////////
IMAGES = []
CROP = []
CROP_BLACK = []
# pwd = os.getcwd() + "\\" #+ "\\damage\\DETECTION\\"
pwd = os.getcwd() + "\\damage\\DETECTION\\"

#print(os.getcwd())

# extracting car===================================================================================


# load the COCO class labels our Mask R-CNN was trained on
labelsPath = pwd + "mask-rcnn-coco\\object_detection_classes_coco.txt"
LABELS = open(labelsPath).read().strip().split("\n")


# derive the paths to the Mask R-CNN weights and model configuration
weightsPath = pwd + "mask-rcnn-coco/frozen_inference_graph.pb"
configPath = pwd + "mask-rcnn-coco/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"

 
# load our Mask R-CNN trained on the COCO dataset (90 classes) from disk
print("[INFO] loading Mask R-CNN from disk...")
net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)


# import images
claim = sys.argv[1]
side = ["front", "left", "back", "right"]
for i in range(4):
        image = cv2.imread("static/IMAGES/" + side[i] + str(claim) + ".jpg")
        # image = cv2.imread(pwd + "\\IMAGES\\" + side[i] + str(claim) + ".jpg")
        image = cv2.resize(image, (720,480))
        IMAGES.append(image)

    
for image in IMAGES:
        (H, W) = image.shape[:2]
        # construct a blob from the input image and then perform a forward
        # pass of the Mask R-CNN, giving us (1) the bounding box  coordinates
        # of the objects in the image along with (2) the pixel-wise segmentation
        # for each specific object
        blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
        net.setInput(blob)
        (boxes, masks) = net.forward(["detection_out_final", "detection_masks"])
 
        # setting variables
        max_area = 0
        SX, SY, EX, EY = 0, 0, 0, 0
        MboxW, MboxH, CID, I = 0, 0, 0, 0

        # loop over the number of detected objects
        for i in range(0, boxes.shape[2]):
                # extract the class ID of the detection
                classID = int(boxes[0, 0, i, 1])
    
                # filter out other objects than car
                if(LABELS[classID] == "car"):
                        # filter out weak predictions
                        confidence = boxes[0, 0, i, 2]
                        if confidence > 0.5:
                        
                                # scale the bounding box coordinates back relative to the
                                # size of the image and then compute the width and the height
                                # of the bounding box
                                box = boxes[0, 0, i, 3:7] * np.array([W, H, W, H])
                                (startX, startY, endX, endY) = box.astype("int")
                                boxW = endX - startX
                                boxH = endY - startY
            
                                # extract max area box and mask
                                area = boxW * boxH
                                if area > max_area:
                                        max_area = area
                                        SX, SY, EX, EY = startX, startY, endX, endY
                                        MboxW, MboxH, CID, I = boxW, boxH, classID, I

        mymask = masks[I, CID]
        mymask = cv2.resize(mymask, (MboxW, MboxH))
        mymask = (mymask > 0.3)


        crop = cv2.resize(image[SY:EY, SX:EX], (720,480))
        CROP.append(crop)
        roi = image[SY:EY, SX:EX][mymask]
        black = image
        cv2.rectangle(black,(0,0),(W,H),(0,0,0),-1)
        black[SY:EY, SX:EX][mymask] = roi
        black_crop = cv2.resize(black[SY:EY, SX:EX], (720,480))
        CROP_BLACK.append(black_crop)
#//////////////////////////////////////////////////////////////////////////////////////////////////



# configuration====================================================================================
class SimpleConfig(Config):
        # give the configuration a recognizable name
        NAME = "coco_inference"

        # set the number of GPUs to use along with the number of images per GPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

        # number of classes (we would normally add +1 for the background but the 
        # background class is *already* included in the class names)
        NUM_CLASSES = 2

# initialize the inference configuration
config = SimpleConfig()
#//////////////////////////////////////////////////////////////////////////////////////////////////



# initialize the Mask R-CNN model for inference and then load the weights==========================
model_names = ["SCRATCH", "DENT", "GLASS", "CRACK", "OUT"]
models = []
for i in range (0, len(model_names)):
        print("[INFO] loading Mask R-CNN " + model_names[i] + " model...")
        c_model = modellib.MaskRCNN(mode="inference", config=config, model_dir=os.getcwd())
        c_model.load_weights(pwd + "DAMAGE/" + model_names[i] + ".h5", by_name=True)
        models.append(c_model)
#//////////////////////////////////////////////////////////////////////////////////////////////////



# detecting damage=================================================================================
c = 0
for image in CROP_BLACK:

        output = CROP[c]

        # load the input image, convert it from BGR to RGB channel ordering============================
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        #//////////////////////////////////////////////////////////////////////////////////////////////



        # perform a forward pass of the network to obtain the results==================================
        r = []
        for i in range (0, len(models)):
                print("[INFO] making " + model_names[i] + " predictions with Mask R-CNN...")
                c_r = models[i].detect([image], verbose=1)[0]
                r.append(c_r)
        #//////////////////////////////////////////////////////////////////////////////////////////////



        # generate random colors=======================================================================
        def getcolor():
                return list([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        #//////////////////////////////////////////////////////////////////////////////////////////////



        # printing masks===============================================================================
        '''for j in range (0, len(r)):
                # loop over of the detected object's bounding boxes and masks
                for i in range(0, r[j]["rois"].shape[0]):

                        score = r[j]["scores"][i]
                
                        # visualize the pixel-wise mask of the object
                        if score > 0.9:
                                color = getcolor()
                                mask = r[j]["masks"][:, :, i]
                                output = visualize.apply_mask(output, mask, color, alpha=0.5)'''
        #//////////////////////////////////////////////////////////////////////////////////////////////



        # convert it from RGB to BGR channel ordering
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        #//////////////////////////////////////////////////////////////////////////////////////////////

        # printing boxes===============================================================================
        for j in range (0, len(r)):
                # loop over the predicted scores and class labels
                for i in range(0, len(r[j]["scores"])):
                
                        score = r[j]["scores"][i]
                        
                        if score > 0.9:
                                color = getcolor()
                                (startY, startX, endY, endX) = r[j]["rois"][i]
                                label = model_names[j]
                                # draw the bounding box, class label, and score of the object
                                cv2.rectangle(output, (startX, startY), (endX, endY), color, 2)
                                text = "{}: {:.3f}".format(label, score)
                                y = startY - 10 if startY - 10 > 10 else startY + 10
                                cv2.putText(output, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                                center = [int(abs(endX-startX)/2), int(abs(endY-startY)/2)]
                                shape =  [image.shape[1], image.shape[0]]
                                jsonmaker(c, center, shape, label, score, claim)
        #//////////////////////////////////////////////////////////////////////////////////////////////



        # show the output image========================================================================
        cv2.imwrite("static/OUTPUTS/" + "output_" + side[c] + str(claim) + ".jpg", output)
        # cv2.imwrite(pwd + "\\OUTPUTS\\output_" +  side[c] + str(claim) + ".jpg", output)
        c += 1
        #//////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
cv2.waitKey()



# if no damage detected=============================================================================
address = "static/JSON/data_" + str(claim) + ".txt"
file = open(address,'a')
if os.stat(address).st_size == 0:
        data = {}
        data["damage"] = "0"
        data["details"] = []
        data["details"].append({
                "front":[],
                "left":[],
                "back":[],
                "right":[]
        })
        json.dump(data,file)
file.close()
#///////////////////////////////////////////////////////////////////////////////////////////////////