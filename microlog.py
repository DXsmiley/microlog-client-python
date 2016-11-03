import time as time_module
import queue
import requests
import json
import collections
import threading
import time

g_username = None
g_api_token = None
g_url = None
g_started = False
g_queue = None
g_thread = None
g_run_thread = True
g_post_interval = 20

def ensure_started(func):
    def internal(*args, **kwargs):
        if g_started:
            func(*args, **kwargs)
        else:
            raise Exception('Attempted to do something to microlog without starting it properly')
    internal.__name__ = func.__name__
    return internal

@ensure_started
def dispatch():
    datasets = collections.defaultdict(list)
    count = 0
    try:
        while True:
            item = g_queue.get_nowait()
            datasets[item['graph']].append({
                'time': item['time'],
                'count': item['count'],
                'text': item['text']
            })
            count += 1
    except queue.Empty:
        pass
    if count > 0:
        organised = []
        for key, value in datasets.items():
            organised.append({
                'graph': key,
                'points': value
            })
        payload = {
            'api_username': g_username,
            'api_token': g_api_token,
            'datasets': organised
        }
        try:
            result = requests.post(g_url, json = payload)
        except Exception:
            pass # TODO: Catch only the things that might matter.
        for i in range(count):
            g_queue.task_done()

@ensure_started
def enque(graph, count = 1, text = '', time = None):
    if not time:
        time = int(time_module.time())
    try:
        g_queue.put_nowait({
            'graph': graph,
            'count': count,
            'time': time,
            'text': str(text)
        })
    except queue.Full:
        pass

@ensure_started
def halt_thread():
    global g_run_thread
    g_run_thread = False

def _thread_function():
    while g_run_thread:
        time.sleep(g_post_interval)
        dispatch()

def start(username, api_token, **kwargs):
    global g_username
    global g_api_token
    global g_url
    global g_started
    global g_queue
    global g_post_interval
    global g_thread
    if g_started:
        raise Exception('Attempted to start microlog client multiple times')
    g_username = username
    g_api_token = api_token
    g_url = kwargs.get('url', 'https://microlog-metrics.herokuapp.com/graphs/api/')
    g_queue = queue.Queue(kwargs.get('queue_maxsize', 0))
    g_post_interval = kwargs.get('post_interval', 20)
    g_started = True
    if kwargs.get('thread', False):
        d = kwargs.get('daemon', None)
        g_thread = threading.Thread(target = _thread_function, daemon = d)
        g_thread.start()
