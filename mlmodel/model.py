import sys
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score,train_test_split 
from sklearn import tree
from sklearn import neighbors
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import perceptron
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from config.configparser import getConfig
import pydotplus
import numpy as np

model = None

def get_labels():
	return ["satisfaction_level","last_evaluation","number_project","average_monthly_hours",\
	"time_spend_company","Work_accident","promotion_last_5years","from_product_mng_dept","from_marketing_dept",\
	"from_technical_dept", "from_sales_dept", "from_hr_dept", "from_IT_dept", "from_RandD_dept", "from_accounting_dept",\
	"from_management_dept", "from_support_dept", "has_low_salary", "has_medium_salary", "has_high_salary"]

def readData():
	conf = getConfig()
	data = pd.read_csv(conf.project_directory + '/mlmodel/HR_comma_sep.csv')
	return data;


def processData(data):
	Y = data["left"]
	Y = list(Y)
	data = data.drop('left', 1)
	# one hot encoding for department
	data["from_product_mng_dept"] = [1 if dept == "product_mng" else 0 for dept in data['sales']]
	data["from_marketing_dept"] = [1 if dept == "marketing" else 0 for dept in data['sales']]
	data["from_technical_dept"] = [1 if dept == "technical" else 0 for dept in data['sales']]
	data["from_sales_dept"] = [1 if dept == "sales" else 0 for dept in data['sales']]
	data["from_hr_dept"] = [1 if dept == "hr" else 0 for dept in data['sales']]
	data["from_IT_dept"] = [1 if dept == "IT" else 0 for dept in data['sales']]
	data["from_RandD_dept"] = [1 if dept == "RandD" else 0 for dept in data['sales']]
	data["from_accounting_dept"] = [1 if dept == "accounting" else 0 for dept in data['sales']]
	data["from_management_dept"] = [1 if dept == "management" else 0 for dept in data['sales']]
	data["from_support_dept"] = [1 if dept == "support" else 0 for dept in data['sales']]
	# one hot encoding for salary
	data["has_low_salary"] = [1 if salary == "low" else 0 for salary in data['salary']]
	data["has_medium_salary"] = [1 if salary == "medium" else 0 for salary in data['salary']]
	data["has_high_salary"] = [1 if salary == "high" else 0 for salary in data['salary']]
	# drop string columns after one hot encoding
	data = data.drop('salary', 1)
	data = data.drop('sales', 1)
	data = data.values.tolist()
	result = train_test_split(data, Y, test_size=0.20, random_state=0)
	return result

def generate_graph(x_train, y_train, file_name, title, xlabel, ylabel):
	colors = ['navy', 'turquoise'] # 'darkorange'
	for color, _class in zip(colors, ['male', 'female']):
		# _x = x_train[y_train == _class, 0]
		# _y = np.zeros(len(_x))
		# plt.scatter(_x, _y, color=color, alpha=.8, lw=2, label=_class)
	    plt.scatter(x_train[y_train == _class, 0], x_train[y_train == _class, 1], color=color, alpha=.8, lw=2, label=_class)
	plt.legend(loc='best', shadow=False, scatterpoints=1)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	# plt.show()
	plt.savefig(file_name)

def runDecisionTreeModel(x_train, x_test, y_train, y_test):
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("decision_tree: %.15f" % scores.mean())

def run_k_nearest_neighbour(x_train, x_test, y_train, y_test):
	clf = neighbors.KNeighborsClassifier(10, 'uniform')
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("k_nearest_neighbour: %.15f" % scores.mean())

def run_logistic_regression(x_train, x_test, y_train, y_test):
	clf = linear_model.LogisticRegression(penalty='l1', verbose=0, random_state=None, fit_intercept=True)
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("logistic_regression: %.15f" % scores.mean())

def run_naive_bayes(x_train, x_test, y_train, y_test):
	clf = GaussianNB()
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("naive_bayes: %.15f" % scores.mean())


def run_neural_network(x_train, x_test, y_train, y_test):
	clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=0)
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("neural_network: %.15f" % scores.mean())

def run_perceptron(x_train, x_test, y_train, y_test):
	clf = perceptron.Perceptron(penalty='l1', max_iter=100, verbose=0, random_state=None, fit_intercept=True, eta0=0.02)
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("perceptron: %.15f" % scores.mean())


def run_random_forest(x_train, x_test, y_train, y_test, return_model = False):
	clf = RandomForestClassifier(n_estimators=10)
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("random_forest: %.15f" % scores.mean())
	if return_model == True:
		return clf

def run_svm(x_train, x_test, y_train, y_test):
	clf = svm.SVC()
	clf.fit(x_train, y_train)
	scores = cross_val_score(clf, x_test, y_test, cv=5)
	print("SVM: %.15f" % scores.mean())

def run_pca(x_train, x_test, y_train, y_test, n_components=2, to_generate_graph = True):
	pca = PCA(n_components=n_components)
	pca.fit(x_train)

	labels = get_labels()

	x_train_new = pca.transform(x_train)
	x_test_new = pca.transform(x_test)

	if(to_generate_graph):
		generate_graph(x_train_new, y_train, 'employee.png', 'PCA(2) plot of Voice dataset', "x", "y")

	return x_train_new, x_test_new

def predict(args):
	global model
	if model is None:
		data = readData()
		x_train, x_test, y_train, y_test = processData(data)
		"training model"
		model = run_random_forest(x_train, x_test, y_train, y_test, return_model = True)
	args = np.array(args)
	args = args.astype(np.float)
	args.reshape(1,-1)
	Y = model.predict([args])
	return Y[0]

if __name__ == '__main__':
	data = readData()
	x_train, x_test, y_train, y_test = processData(data)
	print("=======Decision Tree===============")
	runDecisionTreeModel(x_train, x_test, y_train, y_test)

	print("=======k_nearest_neighbour===============")
	run_k_nearest_neighbour(x_train, x_test, y_train, y_test)

	print("=======logistic_regression===============")
	run_logistic_regression(x_train, x_test, y_train, y_test)

	print("=======naive_bayes===============")
	run_naive_bayes(x_train, x_test, y_train, y_test)

	print("=======neural_network===============")
	run_neural_network(x_train, x_test, y_train, y_test)

	print("=======perceptron===============")
	run_perceptron(x_train, x_test, y_train, y_test)

	print("=======random_forest===============")
	run_random_forest(x_train, x_test, y_train, y_test)

	print("=======svm===============")
	run_svm(x_train, x_test, y_train, y_test)

	# print("=======pca===============")
	# run_pca(x_train, x_test, y_train, y_test)
