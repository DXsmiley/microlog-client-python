import microlog
import time

# You can see this graph: https://microlog-metrics.herokuapp.com/graphs/QB0NXRd1N36pafvXYdFJ?i=60

microlog.start('example', 't0lZe3QFqbRL67IsFU1k')

EXAMPLE_GRAPH = 'QB0NXRd1N36pafvXYdFJ'

time_now = int(time.time())
microlog.enque(EXAMPLE_GRAPH, count = 5)
microlog.enque(EXAMPLE_GRAPH, count = 2, time = time_now - 600)

microlog.dispatch()
