# fastapi-notes-demo — a real FastAPI app for cleanroom's in-tab VM

An ordinary FastAPI notes app. On any machine with Python:

```bash
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000
```

Inside [cleanroom](https://amanvicky.github.io/cleanroom/) it needs none of
that on YOUR machine: paste this repo's link, press **Set up & run**, and the
runner installs `fastapi` into the in-tab VM (pydantic comes from the VM's own
catalog — its compiled core is a WebAssembly build), then drives the ASGI app
with the VM's event loop. No uvicorn, no socket, nothing listens — the page
itself is the app's network. The wipe erases everything, like every session.
