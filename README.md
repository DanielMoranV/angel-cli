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
- 🎨 **Interfaz CLI Amigable:** Construido con Typer y Rich para dar feedback visual, tablas y alertas directamente en la terminal.

---

## 🚀 Instalación

Por el momento, puedes instalar el paquete de forma global usando `pip` o `pipx`:

```bash
git clone git@github.com:DanielMoranV/angel-cli.git
cd angel-cli
pip install -e .
```

*Nota: Requiere Python 3.9 o superior y Git instalado en tu sistema.*

---

## 🛠️ Uso y Comandos

### 1. Inicializar un Proyecto
Ve a cualquier repositorio donde quieras trabajar con IA y ejecuta:
```bash
angel init
```
Esto creará una carpeta oculta `.angel/` con las plantillas necesarias (`ANGEL.md`, `perfil.yaml`) y subcarpetas para `tareas/` y `modulos/`.

### 2. Crear una Tarea
En lugar de decirle a la IA "haz esto", formaliza la instrucción:
```bash
angel new-task --title "Arreglar bug de login en iOS" --task-type bug
```
*(Generará automáticamente el archivo `.angel/tareas/T-001-arreglar-bug-de-login-en-ios.md`)*

### 3. Revisar el Estado
Para que tú y la IA sepan en qué están trabajando y qué memorias están desactualizadas:
```bash
angel status
```

### 4. Actualizar Memoria de Módulo
Cuando le pides a la IA que documente cómo funciona un módulo (`auth`), Angel anota el hash del commit actual. Si más adelante quieres forzar la actualización:
```bash
angel update-module auth
```

### 5. Continuar en Otro Chat (Handoff)
Si la ventana de contexto de la IA está a punto de explotar o quieres cambiar de proveedor:
```bash
angel handoff T-001
```
*(Copia el texto gigante que te devuelve la terminal y pégalo en el nuevo chat).*

### 6. Cerrar Tarea
```bash
angel close T-001
```
*(Marca la tarea como completada para que desaparezca del radar principal).*

---

## 🤖 Integración con Clientes IA

Angel está diseñado para funcionar como **núcleo neutro**. Dependiendo de la herramienta que uses, la integración es sutilmente distinta:

- **Claude Code / CLI Agents:** Simplemente añade a tu prompt de sistema: *"Sigue las instrucciones en `.angel/ANGEL.md` y usa el comando `angel status` antes de proponer cambios"*.
- **IDE Agents (Antigravity / Cursor):** Crea un archivo `.cursorrules` o equivalente que apunte a `.angel/ANGEL.md` como la fuente central de verdad.
- **ChatGPT Web:** Usa la terminal para correr `angel handoff <id>` y pega el resultado para empezar a hablar con el contexto perfecto.

---

## 🛣️ Roadmap

- [x] **Fase 1:** Plantillas base y diseño agnóstico.
- [x] **Fase 2:** Comandos de ciclo de vida (`init`, `new-task`, `status`, `handoff`, `close`).
- [x] **Fase 3:** Validación inteligente de obsolescencia usando Git SHAs.
- [ ] **Fase 4:** Escáner Automático (`angel scan`) para inferir lenguajes y arquitecturas al inicializar.
- [ ] **Fase 5:** Adaptadores nativos para IDEs y Servidor MCP (Model Context Protocol).
