from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import rpy2.robjects.packages as rpackages
from rpy2.robjects.packages import importr, data
from rpy2.robjects import FloatVector
from rpy2 import robjects
import pandas as pd



pandas2ri.activate()

'''

A good resource is https://rpy2.readthedocs.io/en/version_2.8.x/introduction.html

'''


#importing R package custom.analytics and replacing . with _ in 
#package names to ensure no conflicts
d = {'package.dependencies': 'package_dot_dependencies',
     'package_dependencies': 'package_uscore_dependencies'}
# import R's "base" package
base = importr('base', robject_translations = d)

# import R's "utils" package
utils = importr('utils', robject_translations = d)


# select a mirror for R packages
utils.chooseCRANmirror(ind=1) # select the first mirror in the list

# R package names
packnames = ('rlang','ggplot2')

# R vector of strings
from rpy2.robjects.vectors import StrVector

# Make a ggplot2
# Selectively install what needs to be install.
# We are fancy, just because we can.
names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    utils.install_packages(StrVector(names_to_install))

print('hexbin is installed? ', rpackages.isinstalled('hexbin'))
print('ggplot2 is installed? ', rpackages.isinstalled('ggplot2'))

ggplot2 = importr('ggplot2', robject_translations = d)

import math, datetime
import rpy2.robjects.lib.ggplot2 as ggplot2

datasets = importr('datasets')

mtcars = data(datasets).fetch('mtcars')['mtcars']

pp = ggplot2.ggplot(mtcars) + \
     ggplot2.aes_string(x='wt', y='mpg', col='factor(cyl)') + \
     ggplot2.geom_point() + \
     ggplot2.geom_smooth(ggplot2.aes_string(group = 'cyl'),
                         method = 'lm')
pp.plot()

# Run a regresison
stats = importr('stats')


ctl = FloatVector([4.17,5.58,5.18,6.11,4.50,4.61,5.17,4.53,5.33,5.14])
trt = FloatVector([4.81,4.17,4.41,3.59,5.87,3.83,6.03,4.89,4.32,4.69])
group = base.gl(2, 10, 20, labels = ["Ctl","Trt"])
weight = ctl + trt

robjects.globalenv["weight"] = weight
robjects.globalenv["group"] = group
lm_D9 = stats.lm("weight ~ group")
print(stats.anova(lm_D9))

# omitting the intercept
lm_D90 = stats.lm("weight ~ group - 1")
print(base.summary(lm_D90))


#saving R object, summary_stats to file
base.saveRDS(base.summary(lm_D90), file="summary_stats.rds")

lm_D90_reload = base.readRDS(file="summary_stats.rds")
print('Reloaded RDS file:\n', lm_D90_reload)


# Create an pandas df
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C':[7,8,9]},
                  index=["one", "two", "three"])
# turn to R dataframe
rdf = pandas2ri.py2ri(df)
print(type(rdf))

# and turn back to pd
df2 = pandas2ri.ri2py(rdf)
print(type(df2))
