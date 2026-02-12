# ========================================
# WORKSPACE: Software-Socioeconomico
# Email: dinodavidmicroraptor@gmail.com
# SSH Key: id_ed25519_personal
# Color: Rosa
# ========================================

# Cambiar a la carpeta del repo
Set-Location "C:\Users\dinoe\OneDrive\Documentos\Software-Socioeconomico"

# Forzar que esta sesion use la llave SSH correcta
$env:GIT_SSH_COMMAND = "ssh -i $env:USERPROFILE\.ssh\id_ed25519_personal -o IdentitiesOnly=yes"

# Configurar Git para este workspace
git config user.name "DinoDavid Raptor"
git config user.email "dinodavidmicroraptor@gmail.com"

# Agregar clave SSH al agent (sin mensajes de error)
ssh-add "$env:USERPROFILE\.ssh\id_ed25519_personal" 2>$null

# Cambiar el titulo de la ventana de terminal
$host.UI.RawUI.WindowTitle = "Software-Socioeconomico - Workspace"

# Banner de bienvenida
Write-Host ""
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "                                                            " -ForegroundColor Magenta
Write-Host "          WORKSPACE SOFTWARE-SOCIOECONOMICO                 " -ForegroundColor Magenta
Write-Host "                                                            " -ForegroundColor Magenta
Write-Host "  User: DinoDavid Raptor                                   " -ForegroundColor Magenta
Write-Host "  Email: dinodavidmicroraptor@gmail.com                    " -ForegroundColor Magenta
Write-Host "  SSH Key: id_ed25519_personal                             " -ForegroundColor Magenta
Write-Host "  Status: Ready                                            " -ForegroundColor Magenta
Write-Host "                                                            " -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host ""

# Informacion de Git
Write-Host "Git Configuration:" -ForegroundColor Green
git config --local user.name
git config --local user.email
Write-Host ""

# Informacion del repositorio
Write-Host "Repository Status:" -ForegroundColor Cyan
Write-Host "Branch: $(git rev-parse --abbrev-ref HEAD)" -ForegroundColor Cyan
Write-Host "Remote: $(git remote get-url origin)" -ForegroundColor Cyan
Write-Host ""

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "                   Workspace Ready                          " -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host ""
