import psutil

def get_system_stats():
    return{
        "cpu_per":psutil.cpu_percent(),
        "mem_per":psutil.virtual_memory().percent
    }