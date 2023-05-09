import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

os.environ['OPENAI_API_KEY'] = apikey

st.title('GPT haiku creator')
prompt = st.text_input('Write a haiku about:')

title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'Write me a haiku about {topic}'
)

haiku_template = PromptTemplate(
    input_variables = ['title', 'wiki_research'],
    template = 'Write me a haiku based on this title: {title} while leveraging this Wikipedia research: {wiki_research}'
)

title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
haiku_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

llm = OpenAI(temperature = 0.9)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
haiku_chain = LLMChain(llm=llm, prompt=haiku_template, verbose=True, output_key='haiku', memory=haiku_memory)

wiki = WikipediaAPIWrapper()

if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    haiku = haiku_chain.run(title=title, wiki_research=wiki_research)

    st.write(title)
    st.write(haiku)

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Haiku History'):
        st.info(haiku_memory.buffer)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)