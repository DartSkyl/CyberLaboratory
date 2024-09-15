from langchain.chains import LLMChain
from langchain_community.llms import YandexGPT
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
# from pydantic import BaseModel, Field
# from langchain_core.output_parsers import JsonOutputParser
import asyncio

from configuration import MODEL_URI, FOLDER_ID


load_dotenv()

# Задаем модель чата
chat_model = YandexGPT(model_uri=MODEL_URI)

# Формируем векторную базу данных на основе текстового документа
loader = TextLoader(file_path='company_info.txt', encoding='utf-8')
splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=200)
document = loader.load_and_split(text_splitter=splitter)
embedding = YandexGPTEmbeddings(folder_id=FOLDER_ID)
vector_store = FAISS.from_documents(document, embedding=embedding)
store = vector_store.as_retriever(search_kwargs={'k': 1})
chat_history = []

with open('prompt.txt', 'r', encoding='utf-8') as file:
    prompt_text = file.read()


async def create_prompt():
    # global prompt_text
    # company_contact_data = await bot_base.get_company_contacts_data()
    # company_contact_data = (f'Contact information: '
    #                         f'Address {company_contact_data[0][1]}, '
    #                         f'Phone {company_contact_data[1][1]}, '
    #                         f'Office Hours {company_contact_data[2][1]}')
    # prompt_text += company_contact_data
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

    response = (await create_prompt()).invoke({
        'input': user_input,
        'chat_history': chat_history_list,
    })
    return response['answer']


# def check_name(user_msg):
#     model = YandexGPT(model_name='yandexgpt-lite')
#
#     prompt_for_name = ChatPromptTemplate.from_messages([
#         ('system', 'Извлеки имя человека из сообщения если он там есть\nИнструкция форматирования:{format}'),
#         ('human', '{input}')
#     ])
#     # model_config = {}
#
#     class Person(BaseModel):
#         model_config['protected_namespaces'] = ()
#         name: str = Field(description='the name of the person')
#
#     parser = JsonOutputParser(pydantic_object=Person)
#     chain_for_name = prompt_for_name | model | parser
#     return chain_for_name.invoke({'input': user_msg,
#                                   'format': parser.get_format_instructions()})


if __name__ == '__main__':
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

    asyncio.run(start_up())

    # while True:
    #     user = input('You: ')
    #     if user != 'exit':
    #         res = process_chat(user, chat_history)
    #         print('Assistant: ' + res)
    #         chat_history.append(HumanMessage(content=user))
    #         chat_history.append(AIMessage(content=res))
    #     else:
    #         break
