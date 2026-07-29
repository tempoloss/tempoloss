# tempoloss

*in chess, a move that accomplishes nothing. 2500+ elo and i still play them, so
it felt like the honest option.*

backend engineer in astana. mostly python and go — fastapi, litestar,
sqlalchemy, postgres, clickhouse, redis, nats, docker. i end up on the parts
that fail quietly: locks, queues, query plans, auth.

aitu college, red diploma june 2026, then astana it university.

---

**[moxy](https://github.com/tempoloss/moxy)** · go, redis

a reliability layer for redis queues. a lease is a claim with an expiry, so an
unacknowledged task comes back instead of vanishing when its worker dies. a lease
is journalled before it becomes visible to anyone, and a restart replays the
journal instead of stranding what was in flight. the task leaves the ready queue
before that record is durable, though, so a crash in between used to leave it
held by nobody — startup now reconciles the backend against the journal and hands
those tasks back. every crash window is enumerated in `docs/failure-matrix.md`
with the test that proves it; the guarantee is at-least-once, not exactly-once.
the lua scripts that move tasks between ready, processing and dead run against a
live redis in ci — before that they shipped having never once been executed.

**[search-gateway](https://github.com/tempoloss/search-gateway)** · python, fastapi

one gateway over five search apis, with failover between them. every failure is
first blamed on the key, the provider or the caller, and only then does anything
decide whether a retry is even the right move. a malformed query burning a whole
credential pool to arrive at the same 400 is not resilience, it is an outage you
paid for.

**[chessview](https://github.com/tempoloss/chessview)** · python, react

realtime chess where the server owns the board and every clock, and the client
gets no vote. clients send intent and are told what happened. disconnects pause
the clock instead of losing the game, and engine analysis runs in your own
browser rather than on my bill.

**[quackiso](https://github.com/tempoloss/quackiso)** · rust, duckdb

reads iso 20022 bank messages as sql tables — camt statements, camt notifications,
pacs transfers, pain initiations. amounts never touch a float, because
`0.10 + 0.20 + 0.30 + 1500.10` is `1500.7000000000003` and that is somebody's
money. a 1.7 gb statement parses in about 2 mb of memory, since it streams events
instead of building a tree. tested against 45 real messages from nine banks and
vendors; every special case in the parser is there because one of those files
broke it.

**[db-seed](https://github.com/tempoloss/db-seed)** · go

seeds a database in dependency order: reads the schema, builds the graph, sorts
it topologically, and breaks cycles by dropping a minimal set of nullable foreign
keys — never a required one, because nulling it is not something the database
would accept. the sort runs twenty times in ci, because one green pass does not
distinguish a correct ordering from a lucky one. the awkward cases are a schema
file, not a wish: reserved-word table names, composite keys, `match full`,
generated columns, arrays, domains.

<details>
<summary>&nbsp;smaller things</summary>

<br/>

**[mentor-skill](https://github.com/tempoloss/mentor-skill)** · agent skill

refuses to let me merge code i can't explain. shows the failure, prices the
alternatives, then stops and makes me say it back. keeps a ledger of what i
actually understood, and asks again once it has gone stale.

**[terminal-setup](https://github.com/tempoloss/terminal-setup)** · powershell

windows terminal, powershell, oh my posh. one script, and the beige is gone.

</details>

---

[an8kk.dev](https://an8kk.dev) &nbsp;·&nbsp; [t.me/tempoloss](https://t.me/tempoloss) &nbsp;·&nbsp; astana, kazakhstan
