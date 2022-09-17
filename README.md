# example_repo

## Installation

First of all you will need Python(3.8.13). You can download it by https://www.python.org/.

Now let's start installation

Run this commant to clone test repository with project
```sh
git clone https://github.com/zebestroo/example_repo.git
```

Go to the repo

```sh
cd example_repo
```

Create virtual environment

```sh
python3.8 -m venv djangoenv
```

Activate virtual environment

```sh
source djangoenv/bin/activate
```

Install requirements
```sh
pip install -r requirements.txt
```

Go to the project repo
```sh
cd fox
```

After creating stripe [Account](https://stripe.com/) you will have two keys `Publishable key` and `Secret key`. For testing project with this account you should replace fields `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` in your `fox/settings.py` to your personal `Publishable key` and `Secret key`. It will look like this python code in `fox/settings.py`:
```
STRIPE_PUBLISHABLE_KEY = '<Publishable key>'
STRIPE_SECRET_KEY = '<Secret key>'
```

Run server with this command and test it at the localhost(127.0.0.1:8000):
```sh
python manage.py runserver
```

## Note

"_When you'll open webpage you'll see that there are no items. Fill out the form beforehand you can create items with 'Create product' button. After you'll able to view items and buy it with 'Buy' button._"
