"""A real FastAPI notes app — no server needed where it runs.

In cleanroom's in-tab VM the app is driven directly through ASGI (the
VM's own event loop plays the role uvicorn plays on a machine): no
sockets, nothing listens, the page is the app's only network. The store
is an in-memory dict — the VM has no database.
"""
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Notes")
NOTES = []
_next_id = [1]

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Notes — FastAPI in a tab</title>
<style>
  body { font: 15px system-ui, sans-serif; background: #f7f7f5; margin: 0;
         display: flex; justify-content: center; padding: 36px 16px; }
  .card { background: #fff; border: 1px solid #ddd; border-radius: 10px;
          padding: 22px; width: 430px; box-shadow: 0 2px 8px rgba(0,0,0,.06); }
  h1 { margin: 0 0 2px; font-size: 20px; }
  .sub { color: #777; margin: 0 0 14px; font-size: 13px; }
  .row { display: flex; gap: 8px; }
  input { flex: 1; padding: 9px 12px; border: 1px solid #ccc; border-radius: 8px;
          font: 14px system-ui, sans-serif; }
  button { background: #146c94; color: #fff; border: none; border-radius: 8px;
           padding: 9px 14px; font: 600 14px system-ui, sans-serif; cursor: pointer; }
  .del { background: #b34a4a; padding: 4px 9px; font-size: 12px; }
  ul { list-style: none; margin: 14px 0 0; padding: 0; }
  li { display: flex; justify-content: space-between; gap: 8px; padding: 8px 2px;
       border-top: 1px solid #eee; }
  .empty { color: #999; padding: 12px 2px; }
</style>
</head>
<body>
<div class="card">
  <h1>Notes</h1>
  <p class="sub">a real FastAPI app — driven by the VM's event loop, no PC involved</p>
  <form method="post" action="/add" class="row">
    <input name="text" placeholder="write a note…" autofocus>
    <button type="submit">add</button>
  </form>
  <ul>
  {notes_html}
  </ul>
</div>
</body>
</html>
"""


def render():
    items = "".join(
        '<li><span>{}</span><form method="post" action="/delete/{}">'
        '<button class="del" type="submit">✕</button></form></li>'.format(
            n["text"], n["id"])
        for n in NOTES) or '<li class="empty">no notes yet — add one</li>'
    return PAGE.replace("{notes_html}", items)


@app.get("/", response_class=HTMLResponse)
def index():
    return render()


@app.post("/add")
def add(text: str = Form("")):
    text = text.strip()
    if text:
        NOTES.append({"id": _next_id[0], "text": text})
        _next_id[0] += 1
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{note_id}")
def delete(note_id: int):
    global NOTES
    NOTES[:] = [n for n in NOTES if n["id"] != note_id]
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn
    print("this app runs on a machine with uvicorn; inside cleanroom's")
    print("in-tab VM, type: set up & run   (or: serve)")
    uvicorn.run(app, host="127.0.0.1", port=8000)
