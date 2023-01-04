#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[2]:


st.title('$BONK holders')


# In[3]:


st.markdown('The holders are one of the major characteristics to take into account for all of the current blockchain projects because of it talks about how social is a token and how big is the impact of it to the society. The same occurs about how active are these holders over the entire ecosystem. In this section we are gonna analyze the current amount of $BONK holders as well as its evolution. As well we will consider if they are active or not on Solana.') 


# In[11]:


sql = f"""
-- credits to cryptoicicle
with airdrop_txns as (
  select distinct tx_to as address, * from 
  solana.core.fact_transfers
  where tx_from in (
  '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw',
  '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p')
  and mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and block_timestamp >= '2022-12-24 00:00:00.000'
),
transfers_from as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_from as address,
    sum(tx.amount) * -1 as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24 00:00:00.000'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers_to as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_to as address,
    sum(tx.amount) as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24 00:00:00.000'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers as (  
(select *  from transfers_from )
  union (select *  from transfers_to)
),
wallets as (
    select 
    date,
    address,
    sum(n_tokens) as daily_change,
    sum(daily_change) over (partition by address order by date asc rows between unbounded preceding and current row) as daily_balance
  from transfers
  group by 1,2
  qualify daily_balance > 0
)
  
select 
  count(distinct address) as holders,
  avg(daily_balance) as avg_balance
  from wallets where date=CURRENT_DATE-1
"""

sql2 = f"""
-- credits to cryptoicicle
with airdrop_txns as (
  select distinct tx_to as address, * from 
  solana.core.fact_transfers
  where tx_from in (
  '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw',
  '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p')
  and mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and block_timestamp >= '2022-12-24'
),
transfers_from as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_from as address,
    sum(tx.amount) * -1 as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers_to as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_to as address,
    sum(tx.amount) as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers as (  
(select *  from transfers_from )
  union (select *  from transfers_to)
),
wallets as (
    select 
    date,
    address,
    sum(n_tokens) as daily_change,
    sum(daily_change) over (partition by address order by date asc rows between unbounded preceding and current row) as daily_balance
  from transfers
  group by 1,2
  qualify daily_balance > 0
),
active_wallets as (
	select 
    distinct signers[0] as wallet
  from solana.core.fact_transactions
    where block_timestamp >= CURRENT_DATE - 90
)
select 
  count(distinct address) as n_holders
  from wallets
  where address in (select wallet from active_wallets) and date=CURRENT_DATE-1
"""

sql3="""
with maintable as (
select block_timestamp::date as date,
tx_from as User1,
sum (amount)*-1 as Volume
from solana.core.fact_transfers
where mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
group by 1,2

union ALL

select block_timestamp::Date as date,
tx_to as User1,
sum (amount) as Volume
from solana.core.fact_transfers
where mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
group by 1,2),

finaltable as (
select date,
User1,
sum (Volume) as Net_Volume,
sum (Net_Volume) over (partition by User1 order by date rows between unbounded preceding and current row) as User_Net_Volume
from maintable
group by 1,2)
  
select count (distinct User1) as Holders_Count,
avg (Net_Volume) as Average_Held_Bonk_By_User,
avg (user_net_volume) as Average_Daily_Held_BONK
from finaltable
where User_Net_Volume > 0
and date >= '2022-12-24'
"""


# In[12]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()


# In[16]:


import math

