# -*- coding: utf-8 -*-
"""Titanic Dataset .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kAb5ZWOrO9pGgaLYzGmVJ9hJNJ-auhRK

## Description: this program will predict if a passenger will survive on the titanic


```
# This is formatted as code
```
"""

#import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#load the titanic dataset
titanic=sns.load_dataset('titanic')
#print the first 10 rows of the dataset
titanic.head(10)



"""Now here we can see that the PClass and Class is same so one of them can be removed and same for embark and Embark_town"""

#Count the number of rows and columns in the  dataset
titanic.shape

"""So we have around 891 passengers with their discription given in 15 columns"""

# to get the SDME statistics for the dataset
titanic.describe()

#get a count of the number of survived
titanic['survived'].value_counts()

"""549 passengers did not survive and 342 survived. The data is quite balanced as we can see the 39% of data is shows the survival rate while the 61% did not make it.39:61 shows a pretty balanced data."""

#visualize the counts
sns.countplot(titanic['survived'])

#visualize the count of survivors for columns which are 'who','sex','pclass','parch','embarked'
cols=['who','pclass','embarked','sex','sibsp','parch']
n_rows=2
n_cols=3
#The subplot grid and figure size of each graph
fig,axs=plt.subplots(n_rows,n_cols,figsize=(n_cols*3.2,n_rows*3.2))
for r in range(0,n_rows):
  for c in range(0,n_cols):
    i=r*n_cols+c     #index to go though the number of columns
    ax=axs[r][c]   #show where to position each subplot
    sns.countplot(titanic[cols[i]],hue=titanic['survived'],ax=ax)
    ax.set_title(cols[i])
    ax.legend(title='survived',loc='upper right')
plt.tight_layout()

"""From above we can say that 
1)Who=Survival rate for the childrens and womens were far greatter than men- so they first saved weakers of the section         
2)PCLASS-The 1st class passengers were mostly saved when compared to the 3rd class passengers- They were discriminating while selecting who will survive
3)EMBARKED- The more people were from the southhampton but there survival rate was lower compared to the passengers from the Cherbourgh
4)SEX= female survival rate was more compared to the male survival rate and hence we can say female were given priority while rescuing 
5)Siblings- big families were less in number compared to the lone travelers and family with one siblings had little effect on survival( though its more)
6)Parch=Parent or child chart shows that if you are lone traveller your chances of survival are very less
"""

#look at survival rate by sex
titanic.groupby('sex')[['survived']].mean()

"""Chances of survival for females are quite high compared to males


"""

#look at survival rate by sex and class
titanic.pivot_table('survived',index='sex',columns='class')

"""First class females had the highest survival chances

"""

#look at survival rate by sex and class visuallly 
titanic.pivot_table('survived',index='sex',columns='class').plot()

#plot the survivall rate of each class
sns.barplot(x='class',y='survived',data=titanic)

#survival arte by sex ,age and class
age=pd.cut(titanic['age'],[0,18,35,80])
titanic.pivot_table('survived',['sex',age],'class')

#Plot the prices paid by each class
plt.scatter(titanic['fare'],titanic['class'],color='purple',label='Passenger paid')
plt.ylabel('class')
plt.xlabel('Price/fare')
plt.title('Price of each Class')
plt.legend()
plt.show()

#count the empty values in each columns
titanic.isna().sum()

titanic.isna().mean()

#look at counts
for val in titanic:
  print(titanic[val].value_counts())
  print()

#drop the repited columns ,deck is removed because it has to mnay missing values and that cant not be replaced so we need to remove it
titanic=titanic.drop(['deck','embark_town','alive','class','who','alone','adult_male'],axis=1)
#remove the rows with missing values
titanic=titanic.dropna(subset=['embarked','age'])

#count new no of rows and columns
titanic.shape

#look at the data types
titanic.dtypes

#print unique values in the columns
print(titanic['sex'].unique())
print(titanic['embarked'].unique())

#To deal with the Catogorical variables
from sklearn.preprocessing import LabelEncoder
labelencoder=LabelEncoder()
titanic.iloc[:,7]=labelencoder.fit_transform(titanic.iloc[:,7].values)
titanic.iloc[:,2]=labelencoder.fit_transform(titanic.iloc[:,2].values)

#print unique values in the columns
print(titanic['sex'].unique())
print(titanic['embarked'].unique())

