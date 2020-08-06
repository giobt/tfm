import docker
import time

from utils import *
client = docker.DockerClient(base_url='unix:///var/run/docker.sock')

while True:
    for c in client.containers.list():
        cid = c.id
        name = c.name
        stats = c.stats(stream=False)
        
        cpu = calculate_cpu_percent(stats)
        mem = calculate_mem_percent(stats)
        bio = calculate_block_io_bytes(stats)
        net = calculate_network_bytes(stats)

        x = {"id": cid, "name": name, "cpu": cpu, "mem": mem, "bio": bio, "net": net, "time": time.time() }

        with open("enabler.json", "a") as file_object:
            file_object.write(json.dumps(x) + '\n')
