from __future__ import annotations
import uvicorn


























if __name__ == "__main__":

    uvicorn.run("bot_site:app", host="0.0.0.0", port=8900, log_level="info", reload=True, reload_dirs=["site"])
    # uvicorn.run("router:app", host="0.0.0.0", port=5000, log_level="info")
