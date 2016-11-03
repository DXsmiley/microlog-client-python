import microlog
import time
import random

# You can see this graph: https://microlog-metrics.herokuapp.com/graphs/TNNBxb1k16jUfHPs8Ml3?i=60

microlog.start('example', 't0lZe3QFqbRL67IsFU1k', thread = True, post_interval = 5)

EXAMPLE_GRAPH = 'TNNBxb1k16jUfHPs8Ml3'

for i in range(20):
    print('.')
    time_now = int(time.time())
    microlog.enque(EXAMPLE_GRAPH, count = random.randint(1, 5), time = time_now - random.randint(0, 600))
    time.sleep(1)

print()

microlog.halt_thread()
