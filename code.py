import os
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from dotenv import load_dotenv
from mistralai import Mistral

#load env vars
load_dotenv()
file_path=os.getenv("FILE_PATH")

#start mistral client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# load text data and extract relevant column
df = pd.read_csv("file_path")
positions = df['position_text']

# run position text through embeddings model
results = client.embeddings.create(inputs=positions, model="mistral-embed")
embeddings = [data.embedding for data in results.data]

# dimensionality reduction on embeddings vector, 1024 --> 3
tsne = TSNE(n_components=3)
reduced_embeddings = tsne.fit_transform(np.array(embeddings))

# kmeans clustering on reduced embeddings vector
kmeans = KMeans(n_clusters=5, random_state=0)
clusters = kmeans.fit_predict(np.array(reduced_embeddings))

# plot the results:
colors = ['r', 'g', 'b', 'k', 'm']
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i in range(len(clusters)-1):
    color_idx= clusters[i]
    ax.scatter(reduced_embeddings[i,0], reduced_embeddings[i,1], reduced_embeddings[i,2],color=colors[color_idx])
plt.show()  
