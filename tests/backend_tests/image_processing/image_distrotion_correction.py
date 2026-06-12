# reference: https://learnopencv.com/camera-calibration-using-opencv/
# reference: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
import cv2
# assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob



def learn_distortion(image_files_training):
    # checkerboard row/col number
    CHECKERBOARD = (3,4)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # Termination criteria for cornerSubPix, generally fine.

    # vector to store vectors of calculated 3D points for each checkerboard image
    objpoints = []
    # vector to store vectors of measured 2D points for each checkerboard image
    imgpoints = []

    # define world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    prev_img_shape = None # Not used in the code. Can be removed.

    # extract path of individual image stored in a given directory
    # images = glob.glob('./images/*.jpg')
    for fname in image_files_training: # potential issue 1: image_files_training could be empty or contain paths to non-image files.
        img = cv2.imread(fname) # potential issue 2: if fname is invalid path, cv2.imread will return None. No check for None is done.
        if img is None: # Added check if image is read successfully
            print(f"Error: Could not read image from {fname}. Skipping this file.")
            continue # Skip to the next file if image loading fails.

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        min = np.min(gray)
        max = np.max(gray)

        # compute contrast (Michelson contrast, i.e. visibility)
        contrast = (max-min)/(max+min)
        print(f'min: {min}, max: {max}, contrast: {contrast}')
        # Find chess board corners
        # if desired number of corners are found in image then ret = true
        ret, corners = cv2.findChessboardCornersSB(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE) # potential issue 3: if checkerboard is not found, ret will be False and corners will be None.
        # ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE) # potential issue 3: if checkerboard is not found, ret will be False and corners will be None.
        print(f'ret: {ret}\ncorners: {corners}')
        """
        If desired number of corner are detected,
        refine pixel coordinates and display
        them on images of checkerboard
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria) # (11,11)= window size. no. of pixels ard the corner taken for subpixeling # potential issue 4: corners might be None if findChessboardCorners failed, though it is checked by 'ret'.
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            print(f'found for {fname}')
        else:
            print(f'cant find for {fname}')

    cv2.destroyAllWindows() # destroyAllWindows might not be necessary here, especially if hanging occurs before this point.

    if not imgpoints: # potential issue 5: if no checkerboard is found in any image, imgpoints will be empty. calibrateCamera will likely fail or hang if objpoints and imgpoints are empty.
        print("Error: No checkerboard corners found in any image. Calibration cannot proceed.")
        return False, None, None, None, None # Return None values to indicate calibration failure.


    h,w = img.shape[:2] # potential issue 6: 'img' might not be defined if no image is successfully read or processed in the loop. It is safer to use gray.shape if gray is guaranteed to be processed for at least one image. However, if no chessboard is found, 'img' from the last processed image will be used, which might not be ideal if no image was processed successfully. It's better to get shape from first successfully read image or handle the case where no image is processed. Let's use gray.shape since gray is created inside the loop.

    """
    Perform camera calibration by
    passing value of known 3D points (objpoints)
    and corresponding pixel coordinates of
    detected corners (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None) # potential issue 7: if objpoints or imgpoints are empty or have incorrect data, calibrateCamera might hang or fail. This is the most likely location for a hang if checkerboard detection fails or if input images are not suitable for calibration.
    print(f"Camera matrix : {mtx}\ndist : {dist}\nrvecs : {rvecs}\ntvecs : {tvecs}")

    return ret, mtx, dist, rvecs, tvecs







# use following line to crop dst to avoid seeing the ugly remapping of noncheckered area, but it caused a lot of issues so i left it out
# if u use it, replace the second mtx with newcameramtx in cv2.undistort, and uncomment the 2 lines before cv2.imwrite
# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
# print(f'og cameramtx: {mtx}\nnewcameramtx: {newcameramtx}\nroi: {roi}')
def undistort(imagefiles, mtx, dist, mtx0):

    base_path = os.path.dirname(imagefiles)
    print(f'base_path: {base_path}')
    # look for other .bmp file in the same directory
    imagefiles = [f for f in glob.glob(os.path.join(base_path, '*.png'))]
    #print(f'image_files_training_glob: {image_files_training_glob}')


    for fname in imagefiles:
        try:
            # Extract the file name without the directory and extension
            file_name = os.path.splitext(os.path.basename(fname))[0]
            basefolder = os.path.dirname(fname)

            print(file_name)

            # read image
            img = cv2.imread(fname)
            h, w = img.shape[:2]

            # undistort image
            undistort_image = cv2.undistort(img, mtx, dist, None, mtx0)

            # save undistorted image with corresponding index
            undistorted_file_name = os.path.join(basefolder, f"{file_name}_undist.png")
            cv2.imwrite(undistorted_file_name, undistort_image)
            print(f"Saved undistorted image: {undistorted_file_name}")

        except Exception as e:
            print(f"Error processing file {fname}: {e}")
            continue





