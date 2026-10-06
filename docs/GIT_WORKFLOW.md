# Git Workflow

Normas de ramas, commits, versiones y colaboración para este repositorio. Todo cambio, sea de una persona o de un asistente de IA, debe seguirlas.

---

## 1. Modelo de ramas

Se usa **Git Flow simplificado**.

| Rama | Propósito | Nace de | Se integra en |
|---|---|---|---|
| `main` | Código en producción. Cada commit es una versión publicada. | — | — |
| `develop` | Integración de trabajo terminado para la próxima versión. | `main` | `release/*` |
| `feature/*` | Nueva funcionalidad. | `develop` | `develop` |
| `fix/*` | Corrección de un bug no urgente. | `develop` | `develop` |
| `refactor/*` | Mejora interna sin cambiar comportamiento. | `develop` | `develop` |
| `docs/*` | Solo documentación. | `develop` | `develop` |
| `chore/*` | Configuración, dependencias, tooling, CI. | `develop` | `develop` |
| `release/x.y.z` | Preparar una versión (ajustes finales, changelog). | `develop` | `main` y `develop` |
| `hotfix/x.y.z` | Corrección urgente en producción. | `main` | `main` y `develop` |

```
main      ●───────────────●────────────●
           \             / \          /
release     \       ●───●   \        /
             \     /         \      /
develop       ●───●───●───●───●────●───●
                   \     / \     /
feature             ●───●   ●───●
```

### Nombres de ramas

- Formato: `tipo/descripcion-corta` en minúsculas, kebab-case, en inglés.
- Máximo ~4 palabras. Sin fechas ni nombres de personas.
- Si hay issue asociado, se puede prefijar su número.

```
feature/user-authentication
feature/42-shift-calendar
fix/expired-token-handling
refactor/api-client
chore/eslint-config
release/1.2.0
hotfix/1.2.1
```

### Reglas

- **Nunca** se hace commit directo a `main` ni a `develop`.
- Una rama = un objetivo. Si aparece trabajo no relacionado, se abre otra rama.
- Las ramas se eliminan después de integrarse.
- Mantener la rama actualizada con `develop` mediante `git rebase develop` (solo si la rama no está compartida) o `git merge develop`.

---

## 2. Commits — Conventional Commits

### Formato

```
<tipo>(<scope opcional>): <descripción>

<cuerpo opcional>

<footer opcional>
```

### Tipos permitidos

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad para el usuario |
| `fix` | Corrección de un bug |
| `refactor` | Cambio de código que no altera comportamiento |
| `perf` | Mejora de rendimiento |
| `test` | Añadir o corregir tests |
| `docs` | Solo documentación |
| `style` | Formato, espacios, punto y coma (sin cambio lógico) |
| `build` | Sistema de build o dependencias |
| `ci` | Pipelines y configuración de CI/CD |
| `chore` | Mantenimiento que no encaja en lo anterior |
| `revert` | Revertir un commit previo |

### Scope

Opcional. Indica el módulo afectado, en minúsculas y en una palabra: `auth`, `api`, `db`, `ui`, `deps`.

### Descripción (primera línea)

- En **inglés**, modo imperativo: `add`, `fix`, `remove` (no `added`, `fixes`).
- Empieza en minúscula y **sin punto final**.
- Máximo **72 caracteres** en total.
- Describe *qué* cambia, no *cómo*.

### Cuerpo

- Separado por una línea en blanco.
- Explica el *porqué* y el contexto cuando no es obvio.
- Líneas de máximo 72 caracteres.

### Footer

- Referencias: `Closes #42`, `Refs #17`.
- Cambios incompatibles: `BREAKING CHANGE: <descripción>` o `!` tras el tipo.

### Ejemplos válidos

```
feat(auth): add JWT login endpoint
fix(api): return 404 when report does not exist
refactor(db): extract repository layer from services
test(auth): cover expired token scenario
docs: document local development setup
ci: add lint and test workflow
feat(api)!: change pagination to cursor-based

BREAKING CHANGE: `page` query param replaced by `cursor`.
```

### Mensajes prohibidos

`fix`, `changes`, `update`, `stuff`, `wip`, `final`, `final final`, `test`, `asdf`, `cosas`, `.`, o cualquier mensaje que no diga qué cambió.

### Tamaño del commit

- Un commit = una unidad lógica de trabajo que compila y pasa los tests.
- No mezclar refactor con features o fixes en el mismo commit.
- No sobre-dividir: varios cambios pequeños relacionados van juntos.

---

## 3. Pull Requests e integración

- Todo cambio entra a `develop` o `main` mediante Pull Request.
- Título del PR con formato Conventional Commits.
- Descripción mínima: qué cambia, por qué, cómo probarlo.
- Requisitos antes de integrar: CI en verde, sin conflictos, revisión propia del diff.