titanic.dtypes

#split the data independant X and depndant Y variables
X= titanic.iloc[:,1:8].values
Y= titanic.iloc[:,0].values

#Split the dataset into 80% tarining 20% testing 
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)

#scale the data
from sklearn.preprocessing import StandardScaler  
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.fit_transform(X_test)

#Create the function with many machine learning models
def models(X_train,Y_train):
  
  #Use Logistic regression
  from sklearn.linear_model import LogisticRegression
  log=LogisticRegression(random_state=0)
  log.fit(X_train,Y_train)

  #use KNeighbors
  from sklearn.neighbors import KNeighborsClassifier
  knn=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)
  knn.fit(X_train,Y_train)

  #use support vector classifier(linear)
  from sklearn.svm import SVC
  scv_lin=SVC(kernel='linear',random_state=0)
  scv_lin.fit(X_train,Y_train)

  #use the (RBF kernel)SVC
  from sklearn.svm import SVC
  svc_rbf=SVC(kernel='rbf',random_state=0)
  svc_rbf.fit(X_train,Y_train)

  #use gaussianNB
  from sklearn.naive_bayes import GaussianNB
  gauss=GaussianNB()
  gauss.fit(X_train,Y_train)

  #use Decision tree
  from sklearn.tree import DecisionTreeClassifier
  tree=DecisionTreeClassifier(criterion='entropy',random_state=0)
  tree.fit(X_train,Y_train)

  #use random forest classifier
  from sklearn.ensemble import RandomForestClassifier
  Forest=RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)
  Forest.fit(X_train,Y_train)

  #print traning accuracy for the each model 
  print('[0] Logistic regression Training Accuracy',log.score(X_train,Y_train))
  print('[1] KNeighbors Training Accuracy',knn.score(X_train,Y_train))
  print('[2] SVC linear Training Accuracy',scv_lin.score(X_train,Y_train))
  print('[3] SVC nonLinear_RBF  Training Accuracy',svc_rbf.score(X_train,Y_train))
  print('[4] Gaussian NB  Training Accuracy',gauss.score(X_train,Y_train))
  print('[5] Decision_tree Training Accuracy',tree.score(X_train,Y_train))
  print('[6] Random_forest regression Training Accuracy',Forest.score(X_train,Y_train))

  return log, knn, scv_lin, svc_rbf, gauss,tree,Forest

model=models(X_train,Y_train)

"""Decision_tree Training Accuracy 0.9929701230228472 most accurate"""

#Show confusion matrix and accuracy for all of the models on the test data
from sklearn.metrics import confusion_matrix
for i in range(len(model)):
  cm=confusion_matrix(Y_test,model[i].predict(X_test))
  #extraxt TN ,FP,FN, TP
  TN ,FP,FN, TP= confusion_matrix(Y_test,model[i].predict(X_test)).ravel()
  test_score=(TP+TN)/(TP+TN+FN+FP)
  print(cm)
  print('Model[{}] testing accuracy = {} '.format(i,test_score))

#get the feature importances
forest=model[6]
importances=pd.DataFrame({'feature':titanic.iloc[:,1:8].columns,'importance':np.round(forest.feature_importances_, 3)})
importances=importances.sort_values('importance',ascending=False).set_index('feature')
importances

#get the feature importances
Decision_re=model[5]
importances_5=pd.DataFrame({'feature':titanic.iloc[:,1:8].columns,'importance':np.round(Decision_re.feature_importances_, 3)})
importances_5=importances_5.sort_values('importance',ascending=False).set_index('feature')
importances_5

#Visualize the importances
importances.plot.bar()

importances_5.plot.bar()

"""From above both figures we can say that the Age and Fare both are important feature which influence the survival the most followed by the sex 

"""

#print the prediction of the random forest classifier
pred=model[6].predict(X_test)
print(pred)
print()
#print actual values
print(Y_test)

my_survival=[[1,0,35,1,0,503.1,2]]
#scaling the prediction
from sklearn.preprocessing import StandardScaler
#sc=StandardScaler()
my_survival_scaled=sc.fit_transform(my_survival)
#print prrediction of my survival using the random forest classifier
pred=model[6].predict(my_survival_scaled)
print(pred)

if pred==0:
  print("Oh No ! You did not make it.")
else:
  print("Nice! you made it.")

