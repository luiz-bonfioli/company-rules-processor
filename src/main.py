from src import app
from src.commons.config import WEB_SERVER_HOST, WEB_SERVER_PORT

# To run locally
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
