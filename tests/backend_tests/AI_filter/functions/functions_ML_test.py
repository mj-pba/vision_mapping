
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

class IntensityGraphAutoencoder(nn.Module): # X interpolated pixels (inputsize)
    def __init__(self, inputsize):
        super(IntensityGraphAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(inputsize*100, 550),  # Adjusted input size to X and hidden layers
            nn.ReLU(),
            nn.Linear(550, 275),
            nn.ReLU(),
            nn.Linear(275, 100),
            nn.ReLU(),
            nn.Linear(100, 50),  # Bottleneck layer (can be adjusted)
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(50, 100),
            nn.ReLU(),
            nn.Linear(100, 275),
            nn.ReLU(),
            nn.Linear(275, 550),
            nn.ReLU(),
            nn.Linear(550, inputsize*100),
            nn.Sigmoid()  # so reconstructed output is btwn 0-1 (interpretable!)
        )
    
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    
class IntensityGraphDataset(Dataset):
    def __init__(self, intensity_graphs):
        self.intensity_graphs = intensity_graphs

    def __len__(self):
        return len(self.intensity_graphs)

    def __getitem__(self, idx):
        intensity_graph = torch.tensor(self.intensity_graphs[idx], dtype=torch.float32)
        return intensity_graph
    
def custom_loss_intensity(reconstructed_graphs, original_graphs, device):
    # Reconstruction Loss
    reconstruction_loss = nn.MSELoss()(reconstructed_graphs, original_graphs).to(device)
    
    # std dev loss
    std_dev_loss = torch.std(reconstructed_graphs, dim=0).mean()  # Penalizing high std deviation across images. changing dim to 1 will compare stddev across the intensity graph instd of btwn images, so not right. you'll end up w straight line.
    # print(f'std dev loss: {std_dev_loss*100000}, {np.shape(reconstructed_graphs)}')
    
    # combined Loss
    loss = reconstruction_loss  + std_dev_loss 
    return loss

# Assuming i have average_graphs and std_dev_target precomputed
def train_autoencoder(model, optimizer, device, dataloader, num_epochs=25):
    model.train()
    epoch_losses = []
    #torch.cuda.synchronize()
    start_time = time.time()
    for epoch in range(num_epochs):
        running_loss = 0.0
        for intensity_graphs in dataloader:  # Unpack directly
            intensity_graphs = intensity_graphs.to(device)  # Send to device
            optimizer.zero_grad()
            reconstructed_graphs = model(intensity_graphs)
            loss = custom_loss_intensity(reconstructed_graphs, intensity_graphs, device) #recon loss + stddev loss
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        epoch_losses.append(running_loss/len(dataloader))
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(dataloader)}')
        reconstruction_loss = nn.MSELoss()(reconstructed_graphs, intensity_graphs).item()
        std_dev_loss = torch.std(reconstructed_graphs, dim=0).mean().item()
        print(f'Reconstruction Loss: {reconstruction_loss:.4f}, Std Dev Loss: {std_dev_loss:.12f}')
        # print(f'Reconstructed Graph (sample): {reconstructed_graphs[0].detach().cpu().numpy()[:5]}\n')

        ''' OPTIONAL: plot orig vs recon graphs after last epoch '''
        if (epoch ==num_epochs-1):
            plt.figure(figsize=(18,12))
            plt.subplot(2,2,1)
            for i in range(8): 
                plt.plot(reconstructed_graphs[i].detach().cpu().numpy())
            plt.title("reconstructed graphs (random 8)")

            plt.subplot(2,2,2)
            for j in range(8):
                plt.plot(intensity_graphs[j].cpu())
            plt.title("original graphs (random 8)")

            plt.subplot(2,2,3)
            for k in range(8):
                plt.plot(reconstructed_graphs[k].detach().cpu().numpy(), color='c')
                plt.plot(intensity_graphs[k].cpu(), color='r')
            plt.title("og vs recon graphs (random 8)")
            og_patch = mpatches.Patch(color='red', label='og data')
            recon_patch = mpatches.Patch(color='c', label='recon data')
            plt.legend(handles=[og_patch, recon_patch])

    print(f'training time: {time.time() - start_time}s')
    plt.subplot(2,2,4)
    plt.plot(epoch_losses)
    plt.title("loss")
    # plt.subplots_adjust(hspace=0.8)  # Increase or decrease the value to adjust spacing
    plt.show()

    