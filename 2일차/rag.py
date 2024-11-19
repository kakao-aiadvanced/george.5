import bs4

# langchain: 언어 모델과 관련된 작업을 도와주는 라이브러리
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 블로그 내용을 가져오고, 작은 덩어리로 나누고, 검색할 수 있게 준비해요.
# WebBaseLoader는 웹 페이지에서 필요한 정보를 가져오는 도구예요.
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",),  # 블로그 주소
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(  # 블로그에서 필요한 부분만 가져와요.
            class_=("post-content", "post-title", "post-header")  # 글 본문, 제목, 헤더만 선택
        )
    ),
)

# 블로그 내용을 loader가 가져와요.
docs = loader.load()

# RecursiveCharacterTextSplitter: 텍스트를 작게 나누는 도구
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# 블로그 내용을 1000글자씩 나누되, 200글자는 겹치게 만들어요.
splits = text_splitter.split_documents(docs)

# Chroma: 검색할 수 있게 정보를 저장하는 도구
# OpenAIEmbeddings: 내용을 숫자로 바꿔서 컴퓨터가 이해할 수 있게 만들어요.
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# 검색 도우미(retriever)를 만들어요.
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# 질문과 답변을 생성할 때 사용할 '프롬프트'를 가져와요.
promptForRag = hub.pull("rlm/rag-prompt")

# 가져온 문서를 포맷(형식) 맞추는 함수
def format_docs(docs):
    # 모든 문서를 한 번에 합쳐서 큰 글로 만들어요.
    return "\n\n".join(doc.page_content for doc in docs)

parser = JsonOutputParser()

promptForLLM = PromptTemplate(
    template="""
    You are an AI system evaluating the relevance between a user query and a retrieved text. Your task is to determine whether the retrieved text (context) is relevant to the user’s query (question). Use the following criteria:
- Consider the direct relevance of the context to the question. If the context can reasonably help answer the question, it is relevant.
- Ignore minor wording differences; focus on conceptual and semantic alignment.
- If the context is off-topic or unrelated to the question, it is not relevant.

The response is a relevance field, and if relevant, it should be true or false.

\n{format_instructions}\n{question}\n{context}\n
    """,
    input_variables=["question","context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

llmChain = promptForLLM | llm | parser
question = "What is Task Decomposition?"

chainForRag = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | promptForRag
)
context = chainForRag.invoke(question)
response = llmChain.invoke({"question": question, "context": context})

if response["relevance"] == True :
    print("GOOD!")

    prompt = PromptTemplate(
      template="Answer the user query.\n{format_instructions}\n{query}\n",
      input_variables=["query"],
      partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    print(chain.invoke({"query": context}))
else :
    print("No...")

# 하지만... 이렇게 하는 것보다 claude 나 gpt 가 작성해주는 것이 훨씬 깔끔...ㅠ.ㅜ