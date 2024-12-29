import paramiko
import os
from datetime import datetime
from getpass import getpass

def run_remote_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if error:
        print(f"Error ejecutando '{command}': {error}")
    return output

def transfer_files_via_sftp(host, port, username, password, remote_files, local_path):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        for remote_file in remote_files:
            local_file = os.path.join(local_path, os.path.basename(remote_file))
            print(f"Descargando {remote_file} a {local_file}...")
            sftp.get(remote_file, local_file)

        sftp.close()
        transport.close()
    except Exception as e:
        raise Exception(f"Error en la transferencia de archivos: {e}")

def main():
    # Solicitar datos al usuario
    username = input("Ingrese el nombre de usuario: ")
    password = getpass("Ingrese la contraseña: ")

    # Ruta de la carpeta con las listas de hosts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lists_folder = os.path.join(current_dir, "Lists")
    if not os.path.isdir(lists_folder):
        print("La carpeta 'Lists' no existe en el directorio del script.")
        return

    errors = []  # Lista para almacenar errores

    # Procesar cada archivo en la carpeta
    for list_file in os.listdir(lists_folder):
        list_path = os.path.join(lists_folder, list_file)
        if not os.path.isfile(list_path):
            continue

        print(f"Procesando archivo de lista: {list_file}")

        # Crear carpeta para guardar los archivos descargados
        download_path = os.path.join(os.path.expanduser("~/Downloads"), os.path.splitext(list_file)[0])
        os.makedirs(download_path, exist_ok=True)

        # Leer hosts y puertos del archivo
        with open(list_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                try:
                    host, port = line.split(":")
                    port = int(port)

                    # Conexión SSH
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, port=port, username=username, password=password, disabled_algorithms={"mac": ["hmac-md5"]})

                    # Obtener el nombre del dispositivo
                    identity = run_remote_command(ssh, "/system identity print").split(":")[-1].strip()
                    identity = identity.replace(" ", "_")  # Reemplazar espacios con guiones bajos
                    print(f"Identidad del sistema: {identity}")

                    # Generar nombre dinámico para los archivos
                    date = datetime.now().strftime("%Y-%m-%d")
                    file_name = f"MK-{identity}-{date}"

                    # Crear export y backup
                    run_remote_command(ssh, f"export file={file_name}")
                    run_remote_command(ssh, f"system backup save dont-encrypt=no name={file_name}")
                    print(f"Export y backup creados con el nombre: {file_name}")

                    ssh.close()

                    # Transferir archivos con SFTP
                    remote_files = [f"/{file_name}.backup", f"/{file_name}.rsc"]
                    transfer_files_via_sftp(host, port, username, password, remote_files, download_path)

                    # Reconectar para eliminar los archivos remotos
                    ssh.connect(host, port=port, username=username, password=password, disabled_algorithms={"mac": ["hmac-md5"]})
                    run_remote_command(ssh, f"file remove {file_name}.backup,{file_name}.rsc")
                    print(f"Archivos remotos {file_name}.backup y {file_name}.rsc eliminados.")

                    ssh.close()

                except Exception as e:
                    error_message = f"Error procesando {line}: {e}"
                    print(error_message)
                    errors.append(error_message)

    # Mostrar errores al final
    if errors:
        print("\nErrores encontrados durante la ejecución:")
        for error in errors:
            print(error)

if __name__ == "__main__":
    main()
