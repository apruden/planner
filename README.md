# planner

work planning service

# Spec

- A worker has shifts
- A shift is 8 hours long
- A worker never has two shifts on the same day
- It is a 24 hour timetable 0-8 (NIGHT), 8-16 (DAY), 16-24 (LATE)

# API

REST endpoints

```
/workers
/workers/<id>
/workers/<id>/allocations
/allocations
```

# Developing

run dev server

```
$ cd src
$ export FLASK_APP=planner
$ flask run
```

integration tests tests

```
$ cd src
$ python -m pytest
```
