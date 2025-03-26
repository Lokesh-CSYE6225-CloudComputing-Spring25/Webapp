from statsd import StatsClient

statsd = StatsClient(host='localhost', port=8125, prefix='webapp')
