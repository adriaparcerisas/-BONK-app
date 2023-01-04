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


st.title('$BONK movements')


# In[28]:


st.markdown('A good way to track where token supply is going on is by analysing some transfers movements and analyzing its flows. For this reason, this final part tracks all about the $BONK transfers. The main metrics to be analyzedd are: ')
st.markdown('BONK price performance vs $SOL')
st.markdown('BONK flows')
st.markdown('BONK transfers')
st.markdown('BONK whales activity')


# In[29]:


sql="""
with table1 as (
select block_timestamp::date as day,
median (swap_to_amount/swap_from_amount) as BONK_price
from solana.fact_swaps
where swap_to_mint in ('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v','Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB') --USDC,USDT 
and swap_from_mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
and swap_to_amount > 0
and swap_from_amount > 0
and succeeded = 'TRUE'
and block_timestamp::date >= '2022-12-24'
group by 1),

table2 as (
select block_timestamp::date as day,
median (swap_to_amount/swap_from_amount) as SOL_price
from solana.fact_swaps
where swap_to_mint in ('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v','Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB') --USDC,USDT 
and swap_from_mint ilike 'So11111111111111111111111111111111111111112'
and swap_to_amount > 0
and swap_from_amount > 0
and succeeded = 'TRUE'
and block_timestamp::date >= '2022-12-24'
group by 1)

select t1.day as date,
BONK_price,
SOL_price
from table1 t1 join table2 t2 on t1.day = t2.day
"""



# In[30]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

import altair as alt
base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='orange').encode(y=alt.Y('BONK_price:Q', axis=alt.Axis(grid=True)))
bar=base.mark_line(color='purple',opacity=0.5).encode(y='SOL_price:Q')

st.altair_chart((bar + line).resolve_scale(y='independent').properties(title='Daily $BONK vs $SOL price evolution',width=600))



# In[15]:


sql = f"""
--credits: https://app.flipsidecrypto.com/velocity/queries/6bbb795c-9612-4bf2-9320-09179c6fa75c

with airdropees as (
  select distinct tx_to as address from 
  solana.core.fact_transfers
  where tx_from in (
  '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw',
  '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p')
  and mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and block_timestamp > '2022-12-24'
)

SELECT
  --date_trunc('day',tx.block_timestamp) as date,
  time_slice(tx.block_timestamp, 12, 'HOUR') as date,
  case when tx.tx_to = '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw' then 'bonk airdrop address'
       when tx.tx_to = '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p' then 'bonk new airdrop address'
       when tx.tx_to = 'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez' then 'orca bonk-sol pool'
       when tx.tx_to = '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY' then 'orca bonk-usdc pool'
       when tx.tx_to = '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz' then 'dex bonk-usdc pool'
       when tx.tx_to = 'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK' then 'bonk dao wallet'
       when tx.tx_to = '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD' then 'bonk team wallet'
       when tx.tx_to = '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' then 'bonk marketing wallet'
  else coalesce(lto.label,'unlabeled') end as to_label,
  coalesce(lto.label_type,'unlabeled') as to_label_type,
  case when tx.tx_to in (select address from airdropees) then 'airdrop recipient'
       else coalesce(lto.label_subtype,'unlabeled user') end as to_label_subtype,
  case when tx.tx_from = '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw' then 'bonk airdrop address'
       when tx.tx_from = '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p' then 'bonk new airdrop address'
       when tx.tx_from = 'BqnpCdDLPV2pFdAaLnVidmn3G93RP2p5oRdGEY2sJGez' then 'orca bonk-sol pool'
       when tx.tx_from = '5P6n5omLbLbP4kaPGL8etqQAHEx2UCkaUyvjLDnwV4EY' then 'orca bonk-usdc pool'
       when tx.tx_from = '2PFvRYt5h88ePdQXBrH3dyFmQqJHTNZYLztE847dHWYz' then 'dex bonk-usdc pool'
       when tx.tx_from = 'DBR2ZUvjZTcgy6R9US64t96pBEZMyr9DPW6G2scrctQK' then 'bonk dao wallet'
       when tx.tx_from = '4CUMsJG7neKqZuuLeoBoMuqufaNBc2wdwQiXnoH4aJcD' then 'bonk team wallet'
       when tx.tx_from = '2yBBKgCwGdVpo192D8WZeAtqyhyP8DkCMnmTLeVYfKtA' then 'bonk marketing wallet'
  else coalesce(lfr.label,'unlabeled') end as from_label,
  coalesce(lfr.label_type,'unlabeled') as from_label_type,
  case when tx.tx_from in (select address from airdropees) then 'airdrop recipient'
  else coalesce(lfr.label_subtype,'unlabeled user') end as from_label_subtype,
  sum(tx.amount) as n_tokens
FROM
solana.core.fact_transfers tx
  left join solana.core.dim_labels lfr on lfr.address = tx.tx_from
  left join solana.core.dim_labels lto on lto.address = tx.tx_to
where tx.block_timestamp > '2022-12-24'
and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
group by 1,2,3,4,5,6,7
"""

