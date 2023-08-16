from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit

DB_PATH = "vectorstores/db_faiss"

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say "Sorry, I don't know", don't try to make up an answer.

Context: {context}
Question: {question}

Only returns the matching answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])
    return prompt

def load_llm():
    llm = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        config={'max_new_tokens': 512, 'temperature': 0.5}
    )

    return llm

def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        chain_type_kwargs={'prompt': prompt},
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True
    )
    return qa_chain

def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_PATH, embeddings)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

def final_result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    return response

### Chainlit ###
@chainlit.on_chat_start
async def start():
    chain = qa_bot()
    message = chainlit.Message("Starting the app...")
    await message.send()
    message.content = "Hi, welcome to botchat. Ask Away..."
    await message.update()
    chainlit.user_session.set("chain", chain)

@chainlit.on_message
async def main(message):
    chain = chainlit.user_session.get("chain")
    callback = chainlit.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    callback.answer_reached=True
    res = await chain.acall(message, callbacks=[callback])
    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources:" + str(sources)
    else:
        answer += f"\nNo Sources Found"
    
    await chainlit.Message(content=answer).send()