import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

orientation_order = ['horizontal', 'vertical', 'square']
labs_cap = ['Horizontal', 'Vertical', 'Square']

english_df = pd.read_csv('all_english_dims.csv')
eng_ori_count = english_df['orientation'].value_counts().reindex(orientation_order, fill_value = 0)
# orientation     n = 339
# horizontal    231, 68.14%
# vertical       90, 26.55%
# square         17, 5.01%

eng_ori_count.plot(kind = 'bar')
plt.xlabel('Orientation Type')
plt.ylabel('Count')
plt.title('Distribution of Orientations - English')
plt.xticks(ticks = range(len(labs_cap)), labels = labs_cap, rotation = 0)
plt.show()

hindi_df = pd.read_csv('all_hindi_dims.csv')
hin_ori_count = hindi_df['orientation'].value_counts().reindex(orientation_order, fill_value = 0)

# orientation     n = 399
# horizontal    122, 30.58%
# vertical      259, 64.91%
# square         17, 4.26%

hin_ori_count.plot(kind = 'bar')
plt.xlabel('Orientation Type')
plt.ylabel('Count')
plt.title('Distribution of Orientations - Hindi')
plt.xticks(ticks = range(len(labs_cap)), labels = labs_cap, rotation = 0)
plt.show()