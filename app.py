import streamlit as st
import os
import time
from dotenv import load_dotenv
import pickle


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI


from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory

from get_wiki import *

load_dotenv()


@st.cache_data
def get_text_chunks(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text=text)
    return chunks

@st.cache_data
def get_vector_store(store_name, chunks):
    if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            
    else:
        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        with open(f"{store_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

    return VectorStore




def main():
    st.title('🤗💬 Chat with Wiki App')

    url = st.text_input("Please Enter Wikipedia URL")

    if url:

        wiki_extract = get_wiki_extract(url)
        with st.sidebar:
            st.write(wiki_extract)

        
        chunks = get_text_chunks(wiki_extract)
        end_index = wiki_extract.find('\n',0)
        store_name = wiki_extract[0:end_index-2]

        st.markdown("Given URL consist information about ##### " + store_name)
        VectorStore = get_vector_store(store_name, chunks)


        # Initialize Streamlit chat UI
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        

        if query := st.chat_input("Ask a query about given page:"):


            with st.chat_message("Human"):
                st.markdown(query)
            
            llm = OpenAI(model_name='gpt-3.5-turbo')
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            chain = ConversationalRetrievalChain.from_llm(llm, VectorStore.as_retriever(), memory=memory)

            with get_openai_callback() as cb:
                #response = chain({"input_documents": docs, "human_input": query}, return_only_outputs=True)
                response = chain({'question':query})
                print(cb)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                for chunk in response["answer"].split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(response["answer"])
            for msg in response["chat_history"]:
                st.session_state.messages.append({"role": msg.type, "content": msg.content})






if __name__ == '__main__':
    main()