def create_undistort_image(image_files_path, mtx, dist, mtx0):

    base_path = os.path.dirname(image_files_path)

    try:
        # read image
        img = cv2.imread(image_files_path)

        # Check if the image was successfully loaded
        if img is None:
            raise ValueError(f"Could not read image from {image_files_path}")

        # undistort image
        undistort_image = cv2.undistort(img, mtx, dist, None, mtx0)

        # save undistorted image with corresponding index
        undistorted_file_name = os.path.join(base_path, "undist.png")
        cv2.imwrite(undistorted_file_name, undistort_image)
        print(f"Saved undistorted image: {undistorted_file_name}")
        return undistorted_file_name
    
    except Exception as e:
        print(f"Error processing file {image_files_path}: {e}")
        





def save_calibration_data(calibration_file, mtx, dist, rvecs, tvecs):
    """Saves camera calibration data to a .npz file.

    Args:
        calibration_file (str): Path to save the .npz calibration file.
        mtx (numpy.ndarray): Camera matrix.
        dist (numpy.ndarray): Distortion coefficients.
        rvecs (list): Rotation vectors.
        tvecs (list): Translation vectors.
    """
    try:
        np.savez(calibration_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
        print(f"Calibration data saved to '{calibration_file}'")
    except Exception as e:
        print(f"Error saving calibration data to '{calibration_file}': {e}")




def open_calibration_data(calibration_file):
    """Loads camera calibration data from a .npz file.

    Args:
        calibration_file (str): Path to the .npz calibration file.

    Returns:
        tuple: Camera matrix, distortion coefficients, rotation vectors, translation vectors.
    """
    try:
        with np.load(calibration_file) as data:
            mtx = data['mtx']
            dist = data['dist']
            rvecs = data['rvecs']
            tvecs = data['tvecs']
        print(f"Calibration data loaded from '{calibration_file}'")
        print(f"Camera matrix : {mtx}\ndist : {dist}\nrvecs : {rvecs}\ntvecs : {tvecs}")
        return mtx, dist, rvecs, tvecs
    except Exception as e:
        print(f"Error loading calibration data from '{calibration_file}': {e}")
        return None, None, None, None
    
def generate_file_paths(file_extension,file_name):
    base_path = os.path.dirname(file_extension)
    file_path = os.path.join(base_path, file_name)
    return file_path



def traning_from_images(image_files_training):
    base_path = os.path.dirname(image_files_training)
    print(f'base_path: {base_path}')
    # look for other .bmp file in the same directory
    image_files_training_glob = [f for f in glob.glob(os.path.join(base_path, '*.PNG'))]
    #print(f'image_files_training_glob: {image_files_training_glob}')

    # learn distortion coefficients from training images
    ret, mtx, dist, rvecs, tvecs = learn_distortion(image_files_training_glob)

    # Save all calibration data into a single .npz file
    calibration_file_path = generate_file_paths(image_files_training, 'camera_calibration_data.npz')
    save_calibration_data(calibration_file_path, mtx, dist, rvecs, tvecs)


    # call image at a time 

    



#===========
# Test code
#===========



# basepath = r'C:/Users/michelle.lim/Downloads/radialdist/2024_04_07_08_31_05_gridimages/'
# image_files_training = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_07_15_39_05_camera_calibration\test4\Pic_2025_04_08_165416_7.bmp"


# image_files_training = r"C:\Users\malit\Documents\GitHub\2025_10_29_08_46_45\24252470_20251029104037.png"
# image_files_target = r"C:\Users\malit\Documents\GitHub\2025_10_29_08_46_45\test\24252470_20251029104037.png"

# camera_calibration_file_path = r"C:\Users\malit\Documents\GitHub\2D_optical_vision_mapping\src\recipes\camera_calibration_data_2X_lens.npz"
# # Step 1: train from images
# traning_from_images(image_files_training)

# # Step 2:open calibration data and create undistorted image
# mtx, dist, rvecs, tvecs = open_calibration_data(camera_calibration_file_path)
# create_undistort_image(image_files_target, mtx, dist, mtx)

# undistort( image_files_target, mtx, dist, mtx)

# cv2.destroyAllWindows()
