wsgi_app = "askme_grigoreva.wsgi:application"
workers = 2
bind = "0.0.0.0:8000"
reload = True
timeout = 30

def pre_request(worker, req):
    print(f"Connect: {req.method} {req.path}")