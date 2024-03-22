# Malte's quick solution to auth problems

very shitty.

you preferrably set this up using poetry `poetry install` and then `poetry run litestar run`

alternatively you can `pip install nodriver litestar[standard]` in whatever environment you prefer. 
then start using `litestar run`.

dont forget to copy config.example.json to config.json

you need chromedriver installed, and it needs to be in your `PATH`.
The easiest way to do this on ubuntu-like operating systems is `sudo apt install chromium-chromedriver`.

