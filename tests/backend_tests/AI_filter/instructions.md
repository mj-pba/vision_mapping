# Script explanation

## USER ADJUSTABLE PARAMETERS

- NOTE: If script is integrated into main application, these params should be placed in a recipe file.
- seed: used to provide a seed value for the random function. Used when shuffling datasets. Should be constant to get comparable results between runs.

- PIXELNUMBER: How many pixels captured at edge (widthwise), from black to white/white to black.

- interpolation_factor: Interpolation factor, i.e. how many pixels to interpolate per pixel.

- num_epochs: no. of epochs to train the model. adjust freely. observe the loss curve to monitor how well the model is learning.

- batch_size: how many sets of data to process per run

- segment_half_height: half the height of cropped image. too large value will cause shakier reconstructed graphs due to more 
variance in intensity shape, but effect is not as bad as increasing num_files_training

- num_files_training: Number of files used for training. Must be a factor of batch size. smaller val for smoother reconstructed images.

- folderpath_radiuscalc: folder path of '2025_03_25_18_50_51_raduis_calculation'. Change if needed.

## How script works

1. Folder looks for folder called '2025_03_25_18_50_51_raduis_calculation'. Folder should contain circle parameters, and all .png images of the circle

2. Open circle image

3. Grayscale image

4. Use circle parameters to crop out the north, south, east and west edge regions of the circle. Size of cropped regions is defined within PARAMETERS section. 

5. Average the intensity of cropped images across the height. Will end up collapsing the image from (height x width) to (1 x width) dimensions

6. Interpolate image by factor of interpolation_factor

7. Repeat process for all images

8. Grab a specified number of images for training set (num_files_training)

9. Shuffle images

10. Run training images through model for training

11. Save model

12. Grab remaining number of images for testing set. No need to shuffle.

13. Run images through saved model to test/verify saved model

14. OPTIONAL: Plots relevant graphs for visualisation

15. To run script for single image, use code within 'Sample original segment vs reconstructed segment. can be used for single image evaluation in larger codebases'



# Enviroment setup

## Conda
```bash
conda create -n vision_ai_filter python=3.12.0
conda activate vision_ai_filter

```


```bash
pip install opencv-python
pip install numpy
pip install pandas
pip install matplotlib
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

```