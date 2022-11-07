import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_csv(r'steffi_5.csv')

df_long = pd.melt(df, id_vars=["question", "condition"])
df_long.dropna(subset = ["value"], inplace=True)

df_withouthmonths = df_long[df_long["condition"] != "Month"]
df_months = df_long.loc[df_long['condition'] == "Month"]
df_reshaped = df_months.drop(columns=['question', 'condition'])
with_month = df_reshaped.rename(columns={"value": "month"})
all_judgments = pd.merge(df_withouthmonths, with_month, on="variable")



only_numbers = all_judgments[all_judgments.value.str.isnumeric()]
only_numbers_reshaped = only_numbers.drop(columns=['question', 'condition', "month"])


df_2 = pd.read_csv(r'participant_mean.csv', delimiter=";", decimal=",")
df_2 = df_2.rename(columns={"Zeilenbeschriftungen": "variable"})

new_df = pd.merge(all_judgments, df_2, on="variable")
new_df = new_df[new_df.value.str.isnumeric()]
new_df["value"] = new_df["value"].astype(float)
new_df["Mittelwert von value"] = new_df["Mittelwert von value"].astype(float)

new_df["Rating_in_relation_to_mean"] = new_df["value"] - new_df["Mittelwert von value"]

#exclude participants who failed Deutsch_test_1

list_of_non_butzemann = ["participant_91", "participant_92", "participant_102"]
new_df = new_df.loc[-new_df["variable"].isin(list_of_non_butzemann)]

butzemann = all_judgments.loc[all_judgments['condition'] == "Deutsch_test_1"]
nicht_butzemann = butzemann.loc[butzemann["value"] != "Butzemann"]

new_df.to_csv(r'all_judgments_with_mean.csv', index = False)

#simplify condition, one condition = column frequency simple vs. complex or NaN

simple = new_df.loc[new_df['condition'].str.contains('1.|2.|3.')]

keys = simple['condition'].values.tolist()
s_frequencies = {}
for key in keys:
    s_frequencies[key] = 'simple'

complex = new_df.loc[new_df['condition'].str.contains('4.|5.|6.')]

keys_2 = complex['condition'].values.tolist()
c_frequencies = {}
for k in keys_2:
    c_frequencies[k] = 'complex'

frequencies = {**s_frequencies, **c_frequencies}
#print(frequencies)

f_df = pd.DataFrame(list(frequencies.items()), columns = ['condition', 'frequency'])

#print(f_df)

result_df = pd.merge(new_df, f_df, how="outer", on=["condition"])

#print(result_df)

#result_df.to_csv('freq.csv', na_rep='NaN')

#simplify condition umlaut

umlaut = new_df.loc[new_df['condition'].str.contains('U')]

keys_3 = umlaut['condition'].values.tolist()
umlaut_dic = {}
for k3 in keys_3:
    umlaut_dic[k3] = 'umlaut'

no_umlaut = new_df.loc[new_df['condition'].str.contains('L')]

keys_4 = no_umlaut['condition'].values.tolist()
no_umlaut_dic = {}
for k4 in keys_4:
    no_umlaut_dic[k4] = 'no umlaut'

mix_umlaut = new_df.loc[new_df['condition'].str.contains('Mix')]

keys_5 = mix_umlaut['condition'].values.tolist()
mix_umlaut_dic = {}
for k5 in keys_5:
    mix_umlaut_dic[k5] = 'umlaut mix'

ex1 = {**umlaut_dic, **no_umlaut_dic, **mix_umlaut_dic}

umlaut_df = pd.DataFrame(list(ex1.items()), columns = ['condition', 'ex1_umlaut'])

#print(f_df)

result_umlaut_df = pd.merge(result_df, umlaut_df, how="outer", on=["condition"])

#print(result_umlaut_df)

#result_umlaut_df.to_csv('freq.csv', na_rep='NaN')

#simplify condition allomorphy

heit = new_df.loc[new_df['condition'].str.contains('H')]

keys_8 = heit['condition'].values.tolist()
heit_dic = {}
for k8 in keys_8:
    heit_dic[k8] = 'heit'

keit = new_df.loc[new_df['condition'].str.contains('K')]

keys_9 = keit['condition'].values.tolist()
keit_dic = {}
for k9 in keys_9:
    keit_dic[k9] = 'keit'

mismatch = new_df.loc[new_df['condition'].str.contains('Mis')]

#mismatch.to_csv('mismatch.csv')

keys_10 = mismatch['condition'].values.tolist()
mismatch_dic = {}
for k10 in keys_10:
    mismatch_dic[k10] = 'mismatch'

ex2 = {**heit_dic, **keit_dic, **mismatch_dic}

allomorphy_df = pd.DataFrame(list(ex2.items()), columns = ['condition', 'ex2_allomorph'])

result2_df = pd.merge(result_umlaut_df, allomorphy_df, how="outer", on=["condition"])

#print(result_umlaut_df)

##### LAST OUTPUT

#result2_df.to_csv('freq.csv', na_rep='NaN')








#simplify condition umlaut order str.contains can't process single quote...

umlaut_first = result2_df.loc[result2_df['condition'].str.contains('Mix 3.')]

#print(umlaut_first)
#umlaut_first.to_csv('umlaut_first.csv')


keys_6 = umlaut_first['condition'].values.tolist()
umlaut_first_dic = {}
for k6 in keys_6:
    umlaut_first_dic[k6] = 'umlaut first'