| Integración | Estrategia |
|---|---|
| `feature/*`, `fix/*`, etc. → `develop` | **Squash merge** (un commit limpio por PR) |
| `release/*` → `main` | **Merge commit** (`--no-ff`) |
| `hotfix/*` → `main` | **Merge commit** (`--no-ff`) |
| `release/*` / `hotfix/*` → `develop` | **Merge commit** (`--no-ff`) |

---

## 4. Versionado y releases

Se usa **Semantic Versioning**: `MAJOR.MINOR.PATCH`.

- `MAJOR`: cambios incompatibles (`BREAKING CHANGE`).
- `MINOR`: nuevas funcionalidades compatibles (`feat`).
- `PATCH`: correcciones compatibles (`fix`).
- Antes de `1.0.0` el proyecto se considera en desarrollo inicial.

### Proceso de release

```bash
git switch develop && git pull
git switch -c release/1.2.0
# ajustes finales, actualizar CHANGELOG.md y versión
git switch main && git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "release: v1.2.0"
git switch develop && git merge --no-ff release/1.2.0
git branch -d release/1.2.0
git push origin main develop --follow-tags
```

### Proceso de hotfix

```bash
git switch main && git pull
git switch -c hotfix/1.2.1
# corrección + commit fix(...)
git switch main && git merge --no-ff hotfix/1.2.1
git tag -a v1.2.1 -m "release: v1.2.1"
git switch develop && git merge --no-ff hotfix/1.2.1
git branch -d hotfix/1.2.1
git push origin main develop --follow-tags
```

- Tags siempre anotados (`-a`), con prefijo `v`, solo sobre `main`.

---

## 5. Operaciones peligrosas

- Prohibido `git push --force` sobre `main` y `develop`.
- En ramas propias, si hay que reescribir historial, usar `git push --force-with-lease`.
- Antes de cualquier reescritura (`rebase`, `reset --hard`, `filter-repo`) crear un respaldo:

```bash
git branch backup/<descripcion>-<yyyymmdd>
```

- No hacer commit de secretos, `.env`, credenciales ni archivos generados. Mantener `.gitignore` actualizado.

---

## 6. Uso de asistentes de IA (Claude y otros)

Estas reglas son obligatorias para cualquier asistente de IA que genere commits, ramas o Pull Requests en este repositorio.

- **No añadir coautorías.** Prohibido incluir `Co-Authored-By: Claude <...>` o cualquier otro trailer de coautoría en los commits.
- **No añadir firmas ni menciones de generación automática** en commits, PRs, tags o releases (por ejemplo `🤖 Generated with Claude Code` o similares).
- El autor y committer es siempre el desarrollador del repositorio, con la configuración de `user.name` y `user.email` existente. No modificarla.
- Seguir exactamente las normas de ramas y commits de este documento.
- No hacer `push`, `force-push`, reescritura de historial, merges a `main`/`develop` ni crear tags sin aprobación explícita del desarrollador.
- Proponer el mensaje del commit y el diff antes de ejecutar cuando el cambio no sea trivial.

> Copiar esta sección en el `CLAUDE.md` del proyecto para que Claude Code la aplique automáticamente.

---

## 7. Checklist antes de cada commit

- [ ] Estoy en la rama correcta (no `main` ni `develop`).
- [ ] El cambio es una sola unidad lógica.
- [ ] El código compila y los tests pasan.
- [ ] El mensaje sigue Conventional Commits y tiene ≤ 72 caracteres.
- [ ] No hay secretos, archivos temporales ni código de depuración.
- [ ] No hay trailers de coautoría ni firmas de IA.

---

## 8. Estado de la adopción (2026-10-06)

Este documento es la norma, pero no todo está **forzado** por GitHub todavía. Lo que la norma
pide y nadie puede saltarse, frente a lo que por ahora depende de que cada quien lo cumpla:

| Regla | ¿Forzada? | Por qué |
|---|---|---|
| `main` solo cambia por pull request | **Sí** | Ruleset «Proteger main» |
| Los 4 trabajos de «Pruebas» en verde antes de integrar a `main` | **Sí** | Ruleset, *required status checks* |
| Sin force push ni borrado de `main` | **Sí** | Ruleset |
| `main` se integra con merge commit | **Sí** | Ruleset: `allowed_merge_methods: [merge]` |
| Todos los pull request corren pruebas | **Sí** | `pruebas.yml`, sin filtro de ramas |
| `develop` solo cambia por pull request | **No** | El ruleset cubre solo `refs/heads/main` |
| Los pull request apuntan a `develop` por defecto | **No** | La rama por defecto del repositorio sigue siendo `main` |

Las dos últimas necesitan permiso de **administrador** sobre el repositorio, que es de
`F5Alejo`. Para cerrarlas hay que pedirle que:

1. Extienda el ruleset (o cree uno igual) sobre `refs/heads/develop`.
2. Cambie la rama por defecto a `develop`, para que los pull request no apunten a `main` por error.

Mientras tanto, **nadie hace commit directo a `develop`**: es una regla de equipo, no una
barrera técnica.
