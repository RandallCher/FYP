#### THIS FILE CONTAINS COMMON FUNCTIONS AND CLASSES


from torch import nn 
from sklearn import preprocessing
import torch


def preprocess_dataset(df_train, df_test):

    standard_scaler = preprocessing.StandardScaler()
    df_train_scaled = standard_scaler.fit_transform(df_train)

    df_test_scaled = standard_scaler.transform(df_test)

    return df_train_scaled, df_test_scaled

# class MLPBuilder(nn.Module):

#     def __init__(self, no_features, layers, no_labels = 64):
#         super().__init__()
#         layer_list = []
        
#         # Input layer
#         layer_list.append(nn.Linear(no_features, layers[0]))
#         layer_list.append(nn.ReLU())
#         layer_list.append(nn.Dropout(p=0.2))

#         # Hidden layers
#         for i in range(len(layers) - 1):
#             layer_list.append(nn.Linear(layers[i], layers[i+1]))
#             layer_list.append(nn.ReLU())
#             layer_list.append(nn.Dropout(p=0.2))

#         # Define the MLP stack as a sequential model
#         self.mlp_stack = nn.Sequential(*layer_list)

#         # Output layer, 1 outputs
#         self.output_x = nn.Linear(layers[-1], 8) 
#         self.output_y = nn.Linear(layers[-1], 8) 


#         self._initialize_weights() 
        
#     def forward(self, x):
#         features = self.mlp_stack(x)
#         logits_x = self.output_x(features)
#         logits_y = self.output_y(features)
#         return logits_x, logits_y
    
#     def _initialize_weights(self):
#         for layer in self.mlp_stack:
#             if isinstance(layer, nn.Linear):
#                 # Use Kaiming initialization for ReLU activations
#                 nn.init.kaiming_uniform_(layer.weight, nonlinearity='relu')
#                 if layer.bias is not None:
#                     nn.init.zeros_(layer.bias)

    
def train_loop(dataloader, model, loss_fn_x, loss_fn_y, optimizer):
    model.train()
    total_loss = 0
    total_correct = 0
    total_samples = 0

    for inputs, targets_x, targets_y in dataloader:
        optimizer.zero_grad()

        # Forward pass
        logits_x, logits_y = model(inputs)

        # Compute loss
        loss_x = loss_fn_x(logits_x, targets_x)
        loss_y = loss_fn_y(logits_y, targets_y)
        loss = loss_x + loss_y

        # Backpropagation
        loss.backward()
        optimizer.step()

        # Calculate accuracy
        preds_x = torch.argmax(logits_x, dim=1)
        preds_y = torch.argmax(logits_y, dim=1)
        correct = (preds_x == targets_x) & (preds_y == targets_y)  # Joint correctness
        total_correct += correct.sum().item()
        total_samples += inputs.size(0)
        total_loss += loss.item() * inputs.size(0)

    avg_loss = total_loss / total_samples
    accuracy = total_correct / total_samples * 100
    return avg_loss, accuracy

def test_loop(dataloader, model, loss_fn_x, loss_fn_y):
    model.eval()
    total_loss = 0
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for inputs, targets_x, targets_y in dataloader:
            logits_x, logits_y = model(inputs)

            loss_x = loss_fn_x(logits_x, targets_x)
            loss_y = loss_fn_y(logits_y, targets_y)
            loss = loss_x + loss_y

            preds_x = torch.argmax(logits_x, dim=1)
            preds_y = torch.argmax(logits_y, dim=1)
            correct = (preds_x == targets_x) & (preds_y == targets_y)
            total_correct += correct.sum().item()
            total_samples += inputs.size(0)
            total_loss += loss.item() * inputs.size(0)

    avg_loss = total_loss / total_samples
    accuracy = total_correct / total_samples * 100
    return avg_loss, accuracy
