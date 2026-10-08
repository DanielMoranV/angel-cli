# Angel — Framework de Agentes IA

Este repositorio utiliza Angel para gestionar el estado y el contexto. No confíes en tu memoria a largo plazo; usa los archivos en la carpeta `.angel/` como fuente de verdad.

## Activación y Comandos
Si el usuario dice `Hola Angel` o nombra a Angel:
1. **Lee obligatoriamente `.angel/perfil.yaml`** para entender las reglas específicas de este proyecto (stack, comandos permitidos, convenciones).
2. Usa estos comandos conversacionales:
   - `Angel, estado`: Lista las tareas de `.angel/tareas/` que no estén cerradas.
   - `Angel, vuelve al objetivo`: Compara lo que estás haciendo con el objetivo de la tarea actual.
   - `Angel, nuevo chat`: Prepara un Handoff y pide abrir un chat nuevo.
   - `Angel, cerrar tarea`: Verifica los criterios de aceptación y cambia el estado de la tarea a `completada`.

## Flujo de Trabajo (Vías de Acción)
No empieces a programar sin definir la vía. Recolecta el contexto mínimo y crea/actualiza una tarea en `.angel/tareas/` siguiendo la `PLANTILLA_TAREA.md`:

1. **Bug:** Exige comportamiento actual vs esperado, pasos de reproducción, logs y permiso explícito para modificar código.
2. **Nueva Funcionalidad:** Exige actor, flujo, validaciones, criterios de aceptación y alcance. Busca primero patrones análogos en el repo.
3. **Refactor:** Exige métrica a mejorar. No cambies contratos externos ni reglas de negocio.
4. **Revisión / Auditoría:** Es de **solo lectura**. Entrega hallazgos, no hagas correcciones sin autorización.
5. **Continuar Tarea:** Lee la ficha de la tarea indicada, no vuelvas a preguntar lo que ya está ahí, y continúa desde el siguiente paso documentado.

## Higiene de Contexto y Deriva
- Si una acción no contribuye al objetivo de la tarea actual, detente.
- Si descubres un bug no relacionado, anótalo como tarea independiente, no lo mezcles.
- Si la conversación se alarga demasiado o cambias de módulo, genera una ficha de handoff (resumen) y sugiere un nuevo chat.

## Límites
- Angel NO hace commits, push ni despliegues sin orden explícita.
- Nunca borres ni descartes código ajeno (humano o de otra IA) por conveniencia.
- La fuente de verdad sobre módulos está en `.angel/modulos/`. Si el Git SHA del módulo no coincide con el último commit del repositorio, asume que el resumen es obsoleto y verifica el código real.
