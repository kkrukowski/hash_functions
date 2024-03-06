import hashlib
import time, timeit
import plotly.graph_objects as go

# Function that hashes text by every hashing algorithms in hashlib
def hashing_algs():
    text = input("Enter text to hash: ")
    results = []
    algorithms = hashlib.algorithms_available
    for algorithm in algorithms:
        # Used for calculating hashing time
        start_time = time.time()
        hashed_text = hashlib.new(algorithm, text.encode())
        end_time = time.time()

        calc_time = end_time - start_time

        results.append({
            algorithm,
            calc_time,
            hashed_text,
        })

        print(f"Hashing algorithm: {str(algorithm)}")
        print(f"Hashing time: {calc_time:.6f}s")
        print()
    return results

# File Hashing
def hash_file(hashing_algorithm, file_path):
    if hashing_algorithm not in hashlib.algorithms_available:
        raise ValueError("Algorithm not available in hashlib!")

    hasher = hashlib.new(hashing_algorithm)
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)
        file_hash = hasher.hexdigest()
    return file_hash


def check_file_hash(file_path, expected_hash, algorithm):
    hashed_file = hash_file(algorithm, file_path)
    if str(hashed_file) == str(expected_hash):
        print("Hash is valid!")
        return True
    else:
        print("Hash is not valid!")
        return False

# Messages hashing


def gen_message(size):
    return "a" * size


def messages_hashing_bechmark(hashing_algorithm):
    sizes = [100, 1000, 10000, 100000, 1000000]
    times = []

    for size in sizes:
        message = gen_message(size)
        time_data = timeit.timeit(lambda: hashlib.new(hashing_algorithm, message.encode()), number=100)
        times.append(time_data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sizes, y=times, name="SHA-256"))
    fig.update_layout(title="Szybkość generowania hashy", xaxis_title="Rozmiar wiadomości (bajty)",
                      yaxis_title="Czas (sekundy)")
    fig.show()


def main():
    # 1. Using every hashing algorithm in algorithms_avaliable in hashlib
    hashing_algs()

    # 2./3. Hash and verify ubuntu.iso file hash
    check_file_hash("/ubuntu.iso", "071d5a534c1a2d61d64c6599c47c992c778e08b054daecc2540d57929e4ab1fd", "sha256")

    # 3. Benchmark messages hashing
    messages_hashing_bechmark("md5")


if __name__ == '__main__':
    main()