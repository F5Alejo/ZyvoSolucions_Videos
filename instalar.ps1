# Instala el Estudio de video RiskMann en un equipo nuevo (Windows, PowerShell 5.1 o superior).
#
#   powershell -ExecutionPolicy Bypass -File instalar.ps1
#
# Opciones:
#   -SinModelos      no baja las voces Kokoro y Piper (~185 MB); se puede hacer luego.
#   -InstalarFfmpeg  instala ffmpeg con winget si no está.
#   -Probar          al final corre las pruebas (pytest y Vitest).
#   -ConAgentes      baja los modelos de Ollama para los agentes (qwen3:4b y qwen3.5:2b, ~5 GB).
#                    Hace falta Ollama instalado: https://ollama.com/download
#
# Se puede volver a correr: lo que ya está instalado se salta. Nunca sube ni borra nada.

param(
    [switch]$SinModelos,
    [switch]$InstalarFfmpeg,
    [switch]$Probar,
    [switch]$ConAgentes
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
$avisos = New-Object System.Collections.Generic.List[string]

function Paso($texto) { Write-Host ""; Write-Host "==> $texto" -ForegroundColor Cyan }
function Bien($texto) { Write-Host "    OK  $texto" -ForegroundColor Green }
function Aviso($texto) { Write-Host "    !   $texto" -ForegroundColor Yellow; $avisos.Add($texto) }
function Fallar($texto) { Write-Host ""; Write-Host "ERROR: $texto" -ForegroundColor Red; exit 1 }

# Corre un programa y se detiene si falla (en PowerShell 5.1 $ErrorActionPreference no cubre programas externos).
function Correr($programa, [string[]]$argumentos, $queHace) {
    & $programa @argumentos
    if ($LASTEXITCODE -ne 0) { Fallar "$queHace falló (código $LASTEXITCODE)." }
}

function Existe($comando) { return [bool](Get-Command $comando -ErrorAction SilentlyContinue) }

# ── 1. Programas del equipo ─────────────────────────────────────────────────
Paso "Revisando Python, Node y ffmpeg"

$python = $null
foreach ($candidato in @("python", "py")) {
    if (Existe $candidato) {
        try {
            $version = & $candidato -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
            if ($LASTEXITCODE -eq 0 -and $version -and [version]$version -ge [version]"3.12") { $python = $candidato; break }
        } catch {
            # El «python» de la Tienda de Windows que no está instalado: se prueba el siguiente.
        }
    }
}
if (-not $python) { Fallar "Hace falta Python 3.12 o superior: https://www.python.org/downloads/ (marca «Add python.exe to PATH»)." }
Bien "Python $version"

if (-not (Existe "node")) { Fallar "Hace falta Node 22 o superior: https://nodejs.org/" }
$node = (& node --version).TrimStart("v")
if ([version]$node -lt [version]"22.0") { Fallar "Node $node es muy viejo: hace falta 22 o superior (lo pide HyperFrames)." }
Bien "Node $node"

if (Existe "ffmpeg") {
    Bien "ffmpeg"
} elseif ($InstalarFfmpeg -and (Existe "winget")) {
    Correr "winget" @("install", "--id", "Gyan.FFmpeg", "-e", "--accept-source-agreements", "--accept-package-agreements") "Instalar ffmpeg"
    Aviso "ffmpeg quedó instalado: cierra y abre la terminal para que Windows lo encuentre."
} else {
    Aviso "Falta ffmpeg: sin él no se producen videos. Instálalo con «winget install Gyan.FFmpeg» o vuelve a correr con -InstalarFfmpeg."
}

# ── 2. Python: entorno y librerías ──────────────────────────────────────────
Paso "Entorno de Python (.venv) y librerías"
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Correr $python @("-m", "venv", ".venv") "Crear .venv"
}
$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Correr $py @("-m", "pip", "install", "--quiet", "--disable-pip-version-check", "-r", "requirements.txt") "Instalar requirements.txt"
Bien "Librerías instaladas"

Paso "Navegador que dibuja las escenas (Chromium de Playwright)"
Correr $py @("-m", "playwright", "install", "chromium") "Instalar Chromium"
Bien "Chromium listo"

