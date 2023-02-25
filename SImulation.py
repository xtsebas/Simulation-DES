import random
import simpy

def MemoryUse(env, name, time, RAM, CPU):
    global totalTime

    yield env.timeout(time)
    timeProcess = env.now

    timeNeeded = random.randint(1,10)
    ramNeeded = random.randint(1,10)

    print("The %f starts at %dR and needs %o quantity of RAM" % (name, timeNeeded, ramNeeded))

    with CPU.request() as CPU_, RAM.put() as RAM_:
        yield RAM_
        yield CPU_
        yield env.timeout(timeNeeded)
        print("The %f ended at %r" % (name, env.now))

    total = env.now - timeProcess
    print("The %r lasted %dst units of time" % (name, total))
    totalTime += total




env = simpy.Environment()
RAM = simpy.Container(env, init=0, capacity=100)
CPU= simpy.Resource(env, capacity=1)
random.seed(10)
totalTime = 0


for i in range(25):
    env.process(MemoryUse(env, "Process %s"%i, random.expovariate(1.0/10),RAM, CPU))

env.run(100)

print("The average time of the processes is: ", totalTime/25.0)

