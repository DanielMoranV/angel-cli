import sys
import subprocess
from mcp.server.fastmcp import FastMCP

# Inicializar servidor FastMCP
mcp = FastMCP("Angel")

@mcp.tool()
def get_angel_status() -> str:
    """
    Obtiene el estado actual de las tareas activas y los módulos vigentes/obsoletos del proyecto.
    Úsalo antes de modificar archivos para saber en qué tarea debes trabajar.
    """
    try:
        result = subprocess.run(["angel", "status", "--all"], capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error ejecutando angel status: {e}"

@mcp.tool()
def create_angel_task(title: str, task_type: str = "feature") -> str:
    """
    Crea una nueva tarea estructurada en Angel.
    Tipos permitidos: bug, feature, refactor, docs.
    Devuelve el ID de la tarea creada (ej. T-001).
    """
    try:
        result = subprocess.run(
            ["angel", "new-task", "--title", title, "--task-type", task_type],
            capture_output=True, text=True
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error ejecutando angel new-task: {e}"

@mcp.tool()
def close_angel_task(task_id: str) -> str:
    """
    Marca una tarea (ej. T-001) como completada cuando se ha cumplido su criterio de aceptación.
    """
    try:
        result = subprocess.run(["angel", "close", task_id], capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error ejecutando angel close: {e}"

@mcp.tool()
def update_angel_module(module_name: str) -> str:
    """
    Sincroniza la memoria de un módulo (ej. autenticacion) con el Git SHA actual.
    Úsalo después de haber verificado que los cambios en el código son correctos.
    """
    try:
        result = subprocess.run(["angel", "update-module", module_name], capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error ejecutando angel update-module: {e}"

if __name__ == "__main__":
    mcp.run()
