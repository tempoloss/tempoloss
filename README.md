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
unacknowledged task comes back instead of vanishing when its worker dies. every
lease transition is journalled before it happens, which means a restart replays
what was in flight rather than stranding it. the lua scripts that move tasks
between ready, processing and dead run against a live redis in ci — before that
they shipped having never once been executed.

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

**[db-seed](https://github.com/tempoloss/db-seed)** · go

seeds a database in dependency order: reads the schema, builds the graph, sorts
it topologically, breaks cycles through nullable columns. the sort runs twenty
times in ci, because one green pass does not distinguish a correct ordering from
a lucky one.

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
