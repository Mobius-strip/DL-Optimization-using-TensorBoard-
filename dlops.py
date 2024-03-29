# -*- coding: utf-8 -*-
"""Dlops.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kkHf53Fe161YVBNfIYMCoDhlHTVMkxmK
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets

transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

trainset = datasets.CIFAR10(root='./data', train=True,
                            download=True, transform=transform_train)
train_loader = torch.utils.data.DataLoader(trainset, batch_size=128,
                                          shuffle=True, num_workers=2)

testset = datasets.CIFAR10(root='./data', train=False,
                           download=True, transform=transform_test)
test_loader = torch.utils.data.DataLoader(testset, batch_size=128,
                                         shuffle=False, num_workers=2)

"""# original """



class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(128 * 4 * 4, 10)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        x = x.view(-1, 128 * 4 * 4)
        x = self.fc(x)
        return x

!pip install torch-tb-profiler

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNNvanilla'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
#%tensorboard --logdir log
# %tensorboard --logdir ./logs

"""#model2 """

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        #self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(128 * 4 * 4, 10)

    def forward(self, x):
       # x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        #print(x.shape)
        x = x.view(-1, 128 * 4 * 4)
        x = self.fc(x)
        return x

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNN2'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

"""# model 3 """

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        #self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(128 * 4 * 4, 10)

    def forward(self, x):
       # x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        #print(x.shape)
        x = x.view(-1, 128 * 4 * 4)
        x = self.fc(x)
        return x

MyNet

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

model

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNN3'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

"""# model 4"""

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(256 * 4 * 4, 10)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        #print(x.shape)
        x = x.view(-1, 256* 4 * 4)
        x = self.fc(x)
        return x

MyNet

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

model

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNN4'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
#%tensorboard --logdir log
# %tensorboard --logdir ./logs



"""# model 5

"""





class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=1, stride=1)
        self.fc = nn.Linear(256 * 8 * 8, 10)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        #print(x.shape)
        x = x.view(-1, 256* 8 * 8)
        x = self.fc(x)
        return x

MyNet

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

model

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNN5'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
#%tensorboard --logdir log
# %tensorboard --logdir ./logs



"""# model 6

"""

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(64, 256, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(512*4*4, 10)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        #print(x.shape)
        x = x.view(-1, 512*4*4)
        x = self.fc(x)
        return x

MyNet

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

model

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNN6'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
#%tensorboard --logdir log
# %tensorboard --logdir ./logs



"""# model 7

"""

class MyNet(nn.Module):
    def __init__(self):
        super(MyNet, self).__init__()
        #self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(64, 256, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(512*4*4, 10)

    def forward(self, x):
        #x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool1(x)
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(x)
        x = nn.functional.relu(self.conv4(x))
        x = self.pool3(x)
        #print(x.shape)
        x = x.view(-1, 512*4*4)
        x = self.fc(x)
        return x

MyNet

import torch.optim as optim
import torch.nn.functional as F

# define the model
model = MyNet()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

model

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/CNN7'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
#%tensorboard --logdir log
# %tensorboard --logdir ./logs

"""# VGG"""

class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(256, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 10),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

model = VGG()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/vgg_OG'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)

"""## VGG1

"""

class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()
        self.features = nn.Sequential(
            #nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(256, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 10),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

model = VGG()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/vgg_1'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)



"""## VGG2


"""

class VGG(nn.Module):
    def __init__(self):
        super(VGG, self).__init__()
        self.features = nn.Sequential(
            #nn.Conv2d(3, 64, 3, padding=1),
            #nn.ReLU(inplace=True),
            #nn.Conv2d(3, 64, 3, padding=1),
            #nn.ReLU(inplace=True),
            #nn.MaxPool2d(2, 2),
            nn.Conv2d(3, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(256, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 10),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

model = VGG()
# move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = F.cross_entropy

# define the number of epochs to train for
num_epochs = 10

with torch.profiler.profile(
        schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./logs/vgg_2'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True
) as prof:
  for epoch in range(10):
    
    model.train()
    train_loss = 0
    train_correct = 0

    for step, batch_data in enumerate(train_loader):
        if step >= (1 + 1 + 3) * 2:
            break
    
        # iterate over the training data
        #for data, target in train_loader:
        data, target =batch_data  
        # move the data and target to the GPU if available
        data, target = data.to(device), target.to(device)
        # zero the gradients
        optimizer.zero_grad()
        # forward pass
        output = model(data)
        # calculate the loss
        loss = criterion(output, target)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()
        # calculate the number of correct predictions
        pred = output.argmax(dim=1, keepdim=True)
        train_correct += pred.eq(target.view_as(pred)).sum().item()
        # update the training loss
        train_loss += loss.item() * data.size(0)
        prof.step() 
    # calculate the training accuracy and loss for this epoch
    train_acc = train_correct / len(train_loader.dataset)
    train_loss /= len(train_loader.dataset)