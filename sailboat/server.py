from handler.router import app
from common import scheduler


if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True, port=3031)