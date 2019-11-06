# Back-End Capstone
There are a couple steps to run this server. After you clone the repo, cd into it and perform the following steps:
1. Run this command: ```python -m venv backendEnv```
2. Next, run command: ```source ./backendEnvbin/activate```
3. Run: ```pip install -r requirements.txt```


The next steps are for setting up the database:
1. In the root project directory run the command: ```python manage.py makemigrations```
2. Next run: ```python manage.py migrate```
3. Then run: ```python manage.py loaddata <fixture file name minus .json>```
    
    Load order should be:
       
        1. company
        2. userType
        3. giftCard

For this app, the map part of a company report will not work, because the data directory was not added to the repo. You will need to take out 

        <div class="iframe-container">
            <iframe id="mapFrame" title="Map Report" aria-hidden="true" src="{% url 'capstone:map' %}" allowfullscreen></iframe>
        </div>
  
 and
        
        {% block scripts %}
            <script>
                document.getElementById("mapFrame").onload = () => {
                  document.getElementById("loadingScreen").style.display = "none"
                }
            </script>
        {% endblock %}
from
         ```"capstone/templates/report/details.html"```
  
Now that your database is set up all you have to do is run the command:

```python manage.py runserver```

