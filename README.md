<div align="center">
  <h1>👼 Angel CLI</h1>
  <p><b>Un sistema de gestión de estado estructurado y predecible para flujos de trabajo con Agentes de Inteligencia Artificial.</b></p>
</div>

---

**Angel** no es un modelo de IA. Es un **framework agnóstico** (escrito en Python) diseñado para resolver los tres problemas más grandes al programar con asistentes como Claude Code, Cursor, Antigravity o ChatGPT:

1. **La pérdida de contexto:** Cuando el chat se hace muy largo y la IA "olvida" el objetivo original.
2. **La falta de trazabilidad:** Cuando la IA cambia archivos sin un criterio claro o un ticket asignado.
3. **La sincronización:** Cuando usas la app web en tu móvil para investigar, y luego pasas a tu IDE en la computadora para programar.

Con Angel, la **fuente de la verdad deja de ser la memoria del LLM y pasa a ser tu repositorio de Git**, a través de archivos Markdown y YAML perfectamente estructurados.

## ✨ Características Principales

- 🗂️ **Estado Determinista (YAML + Markdown):** Gestiona tareas con IDs estructurados, estado (`activa`, `pausada`, `bloqueada`, `completada`) y frontmatter parseable.
- 🔄 **Handoffs (Transferencias):** Transfiere todo el contexto de una tarea compleja de un LLM a otro (ej. de ChatGPT a Claude) con un solo comando.
- 🔒 **Validación por Git SHA:** Angel comprueba si las "memorias" que generó la IA sobre tu código están obsoletas usando un cruce con el historial de tu repositorio (`git diff`).
- 🤖 **Servidor FastMCP Nativo:** Angel actúa como un servidor *Model Context Protocol*, exponiendo 7 herramientas nativas directamente al cerebro de tu IA (Cursor, Antigravity, Claude Desktop, etc.).
- 📡 **Escáner de Stack:** Infiere automáticamente los lenguajes, frameworks y gestores de paquetes de tu proyecto para dárselos a conocer a la IA.
- 📦 **Soporte Flexible de Monorepos:** Compatible con directorios personalizados mediante la variable `ANGEL_DIR` o detección automática de `Docs/IA/`.

---

## 🚀 Instalación

Puedes clonar e instalar el paquete en modo editable con soporte MCP:

```bash
git clone https://github.com/DanielMoranV/angel-cli.git
cd angel-cli
pip install -e .[mcp]
```

*Nota: Requiere Python 3.10 o superior y Git instalado en tu sistema.*

---

## 🛠️ Uso y Comandos CLI

### 1. Inicializar y Escanear un Proyecto
Ve a cualquier repositorio donde quieras trabajar con IA y ejecuta:
```bash
angel init
angel scan
```
Esto creará la estructura `.angel/`, escaneará tu código (detectando si usas React, FastAPI, Go, Django, etc.) y dejará listo tu `perfil.yaml` y la plantilla de reglas `ANGEL.md`.
> **Tip:** Usa `angel init --force` (o `-f`) si deseas restablecer la estructura inicial.

### 2. Crear una Tarea
Formaliza la instrucción para tu IA en lugar de hacer peticiones al aire:
```bash
angel new-task --title "Arreglar bug de login en iOS" --task-type bug
```
Generará automáticamente un archivo como `.angel/tareas/T-001-a4f2-arreglar-bug-de-login-en-ios.md` con un hash único para evitar colisiones entre ramas paralelas.

Si prefieres un identificador semántico propio, usa `--id`:
```bash
angel new-task --title "Flujo de autenticación" --task-type feature --id feat-auth
```

### 3. Revisar el Estado del Proyecto
Consulta las tareas activas y la vigencia de los módulos de memoria:
```bash
angel status
```
Para ver el historial completo, incluyendo tareas ya completadas:
```bash
angel status --all
```

### 4. Actualizar Memoria de Módulo
Cuando actualices el código cubierto por un módulo, vincula su memoria al commit actual (`HEAD`):
```bash
angel update-module auth
```

### 5. Continuar en Otro Chat (Handoff)
Si la ventana de contexto de la IA está saturada o quieres cambiar de proveedor (ej. llevarte la tarea de Claude a ChatGPT):
```bash
angel handoff T-001
```
*(Puedes usar cualquier fragmento del ID o slug; Angel buscará la coincidencia automáticamente).*

