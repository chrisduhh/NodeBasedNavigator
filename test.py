import timeit
import tracemalloc

def test_performance():
    start_time = timeit.default_timer()
    tracemalloc.start()

    # Test code
    _ = [x**2 for x in range(100000)]

    elapsed_time = timeit.default_timer() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Elapsed Time: {elapsed_time:.6f} seconds")
    print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KiB")

test_performance()
