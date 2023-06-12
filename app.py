from flask import Flask
from datetime import timedelta






app =  Flask(__name__)
app.secret_key = 'kl2sd34hfjkdalfads5fds46f6a1ds5fdasdsjcnflkad45damferopee23'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1000)







