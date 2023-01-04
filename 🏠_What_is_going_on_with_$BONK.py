#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[5]:


st.title('Whats going on with $BONK?')


# In[6]:


st.markdown("**$BONK** is the very first Dog-themed memecoin on **Solana** that’s “for the people, by the people.”")
st.markdown('As the documentation says, _The BONK contributors were tired of toxic Alameda tokenomics and wanted to make a fun memecoin where everyone gets a fair shot_.')
st.markdown("A keep-in-mind particularity is that 50% of the total supply of the cryptocurrency was airdropped to the Solana community, while the main purpose of the team behind it is to bring back liquidity to decentralized exchanges built on Solana.")
st.write("")
st.markdown("This dashboard represents a **$BONK activity overview** in general trends. It is intended to provide an overview of the current $BONK situation and its impact on the main Solana ecosystem.")


# In[7]:


st.markdown("To display all the information properly and make the app more readable and user-friendly, it has been divided in several parts. You can find information about each different section by navigating on the sidebar pages.")


# In[8]:


st.markdown("These includes:") 
st.markdown('1. $BONK global activity')     
st.markdown('2. $BONK holders') 
st.markdown('3. $BONK user behavior') 
st.markdown('4. $BONK movements') 


# In[ ]:




