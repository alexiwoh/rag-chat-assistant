from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models.fake import FakeListChatModel
from langchain.tools import tool

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@tool
def get_greeting(name: str) -> str:
    """Returns a greeting message for the given name."""
    return f"Hey {name}, welcome to our LangChain agent!"


llm = FakeListChatModel(responses=["This is a mock response."])
tools = [get_greeting]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

chat_history = []


@app.get("/", response_class=HTMLResponse)
def serve_chat(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })


@app.post("/", response_class=HTMLResponse)
def handle_chat(request: Request, query: str = Form(...)):
    answer = agent.run(query)
    chat_history.append({"user": query, "agent": answer})
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })
