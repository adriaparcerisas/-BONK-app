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


st.title('$BONK global activity')


# In[3]:


st.markdown('This part shows the basic $BONK activity trends on **Solana** ecosystem. It is intended to provide an overview of the current token activity in Solana.')


# In[4]:


st.markdown('In this section, we are gonna track the basic metrics registered on Flipside databse so far, such as:') 
st.write('- Swaps and swappers')
st.write('- Average swaps per swapper')
st.write('- Volume swapped and average volume swapped')
st.write('- Transfers and transferrers')
st.write('- Average transfers per transferrers')
st.write('- Volume transferred and average volume transferred')
st.write('')


# In[10]:


sql = f"""
with 
  t2 as (
  select
trunc(y.block_timestamp,'hour') as date,
count(distinct y.tx_id) as swaps,
count(distinct swapper) as swappers,
swaps/swappers as avg_swaps_per_swapper,
  sum(case when swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' then swap_to_amount else swap_from_amount end) as volume_swapped,
    avg(case when swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' then swap_to_amount else swap_from_amount end) as avg_swapped
  from solana.core.fact_swaps y
  where y.block_timestamp>='2022-12-24' and (swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' or swap_from_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263')
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'hour') as date,
count(distinct z.tx_id) as transfers,
count(distinct z.tx_from) as transferers,
transfers/transferers as transfers_per_user,
  sum(amount) as amount_transfered,
  avg(amount) as avg_transfered
  from solana.core.fact_transfers z
  where z.block_timestamp>='2022-12-24' and mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  group by 1
  )
  SELECT
  t2.date,swaps,sum(swaps) over (order by t2.date) as cum_swaps,swappers,sum(swappers) over (order by t2.date) as cum_swappers,avg_swaps_per_swapper,volume_swapped,sum(volume_swapped) over (order by t2.date) as cum_swapped,avg_swapped,
  transfers,sum(transfers) over (order by t2.date) as cum_transfers,transferers,sum(transferers) over (order by t2.date) as cum_transferers,transfers_per_user,amount_transfered,sum(amount_transfered) over (order by t2.date) as cum_transfered,avg_transfered
  from t2,t3 where t2.date=t3.date
order by 1 asc 
"""

sql2 = f"""
with 
  t2 as (
  select
trunc(y.block_timestamp,'day') as date,
count(distinct y.tx_id) as swaps,
count(distinct swapper) as swappers,
swaps/swappers as avg_swaps_per_swapper,
  sum(case when swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' then swap_to_amount else swap_from_amount end) as volume_swapped,
    avg(case when swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' then swap_to_amount else swap_from_amount end) as avg_swapped
  from solana.core.fact_swaps y
  where y.block_timestamp>='2022-12-24' and (swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' or swap_from_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263')
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_id) as transfers,
count(distinct z.tx_from) as transferers,
transfers/transferers as transfers_per_user,
  sum(amount) as amount_transfered,
  avg(amount) as avg_transfered
  from solana.core.fact_transfers z
  where z.block_timestamp>='2022-12-24' and mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  group by 1
  )
  SELECT
  t2.date,swaps,sum(swaps) over (order by t2.date) as cum_swaps,swappers,sum(swappers) over (order by t2.date) as cum_swappers,avg_swaps_per_swapper,volume_swapped,sum(volume_swapped) over (order by t2.date) as cum_swapped,avg_swapped,
  transfers,sum(transfers) over (order by t2.date) as cum_transfers,transferers,sum(transferers) over (order by t2.date) as cum_transferers,transfers_per_user,amount_transfered,sum(amount_transfered) over (order by t2.date) as cum_transfered,avg_transfered
  from t2,t3 where t2.date=t3.date
order by 1 asc 
"""

sql3 = f"""
with 
  t2 as (
  select
trunc(y.block_timestamp,'week') as date,
count(distinct y.tx_id) as swaps,
count(distinct swapper) as swappers,
swaps/swappers as avg_swaps_per_swapper,
  sum(case when swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' then swap_to_amount else swap_from_amount end) as volume_swapped,
    avg(case when swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' then swap_to_amount else swap_from_amount end) as avg_swapped
  from solana.core.fact_swaps y
  where y.block_timestamp>='2022-12-24' and (swap_to_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263' or swap_from_mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263')
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'week') as date,
count(distinct z.tx_id) as transfers,
count(distinct z.tx_from) as transferers,
transfers/transferers as transfers_per_user,
  sum(amount) as amount_transfered,
  avg(amount) as avg_transfered
  from solana.core.fact_transfers z
  where z.block_timestamp>='2022-12-24' and mint='DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  group by 1
  )
  SELECT
  t2.date,swaps,sum(swaps) over (order by t2.date) as cum_swaps,swappers,sum(swappers) over (order by t2.date) as cum_swappers,avg_swaps_per_swapper,volume_swapped,sum(volume_swapped) over (order by t2.date) as cum_swapped,avg_swapped,
  transfers,sum(transfers) over (order by t2.date) as cum_transfers,transferers,sum(transferers) over (order by t2.date) as cum_transferers,transfers_per_user,amount_transfered,sum(amount_transfered) over (order by t2.date) as cum_transfered,avg_transfered
  from t2,t3 where t2.date=t3.date
order by 1 asc 
"""


# In[11]:


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

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.subheader('Terra general activity metrics regarding transactions')
#st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[ ]:


st.subheader('Swapping activity')


# In[12]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['swaps'],
                name='# of swaps',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Hourly $BONK swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly swaps", secondary_y=False)
