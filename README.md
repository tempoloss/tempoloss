<h1 align="center">tempoloss</h1>

<p align="center">
  <i>in chess, a move that accomplishes nothing.</i><br/>
  2500+ elo and i still play them, so it felt like the honest option.
</p>

<p align="center">
  <a href="https://t.me/tempoloss"><img alt="telegram" src="https://img.shields.io/badge/telegram-tempoloss-8ec5ff?style=flat-square&logo=telegram&logoColor=8ec5ff&labelColor=04070c"></a>
  <a href="https://an8kk.dev"><img alt="site" src="https://img.shields.io/badge/site-an8kk.dev-8ec5ff?style=flat-square&logo=firefoxbrowser&logoColor=8ec5ff&labelColor=04070c"></a>
  <img alt="chess" src="https://img.shields.io/badge/chess-2500%2B%20elo-8ec5ff?style=flat-square&logo=lichess&logoColor=8ec5ff&labelColor=04070c">
  <img alt="visitors" src="https://komarev.com/ghpvc/?username=tempoloss&style=flat-square&color=8ec5ff&label=visitors">
</p>

---

### about

- 🏛 fullstack engineer at the **agency of financial monitoring**, kazakhstan. crm built from scratch, a clickhouse → postgres migration that took page loads from 15s to under a second, document pipelines behind an air gap
- 🐍 python and go. i end up on the parts that fail quietly: locks, queues, query plans, auth
- 🎓 aitu college, red diploma june 2026, then astana it university
- 📍 astana, kazakhstan · ru / kk native, en fluent

---

### stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=py,go,ts,fastapi,react,nextjs,postgres,redis,clickhouse,docker,kubernetes,nginx,linux,githubactions,grafana,cloudflare&perline=8&theme=dark" alt="stack"/>
</p>

---

### things that exist because something broke

| | |
|:--|:--|
| **[moxy](https://github.com/tempoloss/moxy)** · go, redis<br/><a href="https://github.com/tempoloss/moxy/actions/workflows/go.yml"><img src="https://img.shields.io/github/actions/workflow/status/tempoloss/moxy/go.yml?style=flat-square&label=ci&labelColor=04070c"></a> <a href="https://github.com/tempoloss/moxy/releases"><img src="https://img.shields.io/github/v/release/tempoloss/moxy?include_prereleases&style=flat-square&label=release&labelColor=04070c&color=8ec5ff"></a> | redis queues drop your task when a worker dies and never mention it. leases, acks, and a write-ahead journal, so a restart doesn't quietly strand whatever was in flight |
| **[search-gateway](https://github.com/tempoloss/search-gateway)** · python, fastapi<br/><a href="https://github.com/tempoloss/search-gateway/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/tempoloss/search-gateway/ci.yml?style=flat-square&label=ci&labelColor=04070c"></a> <a href="https://github.com/tempoloss/search-gateway/pkgs/container/search-gateway"><img src="https://img.shields.io/badge/ghcr-published-8ec5ff?style=flat-square&logo=docker&logoColor=8ec5ff&labelColor=04070c"></a> | five search apis, at least one of them is always down. works out whose fault a failure was before retrying, because retrying a bad query across every key you own burns all of them to answer a 400 |
| **[chessview](https://github.com/tempoloss/chessview)** · python, react<br/><a href="https://github.com/tempoloss/chessview/actions/workflows/pr-ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/tempoloss/chessview/pr-ci.yml?style=flat-square&label=ci&labelColor=04070c"></a> <img src="https://img.shields.io/badge/ghcr-3%20images-8ec5ff?style=flat-square&logo=docker&logoColor=8ec5ff&labelColor=04070c"> | realtime chess where the client doesn't get a vote. the server owns the board, clocks pause on disconnect, stockfish runs in your browser |
| **[db-seed](https://github.com/tempoloss/db-seed)** · go<br/><a href="https://github.com/tempoloss/db-seed/actions/workflows/go.yml"><img src="https://img.shields.io/github/actions/workflow/status/tempoloss/db-seed/go.yml?style=flat-square&label=ci&labelColor=04070c"></a> <a href="https://github.com/tempoloss/db-seed/releases"><img src="https://img.shields.io/github/v/release/tempoloss/db-seed?style=flat-square&label=release&labelColor=04070c&color=8ec5ff"></a> | reads a schema, sorts it, fills the database in an order that doesn't trip over its own foreign keys. same order every run |
| **[mentor-skill](https://github.com/tempoloss/mentor-skill)** · agent skill<br/><a href="https://github.com/tempoloss/mentor-skill/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/tempoloss/mentor-skill/ci.yml?style=flat-square&label=ci&labelColor=04070c"></a> | i was shipping code i couldn't explain. this one makes me say it back before it lets me merge, and remembers what i got wrong |

<details>
<summary>&nbsp;smaller things, and what "ci" actually means up there</summary>

<br/>

- **[terminal-setup](https://github.com/tempoloss/terminal-setup)** — windows terminal + powershell + oh my posh, one script. for when a machine is new and beige

every badge above is a pipeline that runs something real, not a linter waving at you:

- **moxy** runs the race detector and the redis-backed suite against a live server. the lua scripts that move tasks between ready, processing and dead used to ship having never once been executed
- **search-gateway** brings up redis in ci too. twelve tests covering key rotation and the cache were quietly skipping before that
- **db-seed** runs the topological sort `-count=20`, because you can't prove determinism with one green run
- **chessview** builds all three docker images the compose stack needs. it broke for a while on a node version mismatch nobody noticed, since the images were two majors behind the ci jobs
- **terminal-setup** parses the powershell without executing it, for reasons that should be obvious

releases are cross-compiled for linux, macos and windows with checksums; the services publish multi-arch images to ghcr.

</details>

---

<p align="center">
  <sub>astana · <a href="https://t.me/tempoloss">t.me/tempoloss</a></sub>
</p>
