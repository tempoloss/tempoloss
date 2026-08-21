<h1 align="center">tempoloss</h1>

<p align="center">
  backend engineer · astana, kazakhstan<br/>
  <sub>aitu college graduate · mathematical and computational science undergrad</sub>
</p>

<p align="center">
  <a href="https://t.me/tempoloss"><img alt="telegram" src="https://img.shields.io/badge/telegram-@tempoloss-26A5E4?style=flat-square&logo=telegram&logoColor=white"></a>
  <a href="mailto:me@an8kk.dev"><img alt="email" src="https://img.shields.io/badge/email-me@an8kk.dev-3fb950?style=flat-square&logo=gmail&logoColor=white"></a>
  <a href="https://an8kk.dev"><img alt="website" src="https://img.shields.io/badge/website-an8kk.dev-0b0d0e?style=flat-square&logo=cloudflare&logoColor=3fb950"></a>
  <br/>
  <a href="https://www.chess.com/member/an8kk"><img alt="chess.com bullet" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.chess.com%2Fpub%2Fplayer%2Fan8kk%2Fstats&query=%24.chess_bullet.last.rating&style=flat-square&label=chess%20bullet&color=3fb950"></a>
  <a href="https://github.com/tempoloss?tab=followers"><img alt="followers" src="https://img.shields.io/github/followers/tempoloss?style=flat-square&logo=github&label=followers&color=848d97"></a>
  <a href="https://github.com/tempoloss?tab=repositories"><img alt="stars" src="https://img.shields.io/github/stars/tempoloss?style=flat-square&logo=github&label=stars&color=848d97"></a>
  <img alt="visitors" src="https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithub.com%2Ftempoloss%2Ftempoloss&label=visitors&icon=github&color=%233fb950">
</p>

### brief

- ♟️ **2500+ peak** on [chess.com](https://www.chess.com/member/an8kk), bullet mostly. challenges welcome
- 📐 math is the love of my life; the degree agrees
- 🎧 lately on repeat:
<!--live:start-->
  **playboi carti - fomdj**
<!--live:end-->
- 🎮 making a game. details when it's real

### stack

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,go,rust,ts,js,react,nextjs,flutter,fastapi,nodejs,postgres,redis,sqlite,docker,linux,bash,git,githubactions,cloudflare,cmake&perline=10" alt="stack"/>
  </a>
</p>

### things that ship

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
journal rather than stranding what was in flight. every crash window is
enumerated in `docs/failure-matrix.md` with the test that proves it; the
guarantee is at-least-once, not exactly-once.

**[chessview](https://github.com/tempoloss/chessview)** · python, typescript

realtime chess where the server owns the board and every clock, and the client
gets no vote. clients send intent and are told what happened. disconnects pause
the clock instead of losing the game, and engine analysis runs in your own
browser rather than on my bill.

<details>
<summary>&nbsp;everything else</summary>

<br/>

- **[search-gateway](https://github.com/tempoloss/search-gateway)** · python — one gateway over five search apis; every failure is blamed on the key, the provider or the caller before anything decides whether a retry is the right move
- **[db-seed](https://github.com/tempoloss/db-seed)** · go — seeds a database in dependency order; the sort runs twenty times in ci, because one green pass does not distinguish a correct ordering from a lucky one
- **[shipwatch](https://github.com/tempoloss/shipwatch)** · python — release tags and iso 20022 changes become github issues and telegram messages, on their own
- **[jot](https://github.com/tempoloss/jot)** · javascript — telegram bot that keeps notes as github issues; anything you send is a note, `/task` promotes one later
- **[bugchat](https://github.com/tempoloss/bugchat)** · python — a telegram bug chat becomes a plane board; bursts from one author become one task instead of three fragments
- **[mentor-skill](https://github.com/tempoloss/mentor-skill)** — an agent skill that refuses to let you merge code you can't explain
- **[terminal-setup](https://github.com/tempoloss/terminal-setup)** · powershell — one script, and the beige is gone

</details>