millnames = ['',' k',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

st.markdown(""" <style> div.css-12w0qpk.e1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid;
 padding: 10px 5px 5px 5px;
 border-radius: 10px;
 color: #ffc300;
 box-shadow: 10px;
}
div.css-1r6slb0.e1tzin5v2{
 background-color: #f5f5f5;
 border: 2px solid; /* #900c3f */
 border-radius: 10px;
 padding: 10px 5px 5px 5px;
 color: green;
}
div.css-50ug3q.e16fv1kl3{
 font-weight: 900;
} 
</style> """, unsafe_allow_html=True)

col1,col2,col3 =st.columns(3)
with col1:
    st.metric('Number of $BONK holders', millify(df['holders'][0]))
col2.metric('Number of $BONK active holders', millify(df2['n_holders'][0]))
col3.metric('Average volume of $BONK holded', millify(df['avg_balance'][0]))

col1,col2 =st.columns(2)
with col1:
    st.metric('Original $BONK holders', millify(df3['holders_count'][0]))
col2.metric('Average held by original holders', millify(df3['average_held_bonk_by_user'][0]))


# In[8]:


sql = f"""
-- credits to cryptoicicle
with airdrop_txns as (
  select distinct tx_to as address, * from 
  solana.core.fact_transfers
  where tx_from in (
  '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw',
  '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p')
  and mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and block_timestamp >= '2022-12-24 00:00:00.000'
),
transfers_from as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_from as address,
    sum(tx.amount) * -1 as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24 00:00:00.000'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers_to as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_to as address,
    sum(tx.amount) as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24 00:00:00.000'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers as (  
(select *  from transfers_from )
  union (select *  from transfers_to)
),
wallets as (
    select 
    date,
    address,
    sum(n_tokens) as daily_change,
    sum(daily_change) over (partition by address order by date asc rows between unbounded preceding and current row) as daily_balance
  from transfers
  group by 1,2
  qualify daily_balance > 0
)
  
select 
  date, 
  count(distinct address) as holders,
  avg(daily_balance) as avg_balance
  from wallets
group by 1
order by date asc
"""

sql2="""
with airdrop_txns as (
  select distinct tx_to as address, * from 
  solana.core.fact_transfers
  where tx_from in (
  '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw',
  '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p')
  and mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and block_timestamp >= '2022-12-24'
),
transfers_from as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_from as address,
    sum(tx.amount) * -1 as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers_to as (
  select
    date_trunc('day',block_timestamp) as date,
  	tx_id,
  	tx.tx_to as address,
    sum(tx.amount) as n_tokens
  from solana.core.fact_transfers tx
  where tx.block_timestamp >= '2022-12-24'
  and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and address not in (
  	'9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw', -- 'bonk airdrop address'
    '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p', -- 'bonk new airdrop address'
    'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez', -- 'orca bonk-sol pool'
    '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY', -- 'orca bonk-usdc pool'
    '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz', -- 'dex bonk-usdc pool'
    'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK', -- 'bonk dao wallet'
    '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD', -- 'bonk team wallet'
    '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' -- 'bonk marketing wallet'
  )
  group by 1,2,3
),
transfers as (  
(select *  from transfers_from )
  union (select *  from transfers_to)
),
wallets as (
    select 
    date,
    address,
    sum(n_tokens) as daily_change,
    sum(daily_change) over (partition by address order by date asc rows between unbounded preceding and current row) as daily_balance
  from transfers
  group by 1,2
  qualify daily_balance > 0
),
active_wallets as (
	select 
    distinct signers[0] as wallet
  from solana.core.fact_transactions
    where block_timestamp >= CURRENT_DATE - 90
),
  active_users as (
select
  date,
  count(distinct address) as n_holders
  from wallets
  where address in (select wallet from active_wallets)
group by 1
order by 1
  ),
all_users as (
  select
  date,
  count(distinct address) as n_holders
  from wallets
group by 1
order by 1
)
SELECT
ifnull(x.date,y.date) as date,
ifnull(x.n_holders,0) as active_holders,
ifnull(y.n_holders,0) as total_holders,
(active_holders/total_holders)*100 as pcg_of_active_holders
from active_users x
join all_users y on x.date=y.DATE
order by 1 asc 
"""


# In[9]:


results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[10]:


import altair as alt
base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='darkgreen').encode(y=alt.Y('avg_balance:Q', axis=alt.Axis(grid=True)))
bar=base.mark_bar(color='green',opacity=0.5).encode(y='holders:Q')

st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily $BONK holders and average balances',width=600))


import altair as alt
base=alt.Chart(df2).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='darkblue').encode(y=alt.Y('pcg_of_active_holders:Q', axis=alt.Axis(grid=True)))
bar=base.mark_bar(color='blue',opacity=0.5).encode(y='active_holders:Q')

st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily active $BONK holders',width=600))


# In[ ]:




