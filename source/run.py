from rest_api import app
import bottle
import api_routes
import multiprocessing

workers =  multiprocessing.cpu_count() * 2 + 1

if __name__ == '__main__':
    bottle.run(host = '0.0.0.0', port = '4356')
