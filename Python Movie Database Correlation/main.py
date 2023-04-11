# import pandas
# import seaborn
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy
# from matplotlib.pyplot import figure
# plt.style.use('ggplot')
#
# # %matplotlib inline
# plt.show()
# matplotlib.rcParams['figure.figsize'] = (12,8)
#
# df = pandas.read_csv('movies.csv')
#
# for col in df.columns:
#     pct_missing = numpy.mean(df[col].isnull())
#     print('{} - {}%'.format(col, pct_missing))
#
# print(df.dtypes)
#
# df.budget = df.budget.astype('int64')


df = 10
df_num = df
df_num += 5

print(df, df_num)