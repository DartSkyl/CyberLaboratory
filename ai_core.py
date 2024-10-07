from langchain_community.llms import YandexGPT
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import asyncio

from configuration import MODEL_URI, FOLDER_ID, MAX_TOKENS


load_dotenv()

# Задаем модель чата
chat_model = YandexGPT(model_uri=MODEL_URI)

# Формируем векторную базу данных на основе текстового документа
loader = TextLoader(file_path='roles_info/company_info.txt', encoding='utf-8')
splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=200)
document = loader.load_and_split(text_splitter=splitter)
embedding = YandexGPTEmbeddings(folder_id=FOLDER_ID)
vector_store = FAISS.from_documents(document, embedding=embedding)
store = vector_store.as_retriever(search_kwargs={'k': 1})
chat_history = []


async def create_prompt():
    with open('roles_prompts/prompt.txt', 'r', encoding='utf-8') as file:
        prompt_text = file.read()
    prompt = ChatPromptTemplate.from_messages([
        ('system', prompt_text),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{input}')
    ])
    # Формируем цепочку
    chain = create_stuff_documents_chain(llm=chat_model, prompt=prompt)
    retrieval_chain = create_retrieval_chain(store, chain)
    return retrieval_chain


# Делаем запрос
async def process_chat(user_input, chat_history_list):

    response = await (await create_prompt()).ainvoke({
        'input': user_input,

        # История чата отключается через пустой список

        'chat_history': chat_history_list,
    })
    print(response)
    return response['answer']


async def start_up():
    while True:
        user = input('You: ')
        if user != 'exit':
            res = await process_chat(user, chat_history)
            print(res)
            chat_history.append(HumanMessage(content=user))
            chat_history.append(AIMessage(content=res))
        else:
            break


if __name__ == '__main__':
    asyncio.run(start_up())
