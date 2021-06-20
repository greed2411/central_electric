
# Central Electric

[![celc.png](https://i.postimg.cc/sghmHnwv/celc.png)](https://postimg.cc/pmPKpBNH)

Coming from southern states of India, we have faced several mass-powercuts and still do. It's far better nowadays, but there have been days when we've had powercut like 9am-5pm on saturdays, or alternating 3 hours during daytime in the rural areas.

So a just a wishful thinking project 🧞, that one day we can get paid during those times. Of course the money is coming out of State's Electricity Board. Why? Just to add more [skin-in-the-game](https://fs.blog/2017/11/hammurabis-code/) 👦🔫 from their (TNEB) end. 


The name of the project comes out as a play-of-word from the organization [General Electric](https://en.wikipedia.org/wiki/General_Electric), and the new and upcoming decentralized [oracle](https://en.wikipedia.org/wiki/Blockchain_oracle) based blockchain systems.


Developed these kind of thoughts ([decentralized insurance use case](https://blog.aeternity.com/blockchain-oracles-657f134ffbc0)) after the witnessing [aeternity's first hackathon](https://humandefihaeck.devpost.com/). The project from that point-of-view is, you get paid 🤑 whenever sensors/io detect that there is a powercut.


## Application

The application is pretty simple. It serves the user (imaginary) from terminal only as of now.

* the `device.py` websocket-streams disconnection (a python process) of powercut.
* the `user.py` can see the incremental addition of rupees to his account every second (yes again streaming).
* the `app` directory has a server which accepts all sorts of `user` and `device` websocket connections.


From a learning point of view, I've always wanted to build a streaming application. Just got the simple chance to build it.

From frameworks pov,

* my very first [FastAPI](https://fastapi.tiangolo.com/) (a)sync application.
* my very first [SQLAlchemy](https://www.sqlalchemy.org/) + [SQLite](https://www.sqlite.org/index.html) ORM application.
* lol even a very first websockets application using asyncio.


## Architecture Diagram

[![central-electric.png](https://i.postimg.cc/7hpNV0vF/central-electric.png)](https://postimg.cc/XBkFNZYL)

The architecture may feel unnecessary and over-complicated. For the lack of `goroutines` and `channels` equivalent in Python, this is the way I felt.

Each device sends `timestamp` and `lapsed` time in seconds, every second over websocket. Which the server, stores in db as events & adds an accrual interest (non-linear) to the user's device over time.

Then these events are pushed to rabbit-mq, consumed (literally just ping-pong) by `consumer`, later sent back to the server, to the active user websocket route. 

Basically this solves the problem of: I'm getting a stream of events, I want to analyze them, then send it to somebody else as a stream in real-time.

This is a [good article](https://ably.com/topic/websockets-kafka#transport-protocol-interoperability) on what all exist out there for this problem. Notable ways of handling it were: [MQTT](https://en.wikipedia.org/wiki/MQTT), [WebSockets](https://en.wikipedia.org/wiki/WebSocket) & [Server-Sent-Events](https://en.wikipedia.org/wiki/Server-sent_events).


## BTW

I thought this would scale fine, but encountered a bottleneck, the websocket opened by `consumer` with `server` doesn't last forever / long-lived. Ran into [Broken Pipe Error](https://stackoverflow.com/questions/4584904/what-causes-the-broken-pipe-error), since there was a situation even thought the websocket connection was global, there was rabbitmq's callback happening on every event payload. which started messing it up. therefore, the `consumer` establishes new websocket connection with the server on new events (lol ik).

I still wanted to refactor this project with pure async coroutines for handling new requests, but meh. the pure `def` sync functions are called [using a threadpool](https://fastapi.tiangolo.com/async/?h=sync#very-technical-details), so i assume it's fine for now.
