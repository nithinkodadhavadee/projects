## Pakcages to install
 - flask
 - werkzeug
 -  numpy
 - soundfile
 - moviepy
 - scipy
 - IPython
 - transformers

## Execution
Open the terminal in the folder where the `app.py` file exists and execute the following command. 

``` flask run --host=0.0.0.0 ```

When you do this, you'll be able to see a URL mentioned in the output which looks somethin like this

``` https://192.168.0.***:5000/ ```

copy the above mentioned link and paste in any of the web browsers.

if you don't want to use the web UI, you can execute the model.py instead as well. buy make sure to go to line 36 in the `model.py` file, remove that line from comment and then pass the *path to the audio file* as a parameter to the function.
