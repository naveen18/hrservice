import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplot
import seaborn as sns
from sklearn.cluster import KMeans
from config.configparser import getConfig

def readData():
	conf = getConfig()
	data = pd.read_csv(conf.project_directory + '/mlmodel/HR_comma_sep.csv')
	return data;

def generateVisualisations():
	print("generating visualization")
	plt.switch_backend('agg')
	conf = getConfig()
	image_dir = conf.project_directory + "/userservice/static/images/"
	data = readData()
	corr = data.corr()
	sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, cmap=sns.diverging_palette(220, 10, as_cmap=True))
	plt.yticks(rotation=0)
	plt.xticks(rotation=90)
	plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.34)
	plt.savefig(image_dir + 'correlation.png')

	fig, axes = plt.subplots(ncols=2, figsize=(12, 6))

	sns.distplot(data.satisfaction_level, kde=False, color="r", ax=axes[0]).set_title('Employee Satisfaction Distribution') 
	axes[0].set_ylabel('Employee Count')

	sns.distplot(data.last_evaluation, kde=False, color="y", ax=axes[1]).set_title('Employee Evaluation Distribution')
	axes[1].set_ylabel('Employee Count')
	plt.tight_layout(True)
	plt.savefig(image_dir + 'distributions1.png')

	fig, axes = plt.subplots(ncols=2, figsize=(12, 6))
	sns.distplot(data.average_montly_hours, kde=False, color="b", ax=axes[0]).set_title('Average Monthly Hours spent by employee Distribution')
	axes[0].set_ylabel('Employee Count')

	sns.distplot(data.time_spend_company, kde=False, color="b", ax=axes[1]).set_title('Time Spent by employee at Company Distribution')
	axes[1].set_ylabel('Employee Count')
	plt.tight_layout(True)
	plt.savefig(image_dir + 'distributions2.png')

	fig, ax = plt.subplots(figsize=(12, 6))
	sns.countplot(y="salary", hue='left', data=data, color = [145/255, 176/255, 47/255]).set_title('Employee Salary, Employee Left Distribution');
	plt.savefig(image_dir + 'distributions3.png')

	fig, ax = plt.subplots(figsize=(12, 6))
	sns.countplot(y="sales", hue='left', data=data, color = [155/255, 149/255, 78/255]).set_title('Employee Department, Employee Left Distribution');
	plt.savefig(image_dir + 'distributions4.png')

	fig, ax = plt.subplots(figsize=(12, 6))
	sns.countplot(x="number_project", hue="left", data=data, color=[63/255, 60/255, 89/255]).set_title('Number of Project, Employee Left Distribution');
	plt.savefig(image_dir + 'distributions5.png')

	kmeans = KMeans(n_clusters=3,random_state=2)
	kmeans.fit(data[data.left==1][["satisfaction_level","last_evaluation"]])
	kmeans_colors = ['red' if c == 0 else 'black' if c == 2 else 'blue' for c in kmeans.labels_]
	fig = plt.figure(figsize=(12, 8))
	plt.scatter(x="satisfaction_level",y="last_evaluation", data=data[data.left==1], alpha=0.25,color = kmeans_colors)
	plt.xlabel("Employee Satisfaction")
	plt.ylabel("Employee Evaluation")
	plt.scatter(x=kmeans.cluster_centers_[:,0],y=kmeans.cluster_centers_[:,1],color="black",marker="x",s=100)
	plt.title("Clusters of Employee Turnover")
	plt.savefig(image_dir + 'clusters.png')

if __name__ == '__main__':
	generateVisualisations()




