import threading
import time
import sys

def process_request(user_id):
    """Simula la venta de una entrada para un usuario."""
    # Simulamos que la venta de una entrada tarda 2 segundos
    time.sleep(2)

def simulate_server(num_threads, num_users=1000):
    """Simula un servidor para la venta de entradas usando threading."""
    print(f"Simulando con {num_threads} hilos y {num_users} usuarios...")
    start_time = time.time()

    # Dividimos los usuarios en grupos por el número de hilos
    user_ids = list(range(num_users))
    chunk_size = len(user_ids) // num_threads
    threads = []

    # Crear y lanzar los hilos
    for i in range(num_threads):
        start = i * chunk_size
        # Asegurarnos de incluir los usuarios restantes en el último hilo
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(user_ids)
        thread = threading.Thread(target=process_chunk, args=(user_ids[start:end],))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total con {num_threads} hilos: {total_time:.2f} segundos")
    return total_time

def process_chunk(user_ids):
    """Procesa un grupo de usuarios."""
    for user_id in user_ids:
        process_request(user_id)

if __name__ == "__main__":
    # Leer el número de hilos desde los argumentos
    if len(sys.argv) != 2:
        print("Uso: python server_simulation_threading.py <num_threads>")
        sys.exit(1)

    num_threads = int(sys.argv[1])
    simulate_server(num_threads)
