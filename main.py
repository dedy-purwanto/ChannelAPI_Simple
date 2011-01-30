from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import channel
from django.utils import simplejson
import datetime

# Handler Utama
class MainPage(webapp.RequestHandler):
    def get(self):
        client_id = "mychannel" + str(datetime.datetime.now()) # Nama Channel
        token = channel.create_channel(client_id) # Buat channel dan ambil tokennya
        # Kirim client_id dan channel ke output
        output = template.render('index.html', {'token' : token, 'client_id' : client_id})
        self.response.out.write(output)
        
# Handler ketika client mengirim pesan
class MessageReceived(webapp.RequestHandler):
    def post(self):
        # Ambil client ID dan name
        client_id = self.request.get('client_id')
        name = self.request.get('name')
        # Format balasan dengan JSON
        reply = {
            'reply_message' : 'Hallo, ' + name + '!'
        }
        # Kirim balasan, parameternya (client_id, pesan)
        channel.send_message(client_id,simplejson.dumps(reply))



application = webapp.WSGIApplication(   [
                                        ('/msg',MessageReceived),
                                        ('/', MainPage)
                                        ],debug = True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()