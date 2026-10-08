import typer
import shutil
from pathlib import Path
from rich.console import Console

app = typer.Typer(help="Angel CLI - Framework de Agentes IA")
console = Console()

# Ruta base donde se instaló el paquete para buscar los templates
PACKAGE_DIR = Path(__file__).parent
TEMPLATES_DIR = PACKAGE_DIR / "templates"

@app.command()
def init(
    force: bool = typer.Option(False, "--force", "-f", help="Sobrescribir si ya existe la carpeta .angel/")
):
    """
    Inicializa Angel en el repositorio actual copiando las plantillas a .angel/
    """
    target_dir = Path.cwd() / ".angel"
    
    if target_dir.exists():
        if not force:
            console.print("[yellow]La carpeta .angel/ ya existe. Usa --force para sobrescribir.[/yellow]")
            raise typer.Exit(code=1)
        else:
            shutil.rmtree(target_dir)
            console.print("[yellow]Carpeta .angel/ anterior eliminada.[/yellow]")

    try:
        shutil.copytree(TEMPLATES_DIR, target_dir)
        
        # Crear subdirectorios para estado dinámico
        (target_dir / "tareas").mkdir(exist_ok=True)
        (target_dir / "modulos").mkdir(exist_ok=True)
        
        console.print("[green]✔ Angel inicializado correctamente en .angel/[/green]")
        console.print("Revisa y configura [bold].angel/perfil.yaml[/bold] con los datos de tu proyecto.")
        
    except Exception as e:
        console.print(f"[red]Error al inicializar Angel: {e}[/red]")
        raise typer.Exit(code=1)

@app.command()
def status(
    show_all: bool = typer.Option(False, "--all", "-a", help="Mostrar todas las tareas, incluyendo completadas.")
):
    """
    Muestra el estado actual del proyecto (tareas activas y estado de módulos).
    """
    import yaml
    from rich.table import Table

    target_dir = Path.cwd() / ".angel"
    if not target_dir.exists():
        console.print("[red]Angel no está inicializado aquí. Ejecuta 'angel init' primero.[/red]")
        raise typer.Exit(code=1)
        
    tareas_dir = target_dir / "tareas"
    
    tareas = []
    if tareas_dir.exists():
        for md_file in tareas_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        if frontmatter:
                            tareas.append(frontmatter)
            except Exception as e:
                console.print(f"[red]Error leyendo {md_file.name}: {e}[/red]")

    if not show_all:
        tareas = [t for t in tareas if t.get("status", "").lower() != "completada"]

    if not tareas:
        if show_all:
            console.print("[cyan]No hay tareas registradas en .angel/tareas/.[/cyan]")
        else:
            console.print("[green]No hay tareas pendientes. ¡Todo al día![/green]")
        return

    table = Table(title="Estado de Tareas (Angel)")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Tipo", style="magenta")
    table.add_column("Estado", style="bold")
    table.add_column("Título")

    # Ordenar por ID
    for t in sorted(tareas, key=lambda x: str(x.get("id", ""))):
        estado = str(t.get("status", "N/A")).lower()
        color = "green" if estado == "activa" else ("yellow" if estado == "pausada" else ("red" if estado == "bloqueada" else "white"))
        
        table.add_row(
            str(t.get("id", "N/A")),
            str(t.get("type", "N/A")),
            f"[{color}]{estado}[/{color}]",
            str(t.get("title", "N/A"))
        )
        
    console.print(table)

