# # to check if cam is working or not.

# import cv2

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print(" Failed to open webcam.")
# else:
#     print("Webcam opened successfully. Press 'q' to quit.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to read frame.")
#             break

#         cv2.imshow("Test Camera", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# cap.release()
# cv2.destroyAllWindows()



# For check pic properties

import cv2

img = cv2.imread('media/face_images/abc.jpg')
print(img.shape)  # Should return (H, W, 3) for RGB
