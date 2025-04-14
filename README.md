# StatusCode418-Battlesnake

## Running

```python -m venv venv```

```source venv/Scripts/activate```

```pip install -r requirements.txt```

```python -m src.main```

## Testing

unittest can mess up imports so I am giving it src as PYTHONPATH

```PYTHONPATH=src python -m unittest test.test_utility -v```

```PYTHONPATH=src python -m unittest discover -s test -v```

## The Board

The board looks like this, which makes the indexing of the matrixes sometimes strange.

(0, 10) (1, 10) ... (10, 10)

...

(0, 1)  (1, 1)  ... (10, 1)

(0, 0)  (1, 0)  ... (10, 0)

## Game objects

### Board object
```python
board = {
    "height": 11,
    "width": 11,
    "food": [
        {"x": 5, "y": 5},
        {"x": 9, "y": 0},
        {"x": 2, "y": 6}
    ],
    "hazards": [
        {"x": 0, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": 2}
    ],
    "snakes": [
        {"id": "snake-one", ... },
        {"id": "snake-two", ... },
        {"id": "snake-three", ... }
    ]
}
```

### Snake object

```python
snake = {
    "id": "totally-unique-snake-id",
    "name": "Sneky McSnek Face",
    "health": 54,
    "body": [
        {"x": 0, "y": 0},
        {"x": 1, "y": 0},
        {"x": 2, "y": 0}
    ],
    "latency": "123",
    "head": {"x": 0, "y": 0},
    "length": 3,
    "shout": "why are we shouting??",
    "squad": "1",
    "customizations":{
        "color":"#26CF04",
        "head":"smile",
        "tail":"bolt"
    }
}
```