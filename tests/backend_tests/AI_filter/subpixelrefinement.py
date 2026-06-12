import  cv2
import numpy as np
import glob
import random
import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
import matplotlib.pyplot as plt
import matplotlib.patches as mptch
import pandas as pd
import os

from functions.functions_ML_test import  train_autoencoder, IntensityGraphAutoencoder, IntensityGraphDataset
from functions.functions_preprocessing import expandPixels, pull_pixelvals_from_single_img, subpixel_edge_refinement, resize_image, viewarray_asbmp


'''======== PARAMETERS. TODO: send all these parameters to a recipe file to keep script clean. Also change folderpath to your own folderpath ========'''
seed = 42
# no. of pixels to be interpolated
PIXELNUMBER = 15 # how many pixels captured at edge, from black to white/white to black.
interpolation_factor = 100 # interpolation factor, i.e. how many pixels to interpolate per pixel.
num_epochs = 55 # no. of epochs to train the model. adjust freely. observe the loss curve to monitor how well the model is learning.
batch_size = 8 # 
segment_half_height = 10 # too large will cause shakier reconstructed graphs due to more variance in intensity shape, but effect is not as bad as increasing num_files_training
num_files_training = 24 # must be a factor of batch size. smaller val for smoother reconstructed images.
cwd = os.getcwd()
# folderpath_radiuscalc = os.path.join(cwd, '2025_03_25_18_50_51_raduis_calculation') # change this to your own folder path
folderpath_radiuscalc = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_03_25_18_50_51_raduis_calculation"
#circleparamspath = f'{folderpath_radiuscalc}\\circle_parameters.csv'
circleparamspath = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_03_25_18_50_51_raduis_calculation\circle_parameters.csv"

filenames = glob.glob(folderpath_radiuscalc + r"\*.png")
'''======== END OF PARAMETERS ========'''

torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)

'''======== open and preprocess images ========'''
data = pd.read_csv(circleparamspath) # read circle parameters
data = data.to_numpy()
all_intensity_averages = [] # initialize list to store extracted intensity averages from the 31 images\
len_firsthalf = int(PIXELNUMBER/2)
len_secondhalf = PIXELNUMBER - len_firsthalf

for i in range(data.shape[0]-5):    # crop out end of csv, which has other data
    single_all_intensity_averages = pull_pixelvals_from_single_img(PIXELNUMBER, segment_half_height, len_firsthalf, len_secondhalf, filenames[i], x=data[i][2], y=data[i][1], r=data[i][3])
    if len(all_intensity_averages) == 0:
        all_intensity_averages = single_all_intensity_averages # runs only once, so no need to stack
    else:
        all_intensity_averages = np.vstack((all_intensity_averages, single_all_intensity_averages))  # stack row-wise

interpolated_values = expandPixels(all_intensity_averages, interpolation_factor, PIXELNUMBER)
interpol_min = np.min(interpolated_values)
interpol_max = np.max(interpolated_values)

interpolated_values = (interpolated_values - interpol_min) / (interpol_max - interpol_min)
#for single segment
print(f'shape of interpolated values: {np.shape(interpolated_values)}')
'''======== END OF open and preprocess images ========'''

'''======== Load training data into model for training ========'''
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# device = 'cpu'
print(device)
model = IntensityGraphAutoencoder(PIXELNUMBER).to(device)
print(model)
num_files_training = 24 #120 # 24
intensity_dataset = IntensityGraphDataset(interpolated_values[:num_files_training]) 
print(f'shape of dataset input for training : {np.shape(intensity_dataset)}')
intensity_dataloader = DataLoader(intensity_dataset, batch_size=batch_size, shuffle=True) #batchsize: no. of files processed per batch. last epoch will have less processed if total!=factor of batch size, so careful when printing subplot (3,1,1) in train_autoencoder()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# train_model(model, optimizer, dataloader)
train_autoencoder(model, optimizer, device, intensity_dataloader, num_epochs)

# Save model's state dictionary
if not os.path.exists('./savedmodels'):
    os.makedirs('./savedmodels')
torch.save(model.state_dict(), f'./savedmodels/1autoenc_model_linearL_interpol{PIXELNUMBER}00_{batch_size}b001L{num_epochs}ee.pth')
'''======== END OF load training data into model for training ========'''

