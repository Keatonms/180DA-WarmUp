# Video Capture with OpenCV
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY
    # start of thresholding code
    import cv2 as cv
    import numpy as np
    from matplotlib import pyplot as plt
    #img = cv.imread('filename.png',0)
    img = frame
    ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
    ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
    ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
    ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
    ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(1):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    #plt.pause(.001)
    plt.show()
    # plt.draw()


# end thresholding code


    # Display the resulting frame
    #cv2.imshow(frame,gray)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
