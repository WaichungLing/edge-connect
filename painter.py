import cv2
import numpy as np
import sys


def draw(event, x, y, flags, param):
    global painting
    t = cv2.getTrackbarPos('Thickness', 'Painter')
    mode = cv2.getTrackbarPos('Sketch', 'Painter')
    # Left button down, start to draw
    if event == cv2.EVENT_LBUTTONDOWN:
        painting = True
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if painting:
            if mode == 0:       # mode 0 is erase
                cv2.circle(img, (x, y), t*25, (255, 255, 255), -1)
                cv2.circle(mask, (x, y), t*25, 255, -1)
            else:               # mode 1 is sketch
                cv2.circle(img, (x, y), 5, (0, 0, 0), -1)
                cv2.circle(sketch, (x, y), 5, 0, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        painting = False


painting = False
filename = sys.argv[1]
print(filename)
img = cv2.imread(filename)
original = img.copy()

height, width, _ = img.shape
mask = np.zeros([height, width], dtype=np.uint8)
sketch = np.ones([height, width], dtype=np.uint8)*255

cv2.namedWindow('Painter')
cv2.createTrackbar('Sketch', 'Painter', 0, 1, lambda x: x)
cv2.createTrackbar('Thickness', 'Painter', 1, 4, lambda x: x)

cv2.setMouseCallback('Painter', draw)

while True:
    cv2.imshow('Painter', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('Sketch', sketch)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('c'):
        img = original.copy()
        mask = np.zeros([height, width], dtype=np.uint8)
        sketch = np.ones([height, width], dtype=np.uint8)*255
    elif k == ord('q'):
        break

cv2.destroyAllWindows()
filename = filename[:filename.find(".")]
Mask_path = "Mask/"+filename+".png"
print(Mask_path)
Sketch_path = "Sketch/"+filename+".png"
print(Sketch_path)
cv2.imwrite(Mask_path, mask)
cv2.imwrite(Sketch_path, sketch)
print("Successfully save your sketch!")
