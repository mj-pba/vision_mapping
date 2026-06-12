import  cv2
import numpy as np
import matplotlib.pyplot as plt

def viewbmp(bmpfilename):
    img = cv2.imread(bmpfilename)
    # Convert from BGR to RGB (OpenCV loads images in BGR by default)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    scale_factor = 10 # zoom factor. doesnt seem to do anything for small imgs?
    
    # resize
    width = int(img_rgb.shape[1] * scale_factor)
    height = int(img_rgb.shape[0] * scale_factor)
    dimensions = (width, height)
    zoomed_img = cv2.resize(img_rgb, dimensions, interpolation=cv2.INTER_NEAREST)
    
    plt.title(f'viewing bmp file ...{bmpfilename[round(len(bmpfilename)*0.7):]}')
    plt.imshow(zoomed_img)
    plt.axis('off')  # Hide axis
    plt.show()

def viewarray_asbmp(pixelarray, pixelarrayname='Viewing array converted to bmp'):
    # print(f'width of your array: {len(pixelarray)}')
    width = len(pixelarray)
    height = 1 #1 pixel high only after averaging
    scale_factor = 10 # zoom factor. doesnt seem to do anything for small imgs?
    
    pixelarray = pixelarray.astype(np.uint8) #make sure all in integers
    image_2d = pixelarray.reshape((height, width))
    zoomed_img = cv2.resize(image_2d, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_NEAREST)
    plt.figure(figsize=(10, 2))  # Adjust figsize for better visibility
    plt.imshow(zoomed_img, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')  # Hide axis
    plt.title(pixelarrayname)
    plt.show()

def pull_pixelvals_from_single_img(pixelnumber, segment_half_height, len_firsthalf, len_secondhalf, filepath, x, y, r):
    len_firsthalf = int(pixelnumber/2)
    len_secondhalf = pixelnumber - len_firsthalf
    img = cv2.imread(filepath)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #test effect of grayscale on bmp image
    right_row_upper = int(y-segment_half_height) # centre of circle go up 12 pixels
    right_row_lower = int(y+segment_half_height) # centre of circle go down 12 pixels
    
    right_col_leftmost = int(x+r-len_firsthalf) 
    right_col_rightmost = int(x+r+len_secondhalf) # left to right should equal PIXELNUMBER no. of pixels
    all_intensity_averages = [] 
    for j in range(right_row_upper, right_row_lower,3): # 24/3 = 8 total, to give 8 * num of image files = 256 data samples for all_intensity_averages
        intensity_averages = img_grey[j:j+3,right_col_leftmost:right_col_rightmost]
        intensity_averages = np.mean(intensity_averages, axis=0)
        all_intensity_averages.append(intensity_averages)
    return all_intensity_averages

def expandPixels(intensityarray, expandFactor, numPixels):
    numFiles = len(intensityarray) # no. of files
    rowLength = numPixels  # Number of original pixels wide
    interpolatedpts = rowLength * expandFactor  # Number of interpolated pixels (100 per pixel)
    interpolated_values = np.zeros((numFiles, interpolatedpts)) # store interpolated values here
    
    og_x = np.arange(rowLength)
    print(f'Current number of pixels: {rowLength}\nNumber of interpolated points: {interpolatedpts}\nNumber of data samples: {len(intensityarray)}')

    for i in range(len(intensityarray)):  # number of files
        og_y = intensityarray[i]
        bestfit_x = np.linspace(0, rowLength - 1, interpolatedpts) # (0, 15-1, 100*15)
        bestfiteqn = bestfit(og_x, og_y, 3)
        bestfit_y = bestfiteqn(bestfit_x)  # Generate y values for the interpolated x
        interpolated_values[i] = bestfit_y

    # plt.title(f'Interpolated points for all {len(intensityarray)} files')
    # plt.plot(bestfit_x, bestfit_y, '--', label=f'Interpolated {interpolatedpts} points')
    # plt.xlim(0, interpolatedpts - 1)  # Set x-axis limits from 0 to 1100
    # plt.show()

    print(f'========length of array after running expandPixels========\n og x: {len(og_x)}')
    print(f'bestfit x: {len(bestfit_x)}\n========end of expandPixels========')
    print(f'Interpolated values shape: {interpolated_values.shape}')
    return interpolated_values


# Note: this is used only for test data, where we calculate the middle point of og and reconst graphs. ASSUME peak looks like a parabola
def subpixel_edge_refinement(gradient, peak_index, window_size=3): # note: only can be used for quadratic-style peak. power=2 only!!
    # crop a small window around the peak
    start_index = max(peak_index - window_size, 0)
    end_index = min(peak_index + window_size + 1, len(gradient))
    x = np.arange(start_index, end_index)
    y = gradient[start_index:end_index]
    
    # Fit quadratic polynom to selected window
    coeffs = np.polyfit(x, y, 2)
    
    # vertex of parabola=subpixel peak 
    subpixel_peak = -coeffs[1] / (2 * coeffs[0]) # peak posn = -b/2a , where y = ax^2+bx+c
    return subpixel_peak

# given array of angles, array of radii and degree of polynomial best fit, return the best fit angles
def bestfit(theta, r, poly_deg):
    # Fit a polynomial to the radius data
    coefficients = np.polyfit(theta, r, poly_deg)
    polynomial = np.poly1d(coefficients)
    return polynomial

def resize_image(image, target_width): # currently used to downsize my image
    # Ensure image is 2D
    if len(image.shape) == 1:
        image = image.reshape((1, image.shape[0]))

    # Resize the image using interpolation
    # original_width = image.shape[1]
    resized_image = cv2.resize(image, (target_width, 1), interpolation=cv2.INTER_LINEAR)
    
    return resized_image