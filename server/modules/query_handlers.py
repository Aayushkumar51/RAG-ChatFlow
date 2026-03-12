from server.logger import logger

def query_chain(chain,user_input:str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        # `create_retrieval_chain` uses the default input key "input"
        result = chain.invoke({"input": user_input})
        docs = result.get("context", []) or []
        response = {
            "response": result.get("answer", ""),
            "sources": [getattr(doc, "metadata", {}) for doc in docs],
        }
        logger.debug(f"Chain response:{response}")
        return response
    except Exception as e:
        logger.exception("Error on query chain")
        raise