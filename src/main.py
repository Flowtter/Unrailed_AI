import cv2
import numpy as np
import time
import sys

# start = time.time()

image = cv2.imread("../data/" + sys.argv[1])
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
template = cv2.imread("../template.png", cv2.IMREAD_GRAYSCALE)


w, h = template.shape[::-1]

# Apply template matching to image
result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
location = np.where(result >= 0.9)     # trust me that threshold is working 89
for point in zip(*location[::-1]):
    cv2.rectangle(image, (point[0] - 10, point[1] - 10), (point[0] + w + 10, point[1] + h + 10), (255, 0, 255), 2)

cv2.imshow("image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
# print(time.time() - start)
