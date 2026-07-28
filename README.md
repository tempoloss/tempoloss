Backend engineer in Astana. Python and Go, mostly the parts where being almost
right is the same as being wrong — locks, queues, query plans, auth flows.

Currently building financial-intelligence tooling: entity resolution across
mismatched registries, analytical workloads that have to answer in under a
second, document pipelines behind an air gap.

2500+ ELO at chess, which turns out to be the same habit as debugging — assume
the position is worse than it looks, then check.

---

**[moxy](https://github.com/tempoloss/moxy)** · Go
Leases, ACKs and visibility timeouts on top of Redis-style queues, so a task
does not vanish when a worker dies. Lease state is journalled write-ahead and
replayed on boot; a torn final record is truncated rather than trusted.

**[search-gateway](https://github.com/tempoloss/search-gateway)** · Python
High-availability middleware over five search providers. Failures are blamed on
the key, the provider or the caller before any retry is chosen — retrying a
malformed query across every credential burns the pool to answer a 400.

**[chessview](https://github.com/tempoloss/chessview)** · Python · React
Realtime chess with server-owned state: the board never trusts the client,
clocks pause on disconnect, engine analysis runs in the browser.

**[db-seed](https://github.com/tempoloss/db-seed)** · Go
Seeds a database in dependency order by reading the schema and topologically
sorting it. Cycles are broken through nullable foreign keys, and the ordering is
deterministic between runs.

**[mentor-skill](https://github.com/tempoloss/mentor-skill)** · agent skill
Refuses to let you ship code you cannot explain. Explains it, then stops and
makes you restate it, and keeps a ledger of what you actually understood.

---

Reachable at [t.me/tempoloss](https://t.me/tempoloss).
