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

if __name__ == "__main__":
    app()
