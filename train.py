import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader

# 1. Transformations des images pour ResNet (redimensionnement et normalisation)
transformations = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 2. Chargement du dataset Food-101 (pointe vers ton dossier extrait food-101)
print("Chargement du dataset Food-101...")
# Assure-toi que le dossier 'food-101' est bien dans ton projet ou indique son chemin exact dans root
train_dataset = datasets.Food101(root='./', split='train', transform=transformations, download=False)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 3. Chargement du modèle pré-entraîné (ResNet-50)
print("Chargement du modèle de Deep Learning (ResNet-50)...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

# Modification de la dernière couche pour qu'elle corresponde aux 101 classes du dataset
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 101)

# Utilisation du GPU si disponible (très recommandé pour accélérer)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# 4. Fonction de perte et optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Entraînement (tu peux ajuster le nombre d'époques 'epochs' selon ta puissance de calcul)
epochs = 2 
print(f"Début de l'entraînement sur {device}...")

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        if i % 50 == 0:
            print(f"Époque [{epoch+1}/{epochs}], Batch [{i}/{len(train_loader)}], Loss: {loss.item():.4f}")

# 6. Sauvegarde des poids du modèle entraîné
torch.save(model.state_dict(), "model-food.pth")
print("Entraînement terminé ! Modèle sauvegardé sous 'model-food.pth'.")