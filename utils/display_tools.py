import cv2






# display image 
def display_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0) 
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()