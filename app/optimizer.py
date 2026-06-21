import psutil
import os

class ResourceOptimizer:
    def __init__(self, ram_limit_mb=512):
        self.ram_limit_mb = ram_limit_mb

    def get_stats(self):
        mem = psutil.virtual_memory()
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info().rss / (1024 * 1024) # MB
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        return {
            "ram_used": round(mem_info, 2),
            "ram_limit": self.ram_limit_mb,
            "ram_percent": round((mem_info / self.ram_limit_mb) * 100, 2),
            "cpu_usage": cpu_percent,
            "status": "Optimal" if mem_info < self.ram_limit_mb * 0.8 else "Warning"
        }

    def optimize(self):
        # In a real scenario, this could clear caches or terminate heavy threads
        # For this implementation, we'll simulate a cleanup
        import gc
        gc.collect()
        return "Garbage collection triggered to optimize memory."

optimizer = ResourceOptimizer()
