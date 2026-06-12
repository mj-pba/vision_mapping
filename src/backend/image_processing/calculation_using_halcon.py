# /src/backend/image_processing/calculation_using_halcon.py
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
import csv
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.patches import Ellipse
from scipy.signal import find_peaks

import halcon as ha
import os

class in_position_calculation:
    def __init__(self,dir):
        self.dir = dir # dummy variable
        self.circle_radius = None
        self.image_center_pixel_x = None
        self.image_center_pixel_y = None
        self.multiplication_factor = None
        self.circle_radius_tolerance = None
        pass

    def read_recipe_csv(self,parameter):
        # get current working directory
        file_path = os.getcwd()  # get the current location
        recipe_file_location = os.path.join(file_path, r'src\recipes\active_recipe.csv')      # Create full file parth
        # print("Active recipe file path : ",recepe_file_location)  
        # check the file is exist or not
        if os.path.exists(recipe_file_location):
            with open(recipe_file_location, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header if present
                for row in reader:
                    if len(row) >= 2 and row[0] == parameter:
                        return row[1]
                    
        else:
            print("File does not exist.")
            return None


    def calculate_center(self,image_path):

        if self.circle_radius == None or self.image_center_pixel_x == None or self.image_center_pixel_y == None or self.circle_radius_tolerance == None:
            self.circle_radius = int(self.read_recipe_csv('circle_radius'))
            self.image_center_pixel_x = int(self.read_recipe_csv('image_center_pixel_x'))
            self.image_center_pixel_y = int(self.read_recipe_csv('image_center_pixel_y'))
            self.circle_radius_tolerance = int(self.read_recipe_csv('circle_radius_tolerance'))


        self.image_path = image_path 
        self.image = ha.read_image(self.image_path)
        self.width,self.height=ha.get_image_size_s(self.image)
        #print(self.width,self.height)

        # define the dot location
        ha.gen_cross_contour_xld ( self.image_center_pixel_y , self.image_center_pixel_x, 30, 0.785398)
 
        MetrologyHandle = ha.create_metrology_model()
        ha.set_metrology_model_image_size (MetrologyHandle, self.width, self.height)
        # MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, Define_Circle_Row , Define_Circle_Column, CircleInitRadius, CircleRadiusTolerance, Thichness_of_the_box, sigma, measure_threshold, ['measure_distance'], [50] )
        MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, self.image_center_pixel_y , self.image_center_pixel_x, self.circle_radius, self.circle_radius_tolerance, 20, 1.5, 1.8, ['measure_distance'], [40] )
        ha.set_metrology_object_param (MetrologyHandle, MetrologyCircleIndices, 'measure_transition', 'uniform')
        ha.apply_metrology_model (self.image, MetrologyHandle)
        CircleParameter = ha.get_metrology_object_result(MetrologyHandle, MetrologyCircleIndices, 'all', 'result_type', 'all_param')
        return CircleParameter

    
    def list_png_files(self):
        # List to store .png file names
        png_files = []

        # Iterate through all files in the folder
        for filename in os.listdir(self.dir):
            if filename.lower().endswith('.png'):
                png_files.append(filename)

        # Sort the list by the numeric part of the filenames
        png_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

        return png_files
    

    def plot_in_posotion_radius(self,circle_params_array,name):
        radius_values = circle_params_array[:, 3]*self.multiplication_factor # radius values in nm

        # Plot the histogram of the radius values
        plt.hist(radius_values, bins=10, density=True, alpha=0.6, color='g')

        # Fit a normal distribution to the data
        mean, std_dev = norm.fit(radius_values)

        # Plot the normal distribution (bell curve) on top of the histogram
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mean, std_dev)

        # Plot the fitted normal distribution curve
        plt.plot(x, p, 'k', linewidth=2)
        title = f"Fit Results: mean = {mean:.2f},  std_dev = {std_dev:.2f}"
        title = "Histrogram of radius calculation with nominal cureve"
        plt.title(title)

        # Labels
        plt.xlabel('Variation in radius calculation in nm')
        plt.ylabel('Probability Density')

        # Show the plot
        plt.show()
        full_file_path = os.path.join(self.dir,name)
        plt.savefig(full_file_path)


    def plot_X_Y_position_in_circle(self,circle_params_array,name):
        X_values = (circle_params_array[:,1] - self.mean_radius[1])*self.multiplication_factor
        Y_values = (circle_params_array[:,2] - self.mean_radius[2])*self.multiplication_factor

        # Create a new figure and axis for the plot
        fig, ax = plt.subplots(figsize=(10, 6))
  
        # Plot X vs Y values
        ax.scatter(X_values, Y_values, marker='.', linestyle='--', color='r', label='X,Y positions')

        # Define the center of the circle (mean X and Y values)
        ellipse_center_x = np.mean(X_values)
        ellipse_center_y = np.mean(Y_values)

        # Define the major and minor axes (2 times the radius values, since width/height is diameter)
        major_axis = self.std_deviation_nm[0]*2  # Example value for the major axis (diameter)
        minor_axis = self.std_deviation_nm[1]*2   # Example value for the minor axis (diameter)

        # Create an ellipse with the specified radii (width = major axis, height = minor axis)
        ellipse1 = Ellipse((ellipse_center_x, ellipse_center_y), width=major_axis, height=minor_axis, angle=0, edgecolor='b', facecolor='none', label='σ bountry for X and Y direction')

        # Define the major and minor axes (2 times the radius values, since width/height is diameter)
        major_axis = self.std_deviation_nm[0]*6  # Example value for the major axis (diameter)
        minor_axis = self.std_deviation_nm[1]*6   # Example value for the minor axis (diameter)
        ellipse2 = Ellipse((ellipse_center_x, ellipse_center_y), width=major_axis, height=minor_axis, angle=0, edgecolor='r', facecolor='none', label='3σ bountry for X and Y direction')

        # Add the ellipse to the plot
        ax.add_patch(ellipse1)
        ax.add_patch(ellipse2)
        
        # Set equal aspect ratio so the circle doesn't look like an ellipse
        ax.set_aspect('equal', 'box')

        # Add title and labels
        plt.title("Dot center X and Y location and standard diviation values")
        plt.xlabel("Dot center X values (nm)")
        plt.ylabel("Dot center Y values (nm)")

        # Add a legend
        plt.legend()
        plt.grid()
        plt.show()
        full_file_path = os.path.join(self.dir,name)
        plt.savefig(full_file_path)


    def plot_in_position(self,circle_params_array,name):

        index = circle_params_array[:, 0]
        
        X_values = (circle_params_array[:,1] - self.mean_radius[1])*self.multiplication_factor
        Y_values = (circle_params_array[:,2] - self.mean_radius[2])*self.multiplication_factor

        # Create a new figure for the plot
        plt.figure(figsize=(10, 6))

        # Plot X values vs. index
        plt.plot(index, X_values, label='X Position', marker='o', linestyle='-', color='b')

        # Plot Y values vs. index
        plt.plot(index, Y_values, label='Y Position', marker='x', linestyle='--', color='r')

        # Add title and labels
        plt.title("Variation of X and Y Position at each image captured")
        plt.xlabel("Image sample index")
        plt.ylabel("X and Y position in nm")

        # Add a legend
        plt.legend()
        plt.show()
        full_file_path = os.path.join(self.dir,name)
        plt.savefig(full_file_path)


    def calculate_and_print(self,x_pos,y_pos,z_pos):

        
        # List all .bmp files in the current directory
        png_files = self.list_png_files()
        #print(png_files)
        circle_params_list = []

        for png_file in png_files:
            full_file_path = os.path.join(self.dir,png_file)
            CircleParameter = self.calculate_center(full_file_path)
            image_number = int(os.path.splitext(png_file)[0]) # Extract the numerical part of the image file name
            #print(png_files,",   " , CircleParameter[0], ", " , CircleParameter[1], ",  " , CircleParameter[2] )
            circle_params_list.append([image_number,CircleParameter[0], CircleParameter[1], CircleParameter[2]])

        circle_params_array = np.array(circle_params_list)          # 
        std_deviation = np.std(circle_params_array, axis=0)         # 
        self.mean_radius = np.mean(circle_params_array, axis=0)     # 
        
        self.multiplication_factor = (0.25/self.mean_radius[3])*1000000     # 0.25  to nm
        self.std_deviation_nm = [std_deviation[1]*self.multiplication_factor, std_deviation[2]*self.multiplication_factor, std_deviation[3]*self.multiplication_factor ]
        self.std_deviation_nm_3_sigma = [self.std_deviation_nm[0]*3, self.std_deviation_nm[1]*3, self.std_deviation_nm[2]*3]
        
        self.plot_in_posotion_radius(circle_params_array,'radius_std.png')
        self.plot_in_position(circle_params_array, 'x_and_y_position.png')
        self.plot_X_Y_position_in_circle(circle_params_array, 'x_and_y_position_circle.png')

        circle_params_list.append([0, 0, 0, 0])
        circle_params_list.append([40, 0, 0, self.mean_radius[3]])                                                                              # mean 'mu'
        circle_params_list.append([1, 0, 0, self.multiplication_factor])                                                                        # single pixel size in nm
        circle_params_list.append([200, self.std_deviation_nm[0], self.std_deviation_nm[1], self.std_deviation_nm[2]])                          # standard deviation sigma
        circle_params_list.append([600, self.std_deviation_nm_3_sigma[0], self.std_deviation_nm_3_sigma[1], self.std_deviation_nm_3_sigma[2]])  # 3 sigma
        circle_params_list.append([0, x_pos, y_pos, z_pos])

        circle_params_array = np.array(circle_params_list)
        file_location_and_name = os.path.join(self.dir,'circle_parameters.csv')
        np.savetxt(file_location_and_name, circle_params_array, delimiter=',', header='Image_index,Row(Y),Column(X),Radius', comments='', fmt='%f')

        return self.std_deviation_nm_3_sigma


