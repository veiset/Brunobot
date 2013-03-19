Scrum Planning Poker
====================

Start a new issue:
```
.pp.start <votes needed> <issue>
```
Close an issue:
```
.pp.agree <issueID>
```
Current status of an issue:
```
.pp.status <issueID>
```

Example module usage (IRC scenario):
```
vz:     .pp.start 1 How much work is this module?
bruno:  Planning poker ID 1 (How much work is this module?) started.
bruno:  type "/msg bruno pp 1 <weight>" to vote on the issue.

> bruno pp 1 5
< bruno Vote registered on issue 'How much work is this module?'.

bruno:  Done voting on issue 1 (How much work is this module?), average vote: 5.0, votes: [5].
bruno:  Vote on 1 reset. To close it, type: .pp.agree 1

vz:     .pp.agree 1
bruno:  Planning poker ID 1 (How much work is this module?) has been closed.
```

