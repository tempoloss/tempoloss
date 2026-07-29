# tempoloss

*in chess, a move that accomplishes nothing. 2500+ elo and i still play them, so
it felt like the honest option.*

backend engineer in astana. fullstack at the **agency of financial monitoring** —
crm built from scratch, a clickhouse to postgres migration that took page loads
from fifteen seconds to under one, document pipelines behind an air gap.

python and go. i end up on the parts that fail quietly: locks, queues, query
plans, auth. aitu college, red diploma june 2026, then astana it university.

## what broke, and what i did about it

> the worker died holding the task. the queue never noticed. nobody found out
> until the person waiting on it asked.

**[moxy](https://github.com/tempoloss/moxy)** · go, redis  
a lease is a claim with an expiry, so an unacknowledged task comes back instead
of vanishing. every lease transition is journalled before it happens, which means
a restart replays what was in flight rather than stranding it. the lua scripts
that move tasks between ready, processing and dead now run against a live redis
in ci — before that they shipped having never once been executed.

> the provider returns 400 because the query was malformed. the retry loop tries
> it again. with every key we own.

**[search-gateway](https://github.com/tempoloss/search-gateway)** · python, fastapi  
one gateway over five search apis. every failure is first blamed on the key, the
provider or the caller, and only then does anything decide whether a retry is
even the right move. a bad request burning a whole credential pool to arrive at
the same 400 is not resilience, it is an outage you paid for.

> the client says it moved its rook. the client is lying.

**[chessview](https://github.com/tempoloss/chessview)** · python, react  
the server owns the board and every clock. clients send intent and are told what
happened. disconnects pause the clock instead of losing the game, and engine
analysis runs in your own browser rather than on my bill.

> insert into orders failed: foreign key constraint. it worked yesterday.

**[db-seed](https://github.com/tempoloss/db-seed)** · go  
reads the schema, builds the dependency graph, seeds tables in topological order.
cycles get broken through nullable columns. the sort runs twenty times in ci,
because one green pass does not distinguish a correct ordering from a lucky one.

> looks right. ship it.

**[mentor-skill](https://github.com/tempoloss/mentor-skill)** · agent skill  
an agent skill that refuses to let me merge code i can't explain. it shows the
failure, prices the alternatives, then stops and makes me say it back. keeps a
ledger of what i actually understood, and re-asks when it has gone stale.

> new machine.

**[terminal-setup](https://github.com/tempoloss/terminal-setup)** · powershell  
windows terminal, powershell, oh my posh. one script, and the beige is gone.

## stack

**languages** &nbsp; python · go · typescript · sql

**backend** &nbsp; fastapi · litestar · sqlalchemy · pydantic · dishka · aiogram

**data** &nbsp; postgresql · clickhouse · redis · nats · minio / s3

**infra** &nbsp; docker · kubernetes · nginx · linux · github actions · cloudflare

**frontend** &nbsp; react · next.js · flutter

## elsewhere

[an8kk.dev](https://an8kk.dev) · [t.me/tempoloss](https://t.me/tempoloss) · astana, kazakhstan
