# coding=UTF-8

from webapp import app
from webapp.dist.views import login_manager

login_manager.init_app(app)

app.run(debug=True,use_reloader=False)