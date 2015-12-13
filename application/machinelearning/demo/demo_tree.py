# coding=UTF-8

from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.externals.six import StringIO
from graphviz import Source

iris = load_iris()
clf = tree.DecisionTreeClassifier()
print(iris.data)
print(iris.target)
clf = clf.fit(iris.data, iris.target)
dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data)
print((dot_data.getvalue()))
'''

src = Source(dot_data.getvalue())
print(type(src))
src.render('test-output/holy-grenade.gv', view=True)'''

'''
fr = open('d:/data/lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age','prescript','astigmatic','tearRate']
lenses_data = [item[0:4] for item in lenses]
lenses_target = [item[4] for item in lenses]
print(lenses_data)
print(lenses_target)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(lenses_data, lenses_target)'''