fig1.update_yaxes(title_text="Total swaps", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['swaps'],
                name='# of swaps',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily $BONK swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily swaps", secondary_y=False)
fig2.update_yaxes(title_text="Total swaps", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['swaps'],
                name='# of sales',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swaps'],
                name='# of sales',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Weekly $BONK swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly swaps", secondary_y=False)
fig3.update_yaxes(title_text="Total swaps", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly swaps", "Daily swaps", "Weekly swaps"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[13]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['volume_swapped'],
                name='Volume swapped (BONK)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swapped'],
                name='Volume swapped (BONK)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig1.update_layout(
    title='Hourly volume swapped (BONK)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly volume swapped (BONK)", secondary_y=False)
fig1.update_yaxes(title_text="Total volume swapped (BONK)", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['volume_swapped'],
                name='Volume swapped (BONK)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swapped'],
                name='Volume swapped (BONK)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily volume swapped (BONK)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily volume swapped (BONK)", secondary_y=False)
fig2.update_yaxes(title_text="Total volume swapped (BONK)", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['volume_swapped'],
                name='Volume swapped (BONK)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swapped'],
                name='Volume swapped (BONK)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig3.update_layout(
    title='Weekly volume swapped (BONK)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly volume swapped (BONK)", secondary_y=False)
fig3.update_yaxes(title_text="Total volume swapped (BONK)", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily volume swapped", "Weekly volume swapped", "Monthly volume swapped"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[14]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['swappers'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swappers'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Hourly BONK swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly swappers", secondary_y=False)
fig1.update_yaxes(title_text="Total swappers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['swappers'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swappers'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily BONK swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily swappers", secondary_y=False)
fig2.update_yaxes(title_text="Total swappers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['swappers'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swappers'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Weekly BONK swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly swappers", secondary_y=False)
fig3.update_yaxes(title_text="Total swappers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily swappers", "Weekly swappers", "Monthly swappers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[15]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Line(x=df['date'],
                y=df['avg_swapped'],
                name='volume (BONK)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig1.update_layout(
    title='Hourly average swapped',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly average swapped (BONK)", secondary_y=False)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Line(x=df['date'],
                y=df2['avg_swapped'],
                name='volume (BONK)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig2.update_layout(
    title='Daily BONK average swapped',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily average swapped (BONK)", secondary_y=False)

# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Line(x=df['date'],
                y=df3['avg_swapped'],
                name='volume (BONK)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig3.update_layout(
    title='Weekly BONK average swapped',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly average swapped (BONK)", secondary_y=False)


tab1, tab2, tab3 = st.tabs(["Daily average swapped", "Weekly average swapped", "Monthly average swapped"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[16]:


st.write('')
st.subheader('Transacting activity')


# In[17]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['transfers'],
                name='# of transfers',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_transfers'],
                name='# of transfers',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Hourly $BONK transfers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly transfers", secondary_y=False)
fig1.update_yaxes(title_text="Total transfers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['transfers'],
                name='# of transfers',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_transfers'],
                name='# of transfers',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily $BONK transfers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily transfers", secondary_y=False)
fig2.update_yaxes(title_text="Total transfers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['transfers'],
                name='# of transfers',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_transfers'],
                name='# of transfers',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Weekly $BONK transfers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly transfers", secondary_y=False)
fig3.update_yaxes(title_text="Total transfers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly transfers", "Daily transfers", "Weekly transfers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[19]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['amount_transfered'],
                name='Volume transfered (BONK)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_transfered'],
                name='Volume transfered (BONK)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig1.update_layout(
    title='Hourly volume transfered (BONK)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly volume transfered (BONK)", secondary_y=False)
fig1.update_yaxes(title_text="Total volume transfered (BONK)", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['amount_transfered'],
                name='Volume transfered (BONK)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_transfered'],
                name='Volume transfered (BONK)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily volume transfered (BONK)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily volume transfered (BONK)", secondary_y=False)
fig2.update_yaxes(title_text="Total volume transfered (BONK)", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['amount_transfered'],
                name='Volume transfered (BONK)',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_transfered'],
                name='Volume transfered (BONK)',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig3.update_layout(
    title='Weekly volume transfered (BONK)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly volume transfered (BONK)", secondary_y=False)
fig3.update_yaxes(title_text="Total volume transfered (BONK)", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily volume transfered", "Weekly volume transfered", "Monthly volume transfered"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[20]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['transferers'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_transferers'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Hourly BONK transferers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly transferers", secondary_y=False)
fig1.update_yaxes(title_text="Total transferers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['transferers'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_transferers'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily BONK transferers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily transferers", secondary_y=False)
fig2.update_yaxes(title_text="Total transferers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['transferers'],
                name='# of users',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_transferers'],
                name='# of users',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Weekly BONK transferers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly transferers", secondary_y=False)
fig3.update_yaxes(title_text="Total transferers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily transferers", "Weekly transferers", "Monthly transferers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[21]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Line(x=df['date'],
                y=df['avg_transfered'],
                name='volume (BONK)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig1.update_layout(
    title='Hourly average transfered',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly average transfered (BONK)", secondary_y=False)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Line(x=df['date'],
                y=df2['avg_transfered'],
                name='volume (BONK)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig2.update_layout(
    title='Daily BONK average transfered',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily average transfered (BONK)", secondary_y=False)

# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Line(x=df['date'],
                y=df3['avg_transfered'],
                name='volume (BONK)',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y'))

fig3.update_layout(
    title='Weekly BONK average transfered',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly average transfered (BONK)", secondary_y=False)


tab1, tab2, tab3 = st.tabs(["Daily average transfered", "Weekly average transfered", "Monthly average transfered"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:




