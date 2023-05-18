import os, time
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

os.environ['OPENAI_API_KEY'] = apikey

st.title('GPT haiku creator')
prompt = st.text_input('Write me a haiku about:')

haiku_template = PromptTemplate(
    input_variables = ['topic'],
    template = '''
    Write a traditional haiku for me.
    A traditional haiku is comprised of three lines of 5, 7, and 5 syllables.

    A syllable is a unit of spoken language that is next bigger than a speech sound 
    and consists of one or more vowel sounds alone or of a syllabic consonant alone 
    or of either with one or more consonant sounds preceding or following. 

    Here are some examples:

    Q: Write me a haiku about video games.

    A: 
    Late nights with my friends
    A·comm-plish im·poss·ible
    Dream·ing on my screen

    Q: Write me a haiku about how it feels to sit by a fire.

    A: 
    Pop crackl·ing sounds
    Smoke stink brings back me·mo·ries
    Glow·ing logs com·fort

    Q: Write me a haiku about San Francisco in the summer time.

    A: 
    At Gol-den Gate Park
    Mu·sic flow·ing through the air    
    People rejoi·cing

    Q: Write me a haiku about the taste of pizza.

    A:
    Nos·trils a·wa·ken 
    Va·por·ous de·li-cious smells 
    Savo·ry good·ness

    Q: Write me a haiku about {topic}.
    
    A:
    '''
)

informed_haiku_template = PromptTemplate(
    input_variables = ['haiku', 'wiki_research'],
    template = 'Write me a haiku based on this haiku: {haiku} while leveraging this Wikipedia research: {wiki_research}'
)

syllable_counter_template = PromptTemplate(
    input_variables = ['haiku'],
    template = ''' 
    How many total syllables are in the following words? {haiku}
    '''
)

haiku_checker_template = PromptTemplate(
    input_variables = ['haiku'],
    template = 'Does the following poem fit the definition of a haiku?: {haiku}'
)

haiku_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
informed_haiku_memory = ConversationBufferMemory(input_key='haiku', memory_key='chat_history')
syllable_counter_memory = ConversationBufferMemory(input_key='haiku', memory_key='chat_history')
haiku_checker_memory = ConversationBufferMemory(input_key='haiku', memory_key='chat_history')

llm = OpenAI(temperature = 0.9)
haiku_chain = LLMChain(llm=llm, prompt=haiku_template, verbose=True, output_key='haiku', memory=haiku_memory)
informed_haiku_chain = LLMChain(llm=llm, prompt=informed_haiku_template, verbose=True, output_key='informed_haiku', memory=informed_haiku_memory)
syllable_counter_chain = LLMChain(llm=llm, prompt=syllable_counter_template, verbose=True, output_key='syllable_count', memory=syllable_counter_memory)
haiku_checker_chain = LLMChain(llm=llm, prompt=haiku_checker_template, verbose=True, output_key='haiku_checker', memory=haiku_checker_memory)

wiki = WikipediaAPIWrapper()

if prompt:
    haiku = haiku_chain.run(prompt)
    # wiki_research = wiki.run(prompt)
    # informed_haiku = informed_haiku_chain.run(haiku=haiku, wiki_research=wiki_research)
    haiku_syllable_count = syllable_counter_chain.run(haiku=haiku)
    # informed_haiku_syllable_count = syllable_counter_chain.run(haiku=informed_haiku)
    haiku_checker = haiku_checker_chain.run(haiku=haiku)
    # informed_haiku_checker = haiku_checker_chain.run(haiku=informed_haiku)

    st.write("Haiku: " + haiku)
    # st.write("Informed haiku: " + informed_haiku)
    st.write("Haiku syllable count: " + haiku_syllable_count)
    # st.write("Informed haiku syllable count: " + informed_haiku_syllable_count)
    st.write("Is the AI's haiku a haiku?" + haiku_checker)
    # st.write("Is the AI's informed haiku a haiku?" + informed_haiku_checker)

    with st.expander('Haiku History'):
        st.info(haiku_memory.buffer)

    with st.expander('Informed Haiku History'):
        st.info(informed_haiku_memory.buffer)

    # with st.expander('Wikipedia Research'):
    #     st.info(wiki_research)

    with st.expander('Syllable history'):
        st.info(syllable_counter_memory.buffer)

    with st.expander('Checker history:'):
        st.info(haiku_checker_memory.buffer)