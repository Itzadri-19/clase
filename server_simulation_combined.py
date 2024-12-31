import multiprocessing
import threading
import time
import sys
import os

def process_request(user_id):
    """Simula la venta de una entrada para un usuario."""
    try:
        time.sleep(2)  # Simulamos 2 segundos de procesamiento por usuario.
    except Exception as e:
        print(f"Error procesando usuario {user_id}: {e}")

def process_chunk_with_threads(user_ids, num_threads):
    """Procesa un grupo de usuarios usando un número limitado de hilos."""
    semaphore = threading.Semaphore(num_threads)  # Limitar hilos activos

    def thread_worker(user_id):
        with semaphore:  # Controla el acceso concurrente
            process_request(user_id)

    threads = []
    for user_id in user_ids:
        thread = threading.Thread(target=thread_worker, args=(user_id,))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

def simulate_server_combined(num_processes, num_threads, num_users=1000):
    """Simula un servidor usando multiprocessing y threading."""
    max_processes = multiprocessing.cpu_count()
    if num_processes > max_processes:
        print(f"Ajustando num_processes a {max_processes} (máximos núcleos disponibles).")
        num_processes = max_processes

    print(f"Simulando con {num_processes} procesos y {num_threads} hilos por proceso...")
    start_time = time.time()

    # Dividir usuarios en grupos para los procesos
    user_ids = list(range(num_users))
    chunk_size = len(user_ids) // num_processes
    process_chunks = [
        user_ids[i * chunk_size: (i + 1) * chunk_size] if i < num_processes - 1
        else user_ids[i * chunk_size:]
        for i in range(num_processes)
    ]

    # Crear procesos
    processes = []
    for chunk in process_chunks:
        process = multiprocessing.Process(target=process_chunk_with_threads, args=(chunk, num_threads))
        processes.append(process)
        process.start()

    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total con {num_processes} procesos y {num_threads} hilos por proceso: {total_time:.2f} segundos")
    return total_time

if __name__ == "__main__":
    # Leer argumentos desde la línea de comandos
    if len(sys.argv) != 3:
        print("Uso: python server_simulation_combined.py <num_processes> <num_threads>")
        sys.exit(1)

    num_processes = int(sys.argv[1])
    num_threads = int(sys.argv[2])

    print(f"CPU disponibles: {multiprocessing.cpu_count()}")
    simulate_server_combined(num_processes, num_threads)
