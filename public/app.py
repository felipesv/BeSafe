''' Run app '''
from flask import Flask, render_template
from uuid import uuid4

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
   ''' render index.html '''
   cache = str(uuid4())
   return render_template('index.html', cache=cache)


@app.errorhandler(404)
def page_404(e):
    ''' 404 error
    '''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
