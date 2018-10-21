import cv2 
import numpy as np 
import sys

def main():
    file_name = sys.argv[1]
    img = cv2.imread(file_name)[:,:,::-1]
    img_size = img.shape[:2]
    r_sum = np.sum(img[:,:,0])
    g_sum = np.sum(img[:,:,1])
    b_sum = np.sum(img[:,:,2])

    overall_pixel = r_sum + g_sum + b_sum
    r_percent = round(r_sum * 100 / overall_pixel, 3)
    g_percent = round(g_sum * 100 / overall_pixel, 3)
    b_percent = round(b_sum * 100 / overall_pixel, 3)

    print('照片大小: {}x{}'.format(img_size[0], img_size[1]))
    print('r/g/b : {}% /{}% /{}%'.format(r_percent, g_percent, b_percent))
    input('按任意鍵繼續....')

if __name__ == '__main__':
    main()

