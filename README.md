# envibe

Simple environment variables parser built on [`feils-catus`](https://github.com/LeeeeT/felis) in order to provide lazy evaluation of environment variables.

Basic example:
```python
from envibe import read_dotenv, take
from felis import lazy

read_dotenv()

print(lazy.run(take("SECRET_KEY")))  # Prints some secret key
```

✨ Yas, it's a pun, btw. FP pun!!! 🐈