### 6. Cerrar Tarea
Marca la tarea como `completada` registrando la fecha de cierre:
```bash
angel close T-001
```

---

## 🧠 Integración con Reglas de IA (`ANGEL.md`)

Al inicializar Angel, se genera el archivo `.angel/ANGEL.md`. Este archivo contiene las directrices de comportamiento que gobiernan cómo debe actuar cualquier modelo de lenguaje cuando interactúa con tu proyecto:

- **Comandos conversacionales:** `Hola Angel`, `Angel, estado`, `Angel, nuevo chat`, `Angel, cerrar tarea`.
- **Vías de acción:** Exigencias estrictas para bugs (reproducción, logs), features (alcance) y refactors.
- **Higiene de contexto:** Prohibición de desviarse de la tarea activa o realizar commits sin autorización.

> **Recomendación:** Si usas **Cursor**, **Claude Code** o **Antigravity**, enlaza este archivo en tus reglas del proyecto (por ejemplo, en `.cursorrules` o `CLAUDE.md`):
> ```markdown
> Lee y respeta las directrices operativas en .angel/ANGEL.md y .angel/perfil.yaml
> ```

---

## 🔌 Integración Nativa con IDEs (Servidor FastMCP)

Angel implementa un servidor MCP nativo. Esto permite que asistentes como **Antigravity**, **Cursor** o **Claude Desktop** ejecuten acciones de Angel de forma transparente como herramientas de su propio entorno.

### Configuración MCP
Añade la siguiente configuración a tu cliente MCP (por ejemplo en `~/.gemini/config/mcp_config.json` para Antigravity o en los ajustes de Cursor):

```json
{
  "mcpServers": {
    "angel": {
      "command": "angel",
      "args": ["mcp"]
    }
  }
}
```

### Herramientas MCP Disponibles

| Herramienta | Parámetros | Descripción |
| :--- | :--- | :--- |
| `get_angel_status` | *(ninguno)* | Obtiene el tablero de tareas activas y el estado de obsolescencia de los módulos. |
| `create_angel_task` | `title`, `task_type` | Crea una nueva tarea estructurada (`bug`, `feature`, `refactor`, `docs`). |
| `read_angel_task` | `task_id` | Lee el contenido íntegro y los criterios de aceptación de una tarea específica. |
| `append_task_progress` | `task_id`, `content` | Añade notas de avance a la tarea sin alterar el frontmatter. |
| `check_module_drift` | `module_name` | Compara los archivos cubiertos por un módulo contra el Git SHA y devuelve el `git diff` de los cambios no documentados. |
| `update_angel_module` | `module_name` | Sincroniza el Git SHA del módulo con el commit actual (`HEAD`). |
| `close_angel_task` | `task_id` | Marca una tarea como completada tras cumplir sus criterios de aceptación. |

---

## ⚙️ Configuración Avanzada y Monorepos

Por defecto, Angel opera sobre la carpeta `.angel/` en la raíz del proyecto. Sin embargo, cuenta con mecanismos flexibles para adaptarse a diferentes arquitecturas:

1. **Detección Automática de `Docs/IA`:** Si tu proyecto contiene una carpeta `Docs/IA/`, Angel la utilizará automáticamente como su directorio principal en lugar de `.angel/`.
2. **Variable de Entorno `ANGEL_DIR`:** Puedes definir una ruta personalizada para monorepos o esquemas de documentación compartidos:
   ```bash
   export ANGEL_DIR="packages/api/.angel"
   angel status
   ```
3. **Tolerancia a mayúsculas:** Admite tanto `tareas/` y `modulos/` como `TAREAS/` y `MODULOS/`.

---

## 🛣️ Roadmap

- [x] **Fase 1:** Plantillas base y diseño agnóstico (`perfil.yaml`, `ANGEL.md`, plantillas).
- [x] **Fase 2:** Comandos de ciclo de vida (`init`, `new-task`, `status`, `handoff`, `close`).
- [x] **Fase 3:** Validación inteligente de obsolescencia usando Git SHAs.
- [x] **Fase 4:** Escáner Automático (`angel scan`) de lenguajes y arquitecturas.
- [x] **Fase 5:** Adaptadores nativos para IDEs y Servidor MCP (FastMCP con 7 herramientas nativas).

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.
