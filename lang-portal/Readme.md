## Install dependencies

```sh
uv pip install -r requirements.txt
```

Using pip method:
```sh
pip install -r requirements.txt
```

## Setup DB

```sh
uv run -m invoke init-db

# OR

invoke init-db
```

## Run

```sh
uv run app.py

# OR

python app.py
```