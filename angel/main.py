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
def status():
    """
    Muestra el estado actual del proyecto (tareas activas y estado de módulos).
    """
    target_dir = Path.cwd() / ".angel"
    if not target_dir.exists():
        console.print("[red]Angel no está inicializado aquí. Ejecuta 'angel init' primero.[/red]")
        raise typer.Exit(code=1)
        
    console.print("[cyan]Angel Status:[/cyan] (Comando en construcción)")
    # TODO: Implementar lectura de tareas en YAML y estado Git de módulos

if __name__ == "__main__":
    app()
