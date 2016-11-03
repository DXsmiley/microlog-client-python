# Microlog Python Client

A minimal python client for [microlog](https://github.com/dxsmiley/microlog).

*Disclaimer:* Microlog, and this python client, are still in early development. They may be unstable or insecure.

## Installation

It's currently not set up to be friendly. The best option at the moment is just to copy the `microlog.py` file.

## API

### `microlog.start(username, api_token, **kwargs)`

#### Positional arguments

`username` - The username of your account, that you'd use to log in to the micrlog website.

`api_token` - Your API token. This can be found on the dashboard of the microlog website.

#### Keyword arguments

`url` - The URL of the microlog website. You can change this if you are running your own instance of microlog, such as in a testing environment.

`queue_maxsize` - The maximum size of the internal queue, in number of items. Defaults to unlimited.

`thread` - Boolean. Specifies whether the internal thread should be started.

`post_interval` - Specifies the approximate time gap between sending data packets to the server. Utilized only when using the internal threading feature.

`daemon` - Specifies whether the thread should be a [daemon](https://docs.python.org/3/library/threading.html#threading.Thread.daemon). Defaults to `None`, which means that it will inherit the property from the thread that called it. This property can also be set to `True` or `False` to enforce daemon-ness.

### `microlog.enque(graph, count = 1, time = None)`

Specify a data point on a graph. Enters the data into the queue to be send to the server.

`graph` - The ID of the graph that the data should be send to. This is found at the end of the URL when viewing the graph from the website.

`count` - The value of the point (roughly the point's position on the y-axis). If not specified, defaults to 1.

`time` - The time of the point (position on the x-axis of the graph). This value should be given in seconds since the UNIX epoch. If not specifies, defaults to the current time.

### `microlog.dispatch()`

Sends all data currently in the queue to the server. You should not have to call this if the thread is running.

### `microlog.halt_thread()`

Stops the thread running. This won't happen immidiately, so the thread may make at most one more call to `dispatch` before stopping.
