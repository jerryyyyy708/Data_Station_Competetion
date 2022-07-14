#V1: only use product counts
import pandas as pd

def create_dataframe(products):
    df_head=[str(i)+'_count' for i in range(products)]
    df_tail=[str(i)+'_buy' for i in range(products)]
    df_head.append('customer')
    df_head.append('age_group')
    df_head+=df_tail
    df=pd.DataFrame(columns=df_head)
    return df

mode = 'product' #department, use add parse
df=pd.read_csv('encoded.csv')
df=df.drop(columns=['Unnamed: 0'])

customers= df['customer'].unique().tolist()
products = df[mode].unique().tolist()
new_dataframe=create_dataframe(len(products))

for i in customers:
    customer_df = df.loc[df.customer == i]
    values = customer_df[mode].value_counts().keys().tolist()
    counts = customer_df[mode].value_counts().tolist()
    orders = customer_df['id'].unique().tolist()

    tempdf = customer_df.loc[customer_df.id != orders[-1]]
    target = customer_df.loc[customer_df.id == orders[-1]]

    target_orders = target[mode].unique().tolist()

    new_row = [0] * len(products)
    new_tail = [0] * len(products)
    new_row += [i,tempdf.iloc[0]['age_group']]
    new_row += new_tail
    for j , k in zip(values, counts):
        new_row[int(j)] = k
    for j in target_orders:
        new_row[len(products)+2+int(j)] = 1 #if add column 2 need to change
    new_dataframe.loc[len(new_dataframe)] = new_row

new_dataframe.to_csv("preprocessed_v1.csv")