Paso "HyperFrames, el motor de video (motor/hyperframes)"
Push-Location "motor\hyperframes"
try {
    Correr "npm.cmd" @("install", "--no-audit", "--no-fund") "Instalar HyperFrames"
    # Su navegador propio; la telemetría va apagada (el material del cliente no sale del equipo).
    $env:HYPERFRAMES_NO_TELEMETRY = "1"
    Correr "node" @("node_modules\hyperframes\bin\hyperframes.mjs", "browser", "ensure") "Instalar el navegador de HyperFrames"
} finally {
    Pop-Location
}
Bien "HyperFrames listo"

# ── 3. Modelos de voz ───────────────────────────────────────────────────────
if ($SinModelos) {
    Aviso "No se bajaron las voces. Cuando quieras: .venv\Scripts\python.exe scripts\descargar_modelos.py"
} else {
    Paso "Voces Kokoro y Piper (~185 MB la primera vez)"
    Correr $py @("scripts\descargar_modelos.py") "Bajar los modelos de voz"
}

# ── 3b. Modelos de los agentes (Ollama) ─────────────────────────────────────
if ($ConAgentes) {
    Paso "Modelos de Ollama para los agentes (~5 GB la primera vez)"
    if (Existe "ollama") {
        foreach ($m in @("qwen3:4b", "qwen3.5:2b")) { Correr "ollama" @("pull", $m) "Bajar $m" }
        Bien "Modelos de los agentes listos"
    } else {
        Aviso "Falta Ollama (https://ollama.com/download). Sin él los agentes usan reglas simples."
    }
} else {
    Aviso "Opcional: vuelve a correr con -ConAgentes para que los agentes usen IA local (Ollama)."
}

# ── 4. Claves (.env, no va a git) ───────────────────────────────────────────
Paso "Clave de ElevenLabs (.env)"
if (Test-Path ".env") {
    Bien ".env ya existe: no se toca"
} else {
    Copy-Item ".env.ejemplo" ".env"
    $clave = ""
    # Sin nadie frente a la ventana (Actions, -NonInteractive o entrada redirigida), Read-Host espera
    # para siempre: no se pregunta.
    $interactiva = [Environment]::UserInteractive -and -not [Console]::IsInputRedirected -and
        -not ([Environment]::GetCommandLineArgs() -match '^-NonI')
    if ($interactiva) { try {
        $segura = Read-Host "    Pega la clave de ElevenLabs (Enter para dejarla vacía)" -AsSecureString
        $clave = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($segura))
    } catch {
        # Sin terminal interactiva: se deja vacía.
    } }
    if ($clave) {
        (Get-Content ".env") -replace "^ELEVENLABS_API_KEY=.*$", "ELEVENLABS_API_KEY=$clave" | Set-Content ".env" -Encoding ASCII
        Bien "Clave guardada en .env"
    } else {
        Aviso "Sin clave de ElevenLabs: Carlos no se podrá usar. Ponla luego en .env (las voces Kokoro sí funcionan)."
    }
}

if (-not (Test-Path "config.local.json")) {
    Aviso "Opcional: copia config.ejemplo.json como config.local.json para ver logos de todas las marcas, videos entregados y el ejemplo csm."
}

# ── 5. Interfaz (Vue) ───────────────────────────────────────────────────────
Paso "Interfaz: librerías y compilación (frontend/)"
Push-Location "frontend"
try {
    Correr "npm.cmd" @("ci", "--no-audit", "--no-fund") "npm ci"
    Correr "npm.cmd" @("run", "build") "Compilar la interfaz"
} finally {
    Pop-Location
}
Bien "Interfaz compilada en frontend\dist"

# ── 6. Pruebas (opcional) ───────────────────────────────────────────────────
if ($Probar) {
    Paso "Pruebas"
    Correr $py @("-m", "pytest", "-q") "pytest"
    Push-Location "frontend"
    try { Correr "npm.cmd" @("test") "Vitest" } finally { Pop-Location }
}

# ── Listo ───────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "Listo. Para abrir el estudio:" -ForegroundColor Green
Write-Host "    .venv\Scripts\activate"
Write-Host "    uvicorn app.main:app --port 8765"
Write-Host "    y abre http://localhost:8765"
if ($avisos.Count) {
    Write-Host ""
    Write-Host "Pendiente:" -ForegroundColor Yellow
    foreach ($a in $avisos) { Write-Host "  - $a" }
}