'''======== Load testing data into model for evaluation/testing ========'''
model = IntensityGraphAutoencoder(PIXELNUMBER) #prev was 8b3L
model.load_state_dict(torch.load(f'./savedmodels/1autoenc_model_linearL_interpol{PIXELNUMBER}00_{batch_size}b001L{num_epochs}ee.pth', weights_only=True))
model.eval()  # Set the model to evaluation mode

# Creating a Dataset and DataLoader for the new data
num_files_training = 216
new_dataset = IntensityGraphDataset(interpolated_values[num_files_training:])
print(f'shape of test set: {np.shape(new_dataset)}')
new_dataloader = DataLoader(new_dataset, batch_size=batch_size, shuffle=False)

reconstructed_graphs = []

with torch.no_grad():  # disable gradient calculation cuz we're in inference mode
    for intensity_dataset in new_dataloader:
        intensity_dataset = intensity_dataset  # .to(device) if using GPU
        outputs = model(intensity_dataset)
        reconstructed_graphs.extend(outputs.numpy())  # Collecting all reconstructed graphs

# convert list to numpy array for easier handling
reconstructed_graphs = np.array(reconstructed_graphs)
'''======== END OF Load testing data into model for evaluation/testing ========'''

''' ======== Plotting orig vs reconstructed graphs (OPTIONAL) ========'''
plt.figure(figsize=(10,8))
zoommin, zoommax = 51,53 # scaled zoom into reconstructed graphs, to see the separate lines more clearly.
midpt_interpol = []
midpt_recon = []
plt.subplot(3, 2, 1)
for i in range(len(reconstructed_graphs)):
    plt.plot(interpolated_values[i], color='r', alpha=0.7)
    plt.plot(reconstructed_graphs[i], color='c', alpha=0.5)
    deriv_interpol = np.gradient(interpolated_values[i])
    deriv_recon = np.gradient(reconstructed_graphs[i])
    line_interpol = np.argmax(np.abs(deriv_interpol))
    line_recon = np.argmax(np.abs(deriv_recon))
    refined_line_interpol = subpixel_edge_refinement(np.abs(deriv_interpol), line_interpol)
    refined_line_recon = subpixel_edge_refinement(np.abs(deriv_recon), line_recon)
    
    midpt_interpol.append(refined_line_interpol)
    midpt_recon.append(refined_line_recon)
    plt.axvline(line_interpol, color='r')
    plt.axvline(line_recon, color='c')
interpol_patch = mptch.Patch(color='r', label='OG interpolated data')
reconstr_patch = mptch.Patch(color='c', label='reconstructed data')
plt.legend(handles=[interpol_patch, reconstr_patch])
plt.title(f'Original interpolated vs reconstructed graphs ({len(reconstructed_graphs)} files)')

plt.subplot(3,2,2)
for i in range(len(reconstructed_graphs)):  
    plt.plot(reconstructed_graphs[i], label='Reconstructed', alpha = 0.4)
    # plt.legend()
plt.title(f'(ZOOM)Reconstructed Intensity Graphs from test set ({len(reconstructed_graphs)} files)')
plt.xlim(zoommin,zoommax)
plt.ylim(np.min(reconstructed_graphs[:,zoommin:zoommax]), np.max(reconstructed_graphs[:,zoommin:zoommax]))

plt.subplot(3, 2, 3)
for i in range (len(interpolated_values)):
    plt.plot(interpolated_values[i], label='Interpolated')
plt.title(f'Original Interpolated Intensity Graphs (all {len(interpolated_values)})')

plt.subplot(3,2,4)
for i in range(len(reconstructed_graphs)):  
    plt.plot(reconstructed_graphs[i], label='Reconstructed', alpha = 0.4)
    # plt.legend()
plt.title(f'Reconstructed Intensity Graphs frm test set({len(reconstructed_graphs)} files)')

plt.subplot(3, 2, 5)
for i in range (len(interpolated_values)):
    plt.plot(interpolated_values[i]*255, label='Interpolated')
plt.title(f'Original Interpolated Intensity Graphs (all {len(interpolated_values)}, denorm)')

