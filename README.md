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

- 🗂️ **Estado Determínista (YAML + Markdown):** Gestiona tareas con IDs autoincrementales, estado (`activa`, `bloqueada`, `completada`) y frontmatter estructurado.
- 🔄 **Handoffs (Transferencias):** Transfiere todo el contexto de una tarea compleja de un LLM a otro (ej. de ChatGPT a Claude) con un solo comando.
- 🔒 **Validación por Git SHA:** Angel comprueba si las "memorias" que generó la IA sobre tu código están obsoletas usando un cruce con el historial de tu repositorio (`git diff`).
- 🤖 **Servidor MCP Nativo:** Angel actúa como un servidor *Model Context Protocol*, exponiendo herramientas nativas directamente al cerebro de tu IA (Cursor, Antigravity, etc.).
- 📡 **Escáner de Stack:** Infiere automáticamente los lenguajes, frameworks y gestores de paquetes de tu proyecto para dárselos a conocer a la IA.

---

## 🚀 Instalación

Por el momento, puedes instalar el paquete de forma global usando `pip`:

```bash
git clone git@github.com:DanielMoranV/angel-cli.git
cd angel-cli
pip install -e .
# Si quieres usar la integración nativa con IDEs, asegúrate de instalar las dependencias:
pip install mcp
```

*Nota: Requiere Python 3.9 o superior y Git instalado en tu sistema.*

---

## 🛠️ Uso y Comandos CLI

### 1. Inicializar y Escanear un Proyecto
Ve a cualquier repositorio donde quieras trabajar con IA y ejecuta:
```bash
angel init
angel scan
```
Esto creará una carpeta oculta `.angel/`, escaneará tu código (detectando si usas React, Go, Python, etc.) y dejará listo tu `perfil.yaml`.

### 2. Crear una Tarea
Formaliza la instrucción para tu IA en lugar de hacer peticiones al aire:
```bash
angel new-task --title "Arreglar bug de login en iOS" --task-type bug
```
*(Generará automáticamente el archivo `.angel/tareas/T-001-arreglar-bug-de-login-en-ios.md`)*

### 3. Revisar el Estado
Para saber qué tareas están activas y qué módulos están desactualizados:
```bash
angel status
```

### 4. Actualizar Memoria de Módulo
Fuerza la actualización de la memoria de un módulo vinculándola al commit actual (`HEAD`):
```bash
angel update-module auth
```

### 5. Continuar en Otro Chat (Handoff)
Si la ventana de contexto de la IA está a punto de explotar o quieres cambiar de proveedor (ej. llevarte la tarea a ChatGPT):
```bash
angel handoff T-001
```
*(Copia el texto gigante que te devuelve la terminal y pégalo en el nuevo chat).*

### 6. Cerrar Tarea
```bash
angel close T-001
```

---

## 🔌 Integración nativa con IDEs (Servidor MCP)

Angel incluye un servidor MCP integrado (`FastMCP`) que expone herramientas directamente a tu IA. En lugar de ejecutar comandos en la terminal a mano, tu IDE (como **Antigravity**, **Claude Desktop** o **Cursor**) puede crear tareas y leer estados como si fueran sus propias funciones.

Para configurarlo, solo debes añadir Angel a tu archivo de configuración de MCP. Por ejemplo, en Antigravity (en `~/.gemini/config/mcp_config.json` o en tu plugin local):

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

Al hacerlo, la IA detectará automáticamente herramientas como `create_angel_task`, `get_angel_status`, etc.

---

## 🛣️ Roadmap

- [x] **Fase 1:** Plantillas base y diseño agnóstico.
- [x] **Fase 2:** Comandos de ciclo de vida (`init`, `new-task`, `status`, `handoff`, `close`).
- [x] **Fase 3:** Validación inteligente de obsolescencia usando Git SHAs.
- [x] **Fase 4:** Escáner Automático (`angel scan`) de lenguajes y arquitecturas.
- [x] **Fase 5:** Adaptadores nativos para IDEs y Servidor MCP (Model Context Protocol).
