import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.patches import Ellipse

import halcon as ha
import os


class image_shapness:
    def __init__(self):
        
        pass

#    # does not in use 
#    def estimate_sharpness_sobel(self,image_path):
#        """
#        Estimates image sharpness using the Sobel edge amplitude method.
#
#        Args:
#            image_path (str): Path to the image file.
#
#        Returns:
#            float: Estimated sharpness value (mean Sobel amplitude).
#                   Higher value indicates sharper image.
#        """
#        try:
#            # 1. Read the image using Halcon
#            self.image_path = image_path 
#            self.image = ha.read_image(self.image_path)
#            self.width,self.height=ha.get_image_size_s(self.image)
#            #print(self.width,self.height)
#
#            # 2. Apply the Sobel operator to calculate edge amplitude
#            #    'sum_abs' is a common type, and 3 is a typical filter size.
#            sobel_amp_image_sum_abs = ha.sobel_amp(self.image, 'sum_sqrt', 5)
#
#            # 3. Retrieve the pixel values from the Sobel amplitude image
#            sobel_amp_values = ha.get_image_pointer1(sobel_amp_image_sum_abs)
#            pointer, type, width, height = ha.get_image_pointer1(sobel_amp_image_sum_abs)
#            print(pointer, type, width, height)
#            #sobel_amp_array = np.frombuffer(pointer, dtype=np.uint8).reshape(height, width)
#
#            # 4. Calculate the mean value of the Sobel amplitude image
#            #mean_amplitude = np.mean(sobel_amp_array)
#
#
#            #return mean_amplitude
#            return None
#
#        except ha.HalconError as e:
#            print(f"Halcon Error: {e}")
#            return None
#        except FileNotFoundError:
#            print(f"Error: Image file not found at {image_path}")
#            return None
#
#
#    def detect_focus_laplacian(self,image_path, threshold):
#        # Load the image in grayscale
#        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#        
#        # 1. Read the image using opencv
#        if image is None:
#            print("Error: Could not read image.")
#            return None, "Error"
#        
#        # Apply the Laplacian operator
#        laplacian = cv2.Laplacian(image, cv2.CV_64F)
#
#        # Compute the variance (measure of sharpness)
#        variance = laplacian.var()
#
#        # Determine focus status
#        status = "In Focus" if variance > threshold else "Blurry"
#        print(f"Focus Status: {status}\nLaplacian Variance: {variance:.2f}")
#
#        # Display the image with focus status
##        plt.figure(figsize=(6, 6))
##        plt.imshow(image, cmap='gray')
##        plt.title(f"Focus Status: {status}\nLaplacian Variance: {variance:.2f}")
##        plt.axis("off")
##        plt.show()
#
#        #return variance, status
#        return 1
#
    def detect_sharpness_sobel(self,image_path, threshold):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Error: Could not read image.")
            return None, "Error"

        # Compute Sobel gradients in X and Y direction
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

        # Compute magnitude of gradient
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        # Compute variance of Sobel response
        variance = sobel_magnitude.var()

        # Determine focus status
        status = "In Focus" if variance > threshold else "Blurry"

        # Show results
        plt.figure(figsize=(6,6))
        plt.imshow(sobel_magnitude, cmap='gray')
        plt.title(f"Sharpness: {variance:.2f} ({status})")
        plt.axis("off")
        plt.show()

        return variance, status


# ==========
# Test code
# ==========
#image_path_1 = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_03_18_11_17_33\auto_focus.png"
#image_path_2 = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_03_18_11_28_28\auto_focus.png"
#image_path_3 = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_03_18_11_36_47\auto_focus.png"
#
#image_shapness_halcon_obj = image_shapness()
#CircleParameter = image_shapness_halcon_obj.estimate_sharpness_sobel(image_path)
#threshold = 100
#mean_amplitude = image_shapness_halcon_obj.detect_focus_laplacian(image_path_3,threshold)
#mean_amplitude = image_shapness_halcon_obj.detect_sharpness_sobel(image_path_3,threshold)