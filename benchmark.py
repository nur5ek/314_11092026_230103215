import sys
import time
import math
from concurrent.futures import ProcessPoolExecutor

LIMIT = 5_000_000


def count_primes(start, end):
    count = 0

    for n in range(max(2, start), end):
        if n == 2:
            count += 1
            continue

        if n % 2 == 0:
            continue

        is_prime = True
        limit = math.isqrt(n)

        for d in range(3, limit + 1, 2):
            if n % d == 0:
                is_prime = False
                break

        if is_prime:
            count += 1

    return count


def run_benchmark(workers):
    chunk = LIMIT // workers
    ranges = []

    for i in range(workers):
        start = i * chunk
        end = LIMIT if i == workers - 1 else (i + 1) * chunk
        ranges.append((start, end))

    start_time = time.perf_counter()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = executor.map(
            count_primes,
            [r[0] for r in ranges],
            [r[1] for r in ranges]
        )

    total_primes = sum(results)

    end_time = time.perf_counter()

    print(f"Workers: {workers}")
    print(f"Primes found: {total_primes}")
    print(f"Time: {end_time - start_time:.3f} seconds")


if __name__ == "__main__":
    workers = int(sys.argv[1])
    run_benchmark(workers)