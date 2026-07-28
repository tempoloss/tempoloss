<h1 align="center">tempoloss</h1>

<p align="center">
  <i>in chess, a move that accomplishes nothing.</i><br/>
  <i>2500+ elo and i still play them, so it felt like the honest option.</i>
</p>

---

backend engineer in astana. fullstack at the **agency of financial monitoring** —
crm built from scratch, a clickhouse to postgres migration that took page loads
from fifteen seconds to under one, document pipelines behind an air gap.

python and go. i end up on the parts that fail quietly: locks, queues, query
plans, auth. aitu college, red diploma june 2026, then astana it university.

---

## things that exist because something broke

**[moxy](https://github.com/tempoloss/moxy)** · go, redis  
redis queues drop your task when a worker dies and never mention it. leases,
acks and a write-ahead journal, so a restart doesn't quietly strand whatever was
in flight. ci runs the race detector and the whole suite against a live redis,
because the lua scripts that move tasks between ready, processing and dead used
to ship having never once been executed.

**[search-gateway](https://github.com/tempoloss/search-gateway)** · python, fastapi  
five search apis, at least one of them is always down. works out whose fault a
failure was before deciding to retry, because retrying a malformed query across
every key you own burns all of them to answer a 400.

**[chessview](https://github.com/tempoloss/chessview)** · python, react  
realtime chess where the client doesn't get a vote. the server owns the board,
clocks pause on disconnect, stockfish runs in your browser.

**[db-seed](https://github.com/tempoloss/db-seed)** · go  
reads a schema, sorts it, fills the database in an order that doesn't trip over
its own foreign keys. the sort runs twenty times in ci, because you can't prove
determinism with one green run.

**[mentor-skill](https://github.com/tempoloss/mentor-skill)** · agent skill  
i was shipping code i couldn't explain. this one makes me say it back before it
lets me merge, and keeps a ledger of what i got wrong.

**[terminal-setup](https://github.com/tempoloss/terminal-setup)** · powershell  
windows terminal, one script, for when a machine is new and beige.

---

## stack

**languages** &nbsp; python · go · typescript · sql

**backend** &nbsp; fastapi · litestar · sqlalchemy · pydantic · dishka · aiogram

**data** &nbsp; postgresql · clickhouse · redis · nats · minio / s3

**infra** &nbsp; docker · kubernetes · nginx · linux · github actions · cloudflare

**frontend** &nbsp; react · next.js · flutter

---

<p align="center">
  <sub>astana, kazakhstan · <a href="https://an8kk.dev">an8kk.dev</a> · <a href="https://t.me/tempoloss">t.me/tempoloss</a></sub>
</p>