umlaut_second = result2_df.loc[result2_df['condition'].str.contains("Mix 3\'.")]

keys_7 = umlaut_second['condition'].values.tolist()
umlaut_second_dic = {}
for k7 in keys_7:
    umlaut_second_dic[k7] = 'umlaut second'

#print(umlaut_second_dic)

for k_d1 in umlaut_first_dic:
    if k_d1 in umlaut_second_dic:
        umlaut_first_dic[k_d1] = umlaut_second_dic[k_d1]

#print(umlaut_first_dic)


ex1_order_df = pd.DataFrame(list(umlaut_first_dic.items()), columns = ['condition','ex1_order'])

#print(ex1_order_df)

result_umlaut_order_df = pd.merge(ex1_order_df, result2_df, how="outer", on=["condition"])

#print(result_umlaut_order_df)

#result_umlaut_order_df.to_csv('freq.csv', na_rep='NaN')


#simplify condition allomorph order

heit_first = result_umlaut_order_df.loc[result_umlaut_order_df['condition'].str.contains('Mis 3.')]


keys_11 = heit_first['condition'].values.tolist()
heit_first_dic = {}
for k11 in keys_11:
    heit_first_dic[k11] = 'heit first'


keit_first = result_umlaut_order_df.loc[result_umlaut_order_df['condition'].str.contains("Mis 3\'.")]

keys_12 = keit_first['condition'].values.tolist()
keit_first_dic = {}
for k12 in keys_12:
    keit_first_dic[k12] = 'keit first'

#print(umlaut_second_dic)

for h_d1 in heit_first_dic:
    if h_d1 in keit_first_dic:
        heit_first_dic[h_d1] = keit_first_dic[h_d1]



ex2_order_df = pd.DataFrame(list(heit_first_dic.items()), columns = ['condition','ex2_order'])


result_ex2_order_df = pd.merge(ex2_order_df, result_umlaut_order_df, how="outer", on=["condition"])

#print(result_ex2_order_df)

result_ex2_order_df.to_csv('freq.csv', na_rep='NaN')


fillers = result_ex2_order_df.loc[result_ex2_order_df['condition'].str.contains("F")]

fillers.to_csv('fillers.csv', na_rep='NaN')

ohne_fillers = result_ex2_order_df.loc[result_ex2_order_df['condition'] != "F"]
ohne_fillers = ohne_fillers.loc[result_ex2_order_df['condition'] != "Deutsch_test_2"]
ohne_fillers = ohne_fillers.loc[result_ex2_order_df['condition'] != "Deutsch_test_3"]
ohne_fillers = ohne_fillers.set_index("condition")

ohne_fillers.to_csv('test.csv', na_rep='NaN')


#stems and affixes
items_df = pd.read_csv(r'items.csv')



item = items_df['item'].to_numpy().tolist()

first = []
second = []

for i in item:
    match = re.search("[A-Za-zäüöÄÜÖß]+- (und|noch)", i).group(0)
    #print(match)
    match = match.split()
    match = match[0]
    match = match.strip('-')
    first.append(match)




for it in item:
    sec_match = re.search("(weder.+noch|- und)\s[A-Za-zäüöÄÜÖß]+", it).group(0)
    sec_match = sec_match.split()
    sec_match = sec_match[-1]
    #sec_match = sec_match.strip('- und ')
    #print(sec_match)
    second.append(sec_match)

items_df['first'] = first
items_df['second'] = second
items_df = items_df.set_index("condition")
print(items_df)
items_df.to_csv('split_items.csv')



ohne_fillers_new = pd.merge(ohne_fillers, items_df, how="outer", on=["condition"])
#print(ohne_fillers)
#ohne_fillers_new = ohne_fillers_new.groupby(['question', 'variable']).first()
ohne_fillers_new = ohne_fillers_new.drop_duplicates()

print(ohne_fillers_new)

################################################

freq_df = pd.read_csv(r'frequencies_de.csv')

freq = freq_df['absolut'].to_numpy().tolist()
words = freq_df['second'].to_numpy().tolist()
seconds = ohne_fillers_new['second'].to_numpy().tolist()
#firsts = ohne_fillers_new['first'].to_numpy().tolist()

ohne_fillers_new.to_csv('ohne_fillers.csv', na_rep='NaN')


word_list = set(words).intersection(seconds)

print(word_list)

freq_df = freq_df.loc[freq_df['second'].isin(word_list)]

print(freq_df)

####################### get the frequency of the words and add them to the df
abs_freq = pd.merge(ohne_fillers_new, freq_df, how="inner", on=["second"])

print(abs_freq)

allomorpy_ex = ohne_fillers_new.loc[ohne_fillers_new['ex2_allomorph'].notna()]

allomorpy_ex = allomorpy_ex.drop(columns=['ex1_umlaut', 'ex1_order'])
#print(allomorpy_ex)
allomorpy_ex.to_csv('allomorphy_ex.csv', na_rep='NaN')

umlaut_ex = ohne_fillers_new.loc[ohne_fillers_new['ex1_umlaut'].notna()]
umlaut_ex = umlaut_ex.drop(columns=['ex2_allomorph', 'ex2_order'])
#print(umlaut_ex)
umlaut_ex.to_csv('umlaut_ex.csv', na_rep='NaN')



