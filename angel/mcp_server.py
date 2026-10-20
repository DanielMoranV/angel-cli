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


@mcp.tool()
def read_angel_task(task_id: str) -> str:
    """
    Lee todo el contenido (frontmatter y cuerpo) de una tarea específica en Angel.
    Úsalo para obtener los detalles técnicos antes de empezar a trabajar.
    """
    import os
    from pathlib import Path
    
    custom_dir = os.environ.get("ANGEL_DIR")
    if custom_dir:
        target_dir = Path.cwd() / custom_dir
    else:
        docs_ia = Path.cwd() / "Docs" / "IA"
        target_dir = docs_ia if docs_ia.exists() and docs_ia.is_dir() else Path.cwd() / ".angel"
    tareas_dir = target_dir / "TAREAS" if (target_dir / "TAREAS").exists() else target_dir / "tareas"
    
    if not tareas_dir.exists():
        return "Error: No se encontró la carpeta de tareas de Angel."
        
    for md_file in tareas_dir.glob("*.md"):
        if task_id.upper() in md_file.name.upper():
            return md_file.read_text(encoding="utf-8")
            
    return f"Error: Tarea {task_id} no encontrada."

@mcp.tool()
def append_task_progress(task_id: str, content: str) -> str:
    """
    Añade un texto o viñeta de progreso a la tarea especificada de forma segura.
    El contenido se añadirá al final del archivo.
    """
    import os
    from pathlib import Path
    import datetime
    
    
    custom_dir = os.environ.get("ANGEL_DIR")
    if custom_dir:
        target_dir = Path.cwd() / custom_dir
    else:
        docs_ia = Path.cwd() / "Docs" / "IA"
        target_dir = docs_ia if docs_ia.exists() and docs_ia.is_dir() else Path.cwd() / ".angel"
    tareas_dir = target_dir / "TAREAS" if (target_dir / "TAREAS").exists() else target_dir / "tareas"
    
    target_file = None
    if tareas_dir.exists():
        for md_file in tareas_dir.glob("*.md"):
            if task_id.upper() in md_file.name.upper():
                target_file = md_file
                break
                
    if not target_file:
        return f"Error: Tarea {task_id} no encontrada."
        
    try:
        import frontmatter
        post = frontmatter.load(target_file)
        post.metadata["updated_at"] = datetime.date.today().isoformat()
        
        # Append content
        post.content += f"\n- **Avance:** {content}\n"
        
        target_file.write_text(frontmatter.dumps(post), encoding="utf-8")
        return f"Progreso añadido correctamente a {task_id}."
    except Exception as e:
        return f"Error al modificar tarea: {e}"

@mcp.tool()
def check_module_drift(module_name: str) -> str:
    """
    Verifica qué ha cambiado exactamente en los archivos de un módulo
    desde la última vez que su memoria (git_sha) fue actualizada.
    Devuelve un diff detallado.
    """
    import os
    from pathlib import Path
    import yaml
    import subprocess
    
    
    custom_dir = os.environ.get("ANGEL_DIR")
    if custom_dir:
        target_dir = Path.cwd() / custom_dir
    else:
        docs_ia = Path.cwd() / "Docs" / "IA"
        target_dir = docs_ia if docs_ia.exists() and docs_ia.is_dir() else Path.cwd() / ".angel"
    modulos_dir = target_dir / "MODULOS" if (target_dir / "MODULOS").exists() else target_dir / "modulos"
    
    if not modulos_dir.exists():
        return "Error: Carpeta modulos no existe."
        
    target_file = None
    for md_file in modulos_dir.glob("*.md"):
        if module_name.lower() in md_file.name.lower():
            target_file = md_file
            break
            
    if not target_file:
        return f"Error: Módulo {module_name} no encontrado."
        
    try:
        content = target_file.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        if len(parts) < 3:
            return "Error: Formato YAML inválido en el módulo."
            
        fm = yaml.safe_load(parts[1])
        git_sha = fm.get("git_sha")
        paths = fm.get("paths_covered", [])
        
        if not git_sha or git_sha == "HEAD":
            return "El módulo no tiene un git_sha registrado aún (es HEAD)."
            
        import re
        if not re.match(r"^[a-fA-F0-9]{4,40}$", git_sha):
            return f"Error: git_sha inválido '{git_sha}'."
            
        if not paths:
            return "El módulo no define paths_covered."
            
        cmd = ["git", "diff", f"{git_sha}..HEAD", "--"] + paths
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if not res.stdout.strip():
            return "El módulo está perfectamente vigente. Ningún archivo cubierto ha cambiado."
            
        return f"Módulo obsoleto. Cambios detectados:\n\n{res.stdout}"
    except Exception as e:
        return f"Error revisando drift: {e}"

if __name__ == "__main__":
    mcp.run()
