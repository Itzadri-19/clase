import multiprocessing
import time
import sys

def process_request(user_id):
    """Simula la venta de una entrada para un usuario."""
    # Simulamos que la venta de una entrada tarda 2 segundos
    time.sleep(2)
    return f"Processed user {user_id}"

def simulate_server(num_processes, num_users=1000):
    """Simula un servidor para la venta de entradas con los parámetros dados."""
    print(f"Simulando con {num_processes} procesos y {num_users} usuarios...")
    start_time = time.time()

    # Creamos un pool de procesos
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Simulamos que cada usuario genera una solicitud
        user_ids = list(range(num_users))
        results = pool.map(process_request, user_ids)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total con {num_processes} procesos: {total_time:.2f} segundos")
    return total_time

if __name__ == "__main__":
    # Leer el número de procesos desde los argumentos
    if len(sys.argv) != 2:
        print("Uso: python server_simulation.py <num_processes>")
        sys.exit(1)

    num_processes = int(sys.argv[1])
    simulate_server(num_processes)
