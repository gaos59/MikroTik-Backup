# Backup y Exportación Automática de Dispositivos Mikrotik

Este script en Python permite automatizar la exportación y creación de respaldos de configuraciones en dispositivos Mikrotik. Los archivos generados se descargan automáticamente al equipo local del usuario y se eliminan del dispositivo remoto una vez completada la transferencia.

## Requisitos

- **Python 3.7+**: Este script requiere una versión actualizada de Python instalada en tu sistema.
- **Biblioteca `paramiko`**: Utilizada para conexiones SSH y transferencia SFTP.
  - Puedes instalarla ejecutando:  
    ```bash
    pip install paramiko
    ```
- **Acceso SSH**: El script requiere credenciales válidas para conectarse a los dispositivos Mikrotik.
- **Estructura del Directorio**:
  - Una carpeta llamada `Lists` debe estar en el mismo directorio que el script.
  - Dentro de esta carpeta, coloca archivos de texto con listas de hosts en el formato `ip:puerto`, uno por línea.

## Funcionamiento

1. **Ingreso de Credenciales**: Al ejecutar el script, el usuario debe proporcionar su nombre de usuario y contraseña para acceder a los dispositivos.

2. **Lectura de Hosts**: El script lee los archivos de la carpeta `Lists`, que contienen direcciones IP y puertos de los dispositivos a procesar.

3. **Conexión SSH**: Se establece una conexión SSH con cada dispositivo para:
   - Obtener el nombre del dispositivo.
   - Crear un archivo de exportación (`.rsc`) y un respaldo (`.backup`).

4. **Transferencia de Archivos**: Los archivos generados se descargan automáticamente al equipo local en la carpeta `~/Downloads/[nombre_del_archivo]`.

5. **Eliminación de Archivos Remotos**: Una vez descargados, los archivos se eliminan del dispositivo remoto para mantener el almacenamiento limpio.

6. **Manejo de Errores**: Cualquier problema durante la ejecución se registra y se muestra al final.

## Uso

1. Asegúrate de que la carpeta `Lists` contiene los archivos con las direcciones IP y puertos en el formato adecuado.
   
2. Ejecuta el script desde la terminal:
   ```bash
   python backup.py
3. Proporciona las credenciales solicitadas.  
4. Revisa la carpeta `~/Downloads` para los respaldos descargados.

## Formato de los Archivos en `Lists`

Cada archivo debe contener las direcciones IP y puertos en el siguiente formato:

```plaintext
192.168.1.1:22  
192.168.1.2:2222  
# Comentarios comienzan con #
```
## Ejemplo de Salida

Al ejecutar el script, verás mensajes como los siguientes:

```plaintext
Procesando archivo de lista: dispositivos.txt  
Conectando a 192.168.1.1:22...  
Identidad del sistema: Router1  
Export y backup creados con el nombre: MK-Router1-2024-12-29  
Descargando /MK-Router1-2024-12-29.backup a ~/Downloads/dispositivos/MK-Router1-2024-12-29.backup...  
Archivos remotos eliminados.
```
## Notas

- El script maneja conexiones fallidas, mostrando los errores al final.
- Si no existe la carpeta `Lists`, el script finalizará con un mensaje de error.

## Contribuciones

¡Tu retroalimentación y contribuciones son bienvenidas! Si tienes ideas para mejorar el script, abre un issue o envía un pull request.
