# backEndCapstone2.0
There are a couple steps to run this server. After you clone the repo, cd into it and perform the following steps:
1. Run this command: ```python -m venv backendEnv```
2. Next, run command: ```source ./backendEnvbin/activate```
3. Run: ```pip install -r requirements.txt```


The next steps are for setting up the database:
1. In the root project directory run the command: ```python manage.py makemigrations```
2. Next run: ```python manage.py migrate```
3. Then run: ```python manage.py loaddata <fixture file name minus .json>```
load order should be:
company
userType
giftCard

Now that your database is set up all you have to do is run the command:

```python manage.py runserver```

