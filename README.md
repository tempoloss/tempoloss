Backend engineer in Astana. Python and Go.

I keep ending up on the parts that break quietly: locks, queues, query plans,
auth flows. Right now that means financial-intelligence tooling — matching
entities across registries that disagree with each other, getting analytical
queries under a second, generating documents inside an air-gapped network.

2500+ ELO at chess. Same reflex as debugging, apparently.

### Things here

[**moxy**](https://github.com/tempoloss/moxy) · Go

Leases and ACKs for Redis queues, so a task doesn't vanish when the worker
dies. Writes a journal before every lease change and replays it on boot, which
means a restart no longer strands whatever was in flight.

[**search-gateway**](https://github.com/tempoloss/search-gateway) · Python

Sits in front of five search APIs and fails over between them. Works out whose
fault a failure was before deciding to retry. Retrying a malformed query across
every credential you own just burns all of them to answer a 400.

[**chessview**](https://github.com/tempoloss/chessview) · Python, React

Realtime chess. The server owns the board and clients don't get a vote. Clocks
pause on disconnect, Stockfish runs in your browser.

[**db-seed**](https://github.com/tempoloss/db-seed) · Go

Fills a database in the right order by reading the schema and sorting it.
Same order every run, which matters more than it sounds.

[**mentor-skill**](https://github.com/tempoloss/mentor-skill) · agent skill

Won't let me merge code I can't explain. Makes me say it back first, and
remembers what I got wrong. Written after noticing I couldn't.

---

[t.me/tempoloss](https://t.me/tempoloss)