plt.subplot(3, 2, 6)
for i in range (len(reconstructed_graphs)):
    plt.plot(reconstructed_graphs[i]*255, label='Reconstructed')
plt.title(f'Reconstructed Interpolated Intensity Graphs ({len(reconstructed_graphs)} files, denorm)')

plt.tight_layout()
plt.subplots_adjust(wspace=0.14)
if not os.path.exists('./plots'):
    os.makedirs('./plots')
imagepath = f'./plots/reconstructed_vs_interpolated_1autoenc_model_linearL_interpol{PIXELNUMBER}00_{batch_size}b001L{num_epochs}ee.png'
plt.savefig(imagepath)
plt.show()
np.set_printoptions(precision=10)
print(f'origl length: {len(midpt_interpol)}, stddev: {np.std(midpt_interpol, dtype=np.float64)}')
print(f'recon length: {len(midpt_recon)}, stddev: {np.std(midpt_recon,  dtype=np.float64)}')

resized_interpol = resize_image(interpolated_values[0]*255, PIXELNUMBER) # view sample original image resized back to orig num of pixels
viewarray_asbmp(resized_interpol.flatten(), pixelarrayname=f'orig img resized back to {PIXELNUMBER} pixels')
resized_recon = resize_image(reconstructed_graphs[0]*255, PIXELNUMBER) # view sample reconstructed image resized back to orig num of pixels
viewarray_asbmp(resized_recon.flatten(), pixelarrayname=f'reconstructed img resized back to {PIXELNUMBER} pixels')

'''======== END OF Plotting orig vs reconstructed graphs (OPTIONAL) ========'''


''' ======== Sample original segment vs reconstructed segment. can be used for single image evaluation in larger codebases ========'''
test_index = 1  # or 0, or any valid index in the test set
filename_index = num_files_training + test_index

# extact original segment for this image
circle_params = data[filename_index]
orig_segment = pull_pixelvals_from_single_img(
    PIXELNUMBER, segment_half_height, len_firsthalf, len_secondhalf,
    filenames[filename_index], x=circle_params[2], y=circle_params[1], r=circle_params[3]
)

# get orig segment, and reconstructed segment to compare
interpolated_segment = expandPixels(orig_segment, interpolation_factor, PIXELNUMBER)[0]
reconstructed_segment = reconstructed_graphs[test_index]

# do some scaling to match orig segmt's range, then resize to pixelnumber
reconstructed_norm = (reconstructed_segment - np.min(reconstructed_segment)) / (np.max(reconstructed_segment) - np.min(reconstructed_segment))
reconstructed_rescaled = reconstructed_norm * (np.max(orig_segment) - np.min(orig_segment)) + np.min(orig_segment)
reconstructed_resized = resize_image(reconstructed_rescaled, PIXELNUMBER).flatten() # save this as a bmp if you want to reconstruct the edges yourself.
print(f'Original segment (length {len(orig_segment)}x{len(orig_segment[0])})')
print(f'Reconstructed segment (length 1x{len(reconstructed_resized)})')

for x in range(len(orig_segment)):
    plt.plot(orig_segment[x], label='Original Segment', color='blue', alpha=0.5)
plt.plot(reconstructed_resized, label='Reconstructed Segment', color='red')
plt.legend()
plt.title(f'Original({len(orig_segment)}) vs Reconstructed Segment') # original has that many segments as we are sampling 2xsegment_half_height rows, the average of 3 rows each.
plt.show()
from PIL import Image
im_orig = Image.fromarray(orig_segment[0].astype(np.uint8).reshape(1, -1))  # Convert to uint8 for saving as image
im_orig.save(f'{folderpath_radiuscalc}\\orig_img.bmp')
im_recon = Image.fromarray(reconstructed_resized.astype(np.uint8).reshape(1, -1))  # Convert to uint8 for saving as image
im_recon.save(f'{folderpath_radiuscalc}\\reconstructed_img.bmp')

# plt.savefig(f'{folderpath}\\reconstructed_vs_interpolated_1autoenc_model_linearL_interpol{PIXELNUMBER}00_8b001L55ee.png')
'''======== END OF Sample original segment vs reconstructed segment ========'''