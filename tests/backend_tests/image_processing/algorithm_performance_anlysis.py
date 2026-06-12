
import time
import tracemalloc
import numpy as np # To simulate some work

# --- Step 1: Create a Decorator for Timing ---
# A decorator is a function that wraps another function to add functionality.
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"--- Starting '{func.__name__}' ---")
        
        # 1. Record the start time using a high-precision clock
        start_time = time.perf_counter()
        
        # 2. Call the original function
        result = func(*args, **kwargs)
        
        # 3. Record the end time and calculate the duration
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        
        print(f"--- Finished '{func.__name__}' in {duration_ms:.2f} ms ---")
        return result
    return wrapper

# --- Step 2: Create a function to simulate your main process ---
# We apply the timing decorator using the '@' syntax.
@timing_decorator
def generate_glass_certificate(rows, cols):
    """
    A dummy function that simulates the work of your certificate generation.
    It creates a large NumPy array to use a noticeable amount of memory.
    """
    print(f"Processing a matrix of size {rows}x{cols}...")
    
    # Simulate work: create a large data structure in memory
    # This will be our main memory and CPU load.
    certificate_matrix = np.random.rand(rows, cols)
    
    # Simulate some calculations
    for _ in range(5): # Loop to simulate iterative calculations
        certificate_matrix *= 1.01 
        time.sleep(0.1) # Simulate I/O or other blocking operations

    print("Processing complete.")
    return certificate_matrix

# --- Step 3: Use tracemalloc to measure memory usage ---
def main():
    # 1. Start tracking memory allocations
    tracemalloc.start()

    # 2. Get the memory usage *before* running the function
    # This gives us a baseline.
    before_size, before_peak = tracemalloc.get_traced_memory()
    print(f"Memory before execution: {before_size / 1024:.2f} KiB")

    # 3. Run the function you want to profile
    # The timing decorator will automatically print the execution time.
    generate_glass_certificate(5000, 5000) # Using a large matrix to see memory change

    # 4. Get the memory usage *after* running the function
    after_size, after_peak = tracemalloc.get_traced_memory()
    print(f"Memory after execution: {after_size / 1024:.2f} KiB")
    
    # 5. Stop tracking memory
    tracemalloc.stop()

    # --- Step 4: Analyze the Results ---
    memory_increase = (after_size - before_size) / 1024**2
    peak_usage = (after_peak) / 1024**2
    
    print("\n--- Profiling Summary ---")
    print(f"Memory increase during function call: {memory_increase:.2f} MiB")
    print(f"Peak memory usage during function call: {peak_usage:.2f} MiB")
    print("-------------------------")


if __name__ == "__main__":
    main()