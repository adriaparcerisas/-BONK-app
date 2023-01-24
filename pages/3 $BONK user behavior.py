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


st.title('$BONK user behavior')


# In[3]:


st.markdown('The user behavior on the major of the blockchains are different. The same occurs with the holders of any asset over an entire ecosystem. In this section we are gonna analyze the distribution of $BONK holders and its activity, as well as some other trends.')


# In[4]:


sql = f"""
--credits to cryptoicicle
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
),
start_dates as (
  select 
    address,
    min(date) as start_date
  from wallets 
  where daily_balance > 0
  group by 1
),
end_dates as (
  select 
    address,
    max(date) as end_date
  from wallets 
  where daily_balance < 0
  group by 1
),
days_held as (
select 
  s.address,
  iff(e.address <> null, datediff('day', s.start_date, e.end_date), datediff('day', s.start_date, CURRENT_DATE)) as holding_days
from start_dates s
	left join end_dates e on s.address = e.address
) 
select avg(holding_days) as avg_holding_days
  from days_held
"""

sql2 = f"""
--credits to cryptoicicle
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
),
start_dates as (
  select 
    address,
    min(date) as start_date
  from wallets 
  where daily_balance > 0
  group by 1
),
end_dates as (
  select 
    address,
    max(date) as end_date
  from wallets 
  where daily_balance < 0
  group by 1
),
days_held as (
select 
  s.address,
  iff(e.address <> null, datediff('day', s.start_date, e.end_date), datediff('day', s.start_date, CURRENT_DATE)) as holding_days
from start_dates s
	left join end_dates e on s.address = e.address
) 
select 
    holding_days,
    count(distinct address) as wallets
  from days_held
group by 1 order by 1 asc 
"""


# In[5]:


st.experimental_memo(ttl=21600)
@st.cache
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[8]:


st.metric('Average time holders are holding $BONK', df['avg_holding_days'][0])

import plotly.graph_objects as go

fig2 = go.Figure([go.Bar(x=df2['holding_days'], y=df2['wallets'],marker_color=px.colors.qualitative.Vivid)])
fig2.update_layout(
    title='Distribution of wallets by $BONK holding days',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


# In[9]:


sql = f"""
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
)
SELECT
case when daily_balance<1000000 then 'A. <1M $BONK'
  when daily_balance between 1000000 and 10000000 then 'B. Between 1-10M $BONK'
  when daily_balance between 10000000 and 100000000 then 'C. Between 10-100M $BONK'
  when daily_balance between 100000000 and 1000000000 then 'D. Between 100M-1T $BONK'
  when daily_balance between 1000000000 and 10000000000 then 'E. Between 1T-10T $BONK'
  when daily_balance between 10000000000 and 100000000000 then 'F. Between 10T-100T $BONK'
  else 'G. >100T $BONK' end as balance,
  count(distinct address) as counts
from wallets
where date=CURRENT_DATE-1
  group by 1
order by 1
"""

sql2="""

--SQL Credit https://app.flipsidecrypto.com/velocity/queries/6bbb795c-9612-4bf2-9320-09179c6fa75c

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
)
SELECT
address,
daily_balance as current_balance
from wallets
where date=CURRENT_DATE-1
order by 2 desc limit 10
"""


# In[10]:


results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[12]:


import plotly.graph_objects as go
fig1 = go.Figure([go.Bar(x=df['balance'], y=df['counts'],marker_color=px.colors.qualitative.Plotly)])
fig1.update_layout(
    title='Distribution of $BONK holders by balances',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig2 = go.Figure([go.Bar(x=df2['address'], y=df2['current_balance'],marker_color=px.colors.qualitative.Vivid)])
fig2.update_layout(
    title='Top 10 holders by current $BONK balance',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


# In[17]:


sql="""
--credits to cryptoicicle
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
holders as (
    select 
    date,
    address,
    sum(n_tokens) as daily_change,
    sum(daily_change) over (partition by address order by date asc rows between unbounded preceding and current row) as daily_balance
  from transfers
  group by 1,2
  qualify daily_balance > 0
), daily_activity as (
  select
  date(BLOCK_TIMESTAMP) as dt,
  'NFTs' as activity,
  count(tx_id) as no_txn,
  purchaser as wallet
  from solana.core.fact_nft_sales
  where SUCCEEDED='TRUE'
  and BLOCK_TIMESTAMP>='2022-12-24'
  group by 1, wallet
  union all 
  select
  date(BLOCK_TIMESTAMP) as dt,
  'NFTs' as activity,
  count(tx_id) as no_txn,
  purchaser as wallet
  from solana.core.fact_nft_mints
  where SUCCEEDED='TRUE'
  and BLOCK_TIMESTAMP>='2022-12-24'
  group by 1, wallet
  union all 
  select
  date(e.BLOCK_TIMESTAMP) as dt,
  'stake' as activity,
  count(e.tx_id) as no_txn,
  t.signers[0] as wallet
  from solana.core.fact_events e
  join solana.core.fact_transactions t on e.tx_id = t.tx_id and e.block_timestamp >='2022-12-24' and t.block_timestamp >='2022-12-24'
  where EVENT_TYPE in ('delegate')
  group by 1, wallet
  union all 
  select
  date(e.BLOCK_TIMESTAMP) as dt,
  'unstake' as activity,
  count(e.tx_id) as no_txn,
  t.signers[0] as wallet
  from solana.core.fact_events e
  join solana.core.fact_transactions t on e.tx_id = t.tx_id and e.block_timestamp >='2022-12-24' and t.block_timestamp >='2022-12-24'
  where EVENT_TYPE='withdraw'
  group by 1, wallet
  
    union all 
    
  select
  date(e.BLOCK_TIMESTAMP) as dt,
  'Add liquidity' as activity,
  count(e.tx_id) as no_txn,
  t.signers[0] as wallet
  from solana.core.fact_events e
  join solana.core.fact_transactions t on e.tx_id = t.tx_id and e.block_timestamp >='2022-12-24' and t.block_timestamp >='2022-12-24'
  where EVENT_TYPE='mintTo'
  group by 1, wallet
  
  union all 
  
  select
  date(e.BLOCK_TIMESTAMP) as dt,
  'Remove liquidity' as activity,
  count(e.tx_id) as no_txn,
  t.signers[0] as wallet
  from solana.core.fact_events e
  join solana.core.fact_transactions t on e.tx_id = t.tx_id and e.block_timestamp >='2022-12-24' and t.block_timestamp >='2022-12-24'
  where EVENT_TYPE='burn'
  group by 1, wallet
  ),
  fin as (
select 
  d.dt as date,
  d.activity,
  iff(h.address = null, 'non-holder', 'holder') as type,
  sum(no_txn) as transactions
  from daily_activity d
  join holders h on d.wallet = h.address and d.dt = h.date
  group by 1, 2, 3
  )
  select date,activity,transactions,sum(transactions) over (partition by activity order by date) as cum_transactions from fin where type='holder'
  order by 1 asc 
"""


# In[18]:


results = compute(sql)
df = pd.DataFrame(results.records)
df.info()


# In[19]:


fig3 = px.line(df, x="date", y="transactions", color="activity", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Daily $BONK transactions by type',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

fig3 = px.area(df, x="date", y="cum_transactions", color="activity", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Total $BONK transactions by type',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:




