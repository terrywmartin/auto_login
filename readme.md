# Auto Login
TODO:

    - Add more error handling
    - Refactor as I learn more

I wanted to create a quick Python script to login to the Olight Store website to get the daily login points.  This is my first time using Selenium so the code could use some optimization.  I'll refactor the code as I learn more about the process.

This project uses Python and Selenium.

You'll need a .env file with the following values:

```
URL=
LOGIN_METHOD=UN_PW
UN=
PSWD=

GA_PSWD=
```

For my use case, the URL is https://olightstore.com.  The LOGIN_METHOD options are UN_PW for basic username and password or GOOGLE for Google Authentication.  The website also supports Facebook login but I haven't implemented that because I don't use it.  

**NOTE: The GOOGLE method is not working at the moment.  The error message states the browser is not secure.**

I have a bat file that runs the Python script.

The file looks similar to this.  I use venv for my virtual environment.  Replace {path} with the path to your Python script.

```
venv\Scripts\python.exe  {path}\login.py
```