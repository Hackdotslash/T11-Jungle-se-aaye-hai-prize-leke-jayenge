import cv2
import dlib
import numpy as np

def shape_to_np(shape, dtype="int"):
    """
    input : shape : a collection of 68 facial landmarks.
    output : a list of (x,y) coordinates of all those 68 points.
    """
    
    # coords will store the list of (x,y)-coordinates 
    coords = np.zeros((68, 2), dtype=dtype)
    #shape is a set of 68 prelearned points, categorising various shapes of face.
    #(x,y) coordinates of each of the 68 data points is to be stored in coords.
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    
    return coords

def eye_on_mask(mask, side):
    #list to store landmark points of the given side of eye.
    points = [shape[i] for i in side]
    #converting it to a numpy array
    points = np.array(points, dtype=np.int32)
    #since the initial mask that we obtain is all black, hence masking is done in white
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask

def contouring(thresh, mid, img, right=False):
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    try:
        cnt = max(cnts, key = cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        if right:
            cx += mid
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
    except:
        pass

# To localize the face from the image
detector = dlib.get_frontal_face_detector()
#predictor is a shape predictor object, using a pre-trained dataset of 68_facial_landmarks
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#left for LeftEye and right for RightEye
left = [36, 37, 38, 39, 40, 41]
right = [42, 43, 44, 45, 46, 47]

#capturing and reading the video frame
cap = cv2.VideoCapture(0)
ret, img = cap.read()
thresh = img.copy()

cv2.namedWindow('image')
kernel = np.ones((9, 9), np.uint8)

#to still the trackbar window
def DoNone(x):
    pass

cv2.createTrackbar('threshold', 'image', 0, 255, DoNone)

while(True):
    #Read image from the steam
    ret, img = cap.read()
    #converting image into a grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #rects stores the faces(probable faces from the image).
    rects = detector(gray, 1)
    for rect in rects:

        #get the coordinates of facial landmarks into a numpy array 
        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        
        #masking the eye out of the frame size image - img.shape[:2] yields the dimensions of the frame
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        #initially the frame is black, masking fills the eye part with white. and leaves rest of the frame as it is.
        #applying the mask for left eye
        mask = eye_on_mask(mask, left)
        #applying the mask for right eye
        mask = eye_on_mask(mask, right)
        
        #expand the white area, using dilate
        mask = cv2.dilate(mask, kernel, 5)
        #bitwise and to segment out the eyeball out of the eye.
        eyes = cv2.bitwise_and(img, img, mask=mask)
        mask = (eyes == [0, 0, 0]).all(axis=2)
        eyes[mask] = [255, 255, 255]
        mid = (shape[42][0] + shape[39][0]) // 2
        eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
        threshold = cv2.getTrackbarPos('threshold', 'image')
        _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, None, iterations=2) #1
        thresh = cv2.dilate(thresh, None, iterations=4) #2
        thresh = cv2.medianBlur(thresh, 3) #3
        thresh = cv2.bitwise_not(thresh)
        contouring(thresh[:, 0:mid], mid, img)
        contouring(thresh[:, mid:], mid, img, True)
        
    cv2.imshow('eyes', img)
    cv2.imshow("image", thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()