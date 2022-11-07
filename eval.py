import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 6})
import numpy

df = pd.read_csv(r'allomorphy_ex.csv')


mismatch = df.loc[df['ex2_allomorph'] == 'mismatch']

mis_decomposed = mismatch.loc[mismatch['frequency'] == 'simple']

#mis_heit_decomposed = mis_decomposed.loc[mis_decomposed['ex2_order'] == 'heit first']

rating = mis_decomposed['Rating_in_relation_to_mean'].to_numpy().tolist()

item = mis_decomposed['condition'].to_numpy().tolist()

participant = mis_decomposed['variable'].to_numpy().tolist()

plt.scatter(item, rating)
plt.show()
