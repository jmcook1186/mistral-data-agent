import os
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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

# determine optimum number of clusters using silhouette score
scs = []
n_clusters_range = np.arange(2,len(positions),1)
for n_clusters in n_clusters_range:
    _kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    _clusters = _kmeans.fit_predict(np.array(reduced_embeddings))
    _sc = silhouette_score(reduced_embeddings, _clusters)
    scs.append(_sc)
optimum_n_clusters = n_clusters_range[np.argmax(scs)]


# run final kmeans with optimal clusters
kmeans = KMeans(n_clusters=optimum_n_clusters, random_state=0)
clusters = kmeans.fit_predict(np.array(reduced_embeddings))


# plot the results:
colors = ['r', 'g', 'b', 'k', 'm']
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i in range(len(clusters)-1):
    color_idx= clusters[i]
    ax.scatter(reduced_embeddings[i,0], reduced_embeddings[i,1], reduced_embeddings[i,2],color=colors[color_idx])
plt.show()  
