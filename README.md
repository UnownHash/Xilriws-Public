# Malte's quick solution to auth problems

very shitty.

you preferrably set this up using poetry `poetry install` and then `poetry run litestar run`

alternatively you can `pip install nodriver litestar[standard]` in whatever environment you prefer. 
then start using `litestar run`.

you probably want to set a host and port. do that with `litestar run --host="127.0.0.1" --port="1234"`