@app.command(name="new-task")
def new_task(
    title: str = typer.Option(..., prompt="Título de la tarea"),
    task_type: str = typer.Option("feature", prompt="Tipo (bug, feature, refactor, docs)"),
):
    """
    Crea una nueva tarea en .angel/tareas/ con un ID autoincremental.
    """
    import datetime
    import re
    
    target_dir = Path.cwd() / ".angel"
    if not target_dir.exists():
        console.print("[red]Angel no está inicializado. Ejecuta 'angel init' primero.[/red]")
        raise typer.Exit(code=1)
        
    tareas_dir = target_dir / "tareas"
    
    # Calcular el próximo ID
    max_id = 0
    if tareas_dir.exists():
        for md_file in tareas_dir.glob("T-*.md"):
            match = re.search(r"T-(\d+)", md_file.name)
            if match:
                num = int(match.group(1))
                if num > max_id:
                    max_id = num
                
    next_id_num = max_id + 1
    next_id = f"T-{next_id_num:03d}"
    
    # Crear slug para el nombre del archivo
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    if not slug:
        slug = "tarea"
    filename = f"{next_id}-{slug}.md"
    filepath = tareas_dir / filename
    
    # Leer plantilla
    template_path = target_dir / "PLANTILLA_TAREA.md"
    if not template_path.exists():
        console.print("[red]No se encontró la plantilla .angel/PLANTILLA_TAREA.md[/red]")
        raise typer.Exit(code=1)
        
    content = template_path.read_text(encoding="utf-8")
    
    # Reemplazar valores básicos
    today = datetime.date.today().isoformat()
    content = content.replace('id: "T-001"', f'id: "{next_id}"')
    content = content.replace('title: "Breve descripción de la tarea"', f'title: "{title}"')
    content = content.replace('type: "bug | feature | refactor | docs"', f'type: "{task_type}"')
    content = content.replace('status: "activa | pausada | bloqueada | completada"', 'status: "activa"')
    content = content.replace('created_at: "YYYY-MM-DD"', f'created_at: "{today}"')
    content = content.replace('updated_at: "YYYY-MM-DD"', f'updated_at: "{today}"')
    
    filepath.write_text(content, encoding="utf-8")
    
    console.print(f"[green]✔ Tarea {next_id} creada exitosamente:[/green] {filepath.name}")

@app.command(name="close")
def close_task(
    task_id: str = typer.Argument(..., help="ID de la tarea a cerrar (ej. T-001)")
):
    """
    Marca una tarea como completada y actualiza su fecha.
    """
    import datetime
    import re
    
    target_dir = Path.cwd() / ".angel"
    tareas_dir = target_dir / "tareas"
    
    if not tareas_dir.exists():
        console.print("[red]Angel no está inicializado aquí.[/red]")
        raise typer.Exit(code=1)
        
    target_file = None
    for md_file in tareas_dir.glob("*.md"):
        if task_id.upper() in md_file.name.upper():
            target_file = md_file
            break
            
    if not target_file:
        console.print(f"[red]No se encontró ninguna tarea con el ID {task_id}[/red]")
        raise typer.Exit(code=1)
        
    content = target_file.read_text(encoding="utf-8")
    
    # Reemplazar estado
    new_content = re.sub(r'status:\s*".*"', 'status: "completada"', content)
    today = datetime.date.today().isoformat()
    new_content = re.sub(r'updated_at:\s*".*"', f'updated_at: "{today}"', new_content)
    
    target_file.write_text(new_content, encoding="utf-8")
    console.print(f"[green]✔ Tarea {task_id} marcada como completada exitosamente.[/green]")

@app.command(name="handoff")
def handoff(
    task_id: str = typer.Argument(..., help="ID de la tarea para generar el paquete de contexto")
):
    """
    Genera un paquete de contexto (prompt) para continuar la tarea en otro LLM o chat.
    """
    from rich.panel import Panel
    
    target_dir = Path.cwd() / ".angel"
    tareas_dir = target_dir / "tareas"
    
    target_file = None
    if tareas_dir.exists():
        for md_file in tareas_dir.glob("*.md"):
            if task_id.upper() in md_file.name.upper():
                target_file = md_file
                break
            
    if not target_file:
        console.print(f"[red]No se encontró la tarea {task_id}[/red]")
        raise typer.Exit(code=1)
        
    perfil_file = target_dir / "perfil.yaml"
    perfil_content = perfil_file.read_text(encoding="utf-8") if perfil_file.exists() else "Sin perfil."
    task_content = target_file.read_text(encoding="utf-8")
    
    handoff_text = f"""[INICIO DE HANDOFF]
Por favor, actúa bajo el framework Angel. Retomaremos esta tarea:

--- PERFIL DEL PROYECTO ---
{perfil_content}

--- ESTADO DE LA TAREA ({task_id}) ---
{task_content}

Instrucción: Confirma que entiendes el objetivo y sugiere el siguiente paso técnico.
[FIN DE HANDOFF]"""
    
    console.print(Panel(handoff_text, title="Copia y pega este texto en tu nuevo LLM", border_style="blue"))

if __name__ == "__main__":
    app()
