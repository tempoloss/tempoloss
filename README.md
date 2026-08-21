```
tmp@astana:~$ whoami
tempoloss · backend engineer, astana
python, go, rust
aitu college graduate; mathematical and computational science undergrad
```

<!--live:start-->
```
tmp@astana:~$ status
chess    bullet 2419 · peak 2602
music    last played: playboi carti - fomdj
llm      866,941,544 tokens
shipped  quackiso v1.5.1 · duckdb community registry
updated  2026-08-21 22:42 utc
```
<!--live:end-->

```
tmp@astana:~$ ls ~/things-that-ship
```

**[quackiso](https://github.com/tempoloss/quackiso)** · rust, duckdb

reads iso 20022 and swift mt bank messages as sql tables — camt statements and
notifications, pacs transfers, pain initiations, and the mt940/mt942 files banks
actually dump. amounts never touch a float, because
`0.10 + 0.20 + 0.30 + 1500.10` is `1500.7000000000003` and that is somebody's
money. a 1.7 gb statement parses in about 2 mb of memory, and ci asserts that
number on every push. lives in the
[official duckdb community registry](https://community-extensions.duckdb.org/extensions/quackiso.html);
getting it there involved finding and fixing a bug in the
[registry's own release pipeline](https://github.com/duckdb/community-extensions/pull/2430).
tested against ~280 real messages from more than a dozen banks and vendors; every
special case in the parser is there because one of those files broke it.

**[moxy](https://github.com/tempoloss/moxy)** · go, redis

a reliability layer for redis queues. a plain pop deletes the task outright, so a
worker that dies mid-task takes it with them and redis keeps no record it existed.
a lease is a claim with an expiry, so an unacknowledged task comes back instead.
the lease is journalled before anyone can see it, and a restart replays the
journal rather than stranding what was in flight — though the task leaves the
ready queue before that record is durable, so a crash in between used to leave it
held by nobody, and startup now reconciles the backend against the journal to
hand those tasks back. every crash window is enumerated in
`docs/failure-matrix.md` with the test that proves it; the guarantee is
at-least-once, not exactly-once. the lua scripts that move tasks between ready,
processing and dead run against a live redis in ci — before that they shipped
having never once been executed.

**[search-gateway](https://github.com/tempoloss/search-gateway)** · python

one gateway over five search apis, with failover between them. every failure is
first blamed on the key, the provider or the caller, and only then does anything
decide whether a retry is the right move. 

**[chessview](https://github.com/tempoloss/chessview)** · python, typescript

realtime chess where the server owns the board and every clock, and the client
gets no vote. clients send intent and are told what happened. disconnects pause
the clock instead of losing the game, and engine analysis runs in your own
browser rather than on my bill.

**[db-seed](https://github.com/tempoloss/db-seed)** · go

seeds a database in dependency order: reads the schema, builds the graph, sorts
it topologically, and breaks cycles by dropping a minimal set of nullable foreign
keys — never a required one, because nulling it is not something the database
would accept. the sort runs twenty times in ci, because one green pass does not
distinguish a correct ordering from a lucky one. the awkward cases are a schema
file, not a wish: reserved-word table names, composite keys, `match full`,
generated columns, arrays, domains.

<details>
<summary>&nbsp;ls ~/smaller-things</summary>

<br/>

**[mentor-skill](https://github.com/tempoloss/mentor-skill)** · agent skill

refuses to let you merge code you can't explain. shows the failure, prices the
alternatives, then stops and makes you say it back. keeps a ledger of what you
actually understood, and asks again once it has gone stale.

**[jot](https://github.com/tempoloss/jot)** · javascript, cloudflare workers

a telegram bot that keeps notes as github issues. anything you send is a note —
deciding whether a thought is a task is work, and doing it at capture time is how
the note never gets written. `/task` promotes one later. storage is issues, so
the github app is a second client i didn't have to write.

**[shipwatch](https://github.com/tempoloss/shipwatch)** · python, github actions

keeps public follow-through from getting forgotten: release tags and iso 20022
changes become github issues and telegram messages. state is written only after
every sink accepts, so a failed delivery retries instead of going silent.

**[bugchat](https://github.com/tempoloss/bugchat)** · python, telegram, plane

a telegram bug chat becomes a plane board. bursts from one author become one
task instead of three fragments, screenshots stay with the report, replies become
comments, and a closed task gets answered back in the chat.

**[terminal-setup](https://github.com/tempoloss/terminal-setup)** · powershell

windows terminal, powershell, oh my posh. one script, and the beige is gone.

</details>

```
tmp@astana:~$ contact --sorted-by=speed
```

[t.me/tempoloss](https://t.me/tempoloss) &nbsp;·&nbsp; [an8kk.dev](https://an8kk.dev) &nbsp;·&nbsp; [me@an8kk.dev](mailto:me@an8kk.dev)

```
tmp@astana:~$ █
```