class position_error_claculation:
    def __init__(self):
        #self.image_radius = 571 # in pixel 
        self.circle_radius = None
        self.image_center_pixel_x = None
        self.image_center_pixel_y = None
        self.circle_radius_tolerance = None

        
        pass


    def read_recipe_csv(self,parameter):
        # get current working directory
        file_path = os.getcwd()  # get the current location
        recipe_file_location = os.path.join(file_path, r'src\recipes\active_recipe.csv')      # Create full file parth
        # print("Active recipe file path : ",recepe_file_location)  
        # check the file is exist or not
        if os.path.exists(recipe_file_location):
            with open(recipe_file_location, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header if present
                for row in reader:
                    if len(row) >= 2 and row[0] == parameter:
                        return row[1]
                    
        else:
            print("File does not exist.")
            return None



    def calculate_center(self,image_path):

        # getting the image radius and center pixel location from the recipe file
        if self.circle_radius == None or self.image_center_pixel_x == None or self.image_center_pixel_y == None or self.circle_radius_tolerance == None:
            self.circle_radius = int(self.read_recipe_csv('circle_radius'))
            self.image_center_pixel_x = int(self.read_recipe_csv('image_center_pixel_x'))
            self.image_center_pixel_y = int(self.read_recipe_csv('image_center_pixel_y'))
            self.circle_radius_tolerance = int(self.read_recipe_csv('circle_radius_tolerance'))


        self.image_path = image_path 
        #self.pre_processing()

        # halcon xld based image center calculation
        self.image = ha.read_image(self.image_path)
        
        self.width,self.height=ha.get_image_size_s(self.image)
        #print(self.width,self.height)

        # define the dot location
        ha.gen_cross_contour_xld ( self.image_center_pixel_y, self.image_center_pixel_x, 30, 0.785398)
        
        MetrologyHandle = ha.create_metrology_model()
        ha.set_metrology_model_image_size (MetrologyHandle, self.width, self.height)
        # MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, Define_Circle_Row , Define_Circle_Column, CircleInitRadius, CircleRadiusTolerance, Thichness_of_the_box, sigma, measure_threshold, ['measure_distance'], [50] )
        MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, self.image_center_pixel_y , self.image_center_pixel_x, self.circle_radius, self.circle_radius_tolerance, 20, 1.5, 1.8, ['measure_distance'], [40] )
        ha.set_metrology_object_param (MetrologyHandle, MetrologyCircleIndices, 'measure_transition', 'uniform')
        ha.apply_metrology_model (self.image, MetrologyHandle)
        CircleParameter = ha.get_metrology_object_result(MetrologyHandle, MetrologyCircleIndices, 'all', 'result_type', 'all_param')
        print(CircleParameter[0], CircleParameter[1], CircleParameter[2])
        return CircleParameter



