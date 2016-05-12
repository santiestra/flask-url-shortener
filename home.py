from flask import Flask, render_template, request, redirect
import utils
import redis

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def url_shortener():
    if request.method == 'POST':
        redisConn = redis.StrictRedis(host='localhost', port=6379, db=0)
        url = request.form['url']

        # Check if valid url
        if utils.isValidUrl(url):
            pass
        else:
            return 'Url Invalida'

        savedInRedis = redisConn.get(url)

        if savedInRedis:
            # If that url already has a shortened url, return it.
            return 'ShortCode:  ' + savedInRedis
        else:
            randomExists = True
            # If it doesn't have a short url created, creat it.
            # Iterate creating random string until we find a string that is not
            #  taken.
            while randomExists:
                randomString = utils.randomShortString(5)
                if redisConn.get(randomString):
                    pass
                else:
                    randomExists = False
                    # We save both key-value couples, short code -> url
                    #  and url -> short code
                    redisConn.set(randomString, url)
                    redisConn.set(url, randomString)
                    return 'ShortCode:  ' + randomString


    else:
        return render_template('home.html')


@app.route('/<shortCode>')
def redirect_to_original_url(shortCode):
    redisConn = redis.StrictRedis(host='localhost', port=6379, db=0)
    savedInRedis = redisConn.get(shortCode)
    if savedInRedis:
        return redirect(savedInRedis)
    else:
        return 'Error, invalid url'

if __name__ == '__main__':
    app.run(debug=True)