sql2 = f"""
--credits: https://app.flipsidecrypto.com/velocity/queries/6bbb795c-9612-4bf2-9320-09179c6fa75c

with airdropees as (
  select distinct tx_to as address from 
  solana.core.fact_transfers
  where tx_from in (
  '9AhKqLR67hwapvG8SA2JFXaCshXc9nALJjpKaHZrsbkw',
  '6JZoszTBzkGsskbheswiS6z2LRGckyFY4SpEGiLZqA9p')
  and mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  and block_timestamp > '2022-12-24'
)
SELECT

  coalesce(lto.label_type,'unlabeled') as to_label_type,
  coalesce(lfr.label_type,'unlabeled') as from_label_type,
  sum(tx.amount) as n_tokens
FROM
solana.core.fact_transfers tx
  left join solana.core.dim_labels lfr on lfr.address = tx.tx_from
  left join solana.core.dim_labels lto on lto.address = tx.tx_to
where tx.block_timestamp > '2022-12-24'
and tx.mint = 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
group by 1,2
"""


# In[16]:


results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[17]:


fig3 = px.area(df, x="date", y="n_tokens", color="from_label_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Daily $BONK tokens transferred from each sector',
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


fig4 = px.area(df, x="date", y="n_tokens", color="to_label_type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig4.update_layout(
    title='Daily $BONK tokens transferred to each sector',
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
col1,col2=st.columns(2)
with col1:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
col2.plotly_chart(fig4, theme="streamlit", use_container_width=True)


# In[18]:


fig3 = px.area(df, x="date", y="n_tokens", color="from_label", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Daily $BONK tokens transferred from each platform',
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


fig4 = px.area(df, x="date", y="n_tokens", color="to_label", color_discrete_sequence=px.colors.qualitative.Plotly)
fig4.update_layout(
    title='Daily $BONK tokens transferred to each platform',
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
col1,col2=st.columns(2)
with col1:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
col2.plotly_chart(fig4, theme="streamlit", use_container_width=True)


# In[22]:


import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["DEX", "CEX", "NFT", "Token", "Unlabeled"],
      color = "blue"
    ),
    link = dict(
      source = [0, 1, 2, 3, 4, 4, 2, 0, 0, 1, 3, 0, 4, 1, 1, 4, 3, 4, 2], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = [1, 0, 0, 4, 3, 2, 4, 2, 4, 3, 3, 3, 1, 4, 1, 0, 0, 4, 3],
      value = [3.106345e+09, 3.106345e+09, 4.027262e+08, 3.246146e+09, 4.426406e+13, 4.777803e+10
              , 6.527745e+10, 1.135914e+09, 7.477750e+13, 5.419399e+10, 3.380017e+13, 1.375667e+12,
              2.766170e+11, 2.646597e+12, 2.793438e+12, 7.564546e+13, 2.373185e+10, 2.912901e+13, 8.386880e+09]
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


# In[23]:


sql = f"""
--credits: https://app.flipsidecrypto.com/velocity/queries/6bbb795c-9612-4bf2-9320-09179c6fa75c

with 
  ins as (
  select 
  trunc(block_timestamp,'day') as date,
  sum(amount) as amount_in
  from solana.core.fact_transfers x
  join solana.core.dim_labels y on x.tx_from = y.address  
  where mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' --BONK contract
  group by 1
),
 outs as (
select 
  trunc(block_timestamp,'day') as date,
  sum(amount) as amount_out
  from solana.core.fact_transfers x
  join solana.core.dim_labels y on x.tx_to = y.address  
  where mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' --BONK contract
  group by 1
),
  final as (
select
  ifnull(x.date,y.date) as dates,
  ifnull(amount_in,0) as amount_ins,ifnull(amount_out*(-1),0) as amount_outs,
  amount_ins + amount_outs as netflow,
  sum(ifnull(amount_in,0)) over (order by dates) as total_amount_in,
  sum(ifnull(amount_out*(-1),0)) over (order by dates) as total_amount_out,
  total_amount_in+total_amount_out as total_netflow
 from ins x
  join outs y on x.date=y.date 
order by 1 asc 
  )
select * from final where dates>='2022-12-24'
"""

sql2="""

with
  ins as (
  SELECT
  distinct tx_to,
  sum(amount) as USDC_received
  from solana.core.fact_transfers
  where mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' --USDC contract
  group by 1
  ),
  outs as (
  SELECT
  distinct tx_from,
  sum(amount) as USDC_sent
  from solana.core.fact_transfers
  where mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' --USDC contract
  group by 1
  ),
  whales as (
  SELECT
  distinct tx_to as whale,
  USDC_received-USDC_sent as USDC_holdings
  from ins join outs on ins.tx_to=outs.tx_from
  having USDC_holdings>1e11
  ),
  ins2 as (
  select 
  trunc(block_timestamp,'day') as date,
  case when tx_to in (select whale from whales) then 'Whales'
  else 'Regular users' end as type,
  sum(amount) as amount_in
  from solana.core.fact_transfers x
  join solana.core.dim_labels y on x.tx_from = y.address  
  where mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' --USDC contract
  group by 1,2
),
 outs2 as (
select 
  trunc(block_timestamp,'day') as date,
  case when tx_to in (select whale from whales) then 'Whales'
  else 'Regular users' end as type,
  sum(amount) as amount_out
  from solana.core.fact_transfers x
  join solana.core.dim_labels y on x.tx_to = y.address  
  where mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' --USDC contract
  group by 1,2
),
  final as (
select
  x.date,
  x.type,
  amount_in,amount_out*(-1) as amount_outs,
  amount_in - amount_out as netflow
 from ins2 x
  join outs2 y on x.date=y.date and x.type=y.type
order by 1 asc 
  )
select * from final where date>'2022-12-24'
"""


# In[24]:


results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()


# In[27]:


import altair as alt
base=alt.Chart(df).encode(x=alt.X('date:O', axis=alt.Axis(labelAngle=325)))
line=base.mark_line(color='black').encode(y=alt.Y('netflow:Q', axis=alt.Axis(grid=True)))
bar=base.mark_bar(color='red',opacity=0.5).encode(y='amount_outs:Q')
bar2=base.mark_bar(color='green',opacity=0.5).encode(y='amount_ins:Q')

st.altair_chart((bar + bar2 + line).resolve_scale(y='independent').properties(title='Daily $BONK transfer volume flow',width=600))


fig = px.area(df2, x="date", y="amount_in", color="type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(
    title='Amounts inflow by user',
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


fig2 = px.area(df2, x="date", y="amount_outs", color="type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig2.update_layout(
    title='Amounts outflow by user',
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


fig3 = px.area(df2, x="date", y="netflow", color="type", color_discrete_sequence=px.colors.qualitative.Plotly)
fig3.update_layout(
    title='Netflow transfers by user type',
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

col1,col2,col3=st.columns(3)
with col1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:




