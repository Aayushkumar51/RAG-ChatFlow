from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



#CORSMiddleware is used in FastAPI to allow requests from different origins (domains, ports, or protocols).
from server.middlewares.exception_handlers import catch_exceptions_middleware
from server.modules.routes.upload_pdf import router as upload_router
from server.modules.routes.ask_question import router as ask_router
app=FastAPI(title="Medical Assistant API",description="API for AI medical Assistant Chatbot")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)





#middleware execption handlers
app.middleware("http")(catch_exceptions_middleware)


#upload pdf file
app.include_router(upload_router)


#asking query

app.include_router(ask_router)
