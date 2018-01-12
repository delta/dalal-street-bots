import sched, time
s = sched.scheduler(time.time, time.sleep)
def print_time(a='default'):
    print("From print_time", time.time(), a)

def print_some_times():
    print(time.time())
    #s.enter(.010, 1, print_time)
    #s.enter(.005, 2, print_time, argument=('positional',))
    #s.enter(.005, 1, print_time, kwargs={'a': 'keyword'})
    for i in range(10000):
        s.enter(0.1, 1, print_time)
    s.run()
    print(time.time())

if __name__ == "__main__":
    print_some_times()
