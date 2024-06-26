# -*- coding: utf-8 -*-
"""Clustering Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d6zj4RH-B3qw8e5fgbto1NVzfbvosDH6
"""

#kmeans clustering
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler , LabelEncoder

data=pd.read_csv("/content/sample_data/customer_segmentation.csv")
data.head()

data.shape

data.info()

data.describe()

#to find null values
data.isnull().sum()

#handling null values
data.dropna(inplace=True)

#handling duplicates
data.duplicated().sum()

#detecting outliers
plt.figure(figsize=(15,6))
sns.boxplot(data)

num_col=data.columns[data.dtypes!="object"]
cat_col=data.columns[data.dtypes=="object"]

def remove_out(df1):
	num_col=df1.columns[df1.dtypes!="object"]
	for i in num_col:
		q1=df1[i].quantile(0.25)
		q3=df1[i].quantile(0.75)
		iqr=q3-q1
		med=df1[i].median()
		df1[i]=np.where((df1[i]<q1-1.5*iqr) | (df1[i]>q3+1.5*iqr),med,df1[i])
	return(df1)

outlier1=remove_out(data)
#outliers removed

data.isnull().sum()

data.info()

from sklearn.impute import SimpleImputer
imp = SimpleImputer(strategy="mean")
data["Recency"]=imp.fit_transform(data[["Recency"]])
data.isnull().sum()

for j in cat_col:
	data[j]=LabelEncoder().fit_transform(data[j])
#encoded the categorical column

sns.heatmap(data.corr(),annot=True,cmap="viridis")

#scaling
mi_ma_s = MinMaxScaler()
X = mi_ma_s.fit_transform(data)
X = pd.DataFrame(data)
print(X.head())

#finding the optimal value of k using elbow method an dsilhoette method
inertia_values = []
silhouette_scores = []
k_values = range(2, 10)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X, kmeans.labels_))

plt.plot(k_values, inertia_values, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Curve for Optimal k')
plt.xticks(k_values)
plt.show()

plt.plot(k_values, silhouette_scores, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Scores for Optimal k')
plt.xticks(k_values)
plt.show()

optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(X)

cluster_labels = kmeans.predict(X)

#silhouette score
silhouette_avg = silhouette_score(X, cluster_labels)
print("silhouette score: ",silhouette_avg)

data['Cluster'] = kmeans.labels_
cluster_profiles = data.groupby('Cluster').mean()
print(cluster_profiles)

# Add cluster labels to the original data
data['Cluster'] = kmeans.labels_

data.head()

