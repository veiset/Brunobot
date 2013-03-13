Displays users of a channel and their status.


Events
======

"users.#channel"
"users.#channel.join"
"users.#channel.part"
"users.#channel.mode"

API
===

getUsers(#channel) -> List of (User, Status)
getUser(#channel, user) -> (User, Status)
