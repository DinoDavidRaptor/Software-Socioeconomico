; =====================================================
; INNO SETUP SCRIPT - SoftSE
; DINOS Tech - Copyright (c) 2026
; =====================================================
; Requisitos: Inno Setup 6.x (https://jrsoftware.org/isinfo.php)
;
; Instrucciones:
; 1. Compila la app con Nuitka (scripts/build_nuitka.py)
; 2. Coloca los archivos de dist/ en la carpeta "dist/"
; 3. Agrega los graficos en assets/installer/
; 4. Abre este archivo con Inno Setup Compiler
; 5. Compila (Ctrl+F9) o Build > Compile
; =====================================================

#define MyAppName "DINOS SoftSE"
#define MyAppVersion "0.3.7"
#define MyAppPublisher "DINOS Tech"
#define MyAppURL "https://dinoraptor.tech/dinostech/SoftSE"
#define MyAppExeName "DINOS SoftSE.exe"
#define MyAppCopyright "Copyright (c) 2026 DINOS Tech"

[Setup]
; Identificador unico de la aplicacion (genera uno nuevo para tu app)
AppId={{8A2B3C4D-5E6F-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/soporte
AppUpdatesURL={#MyAppURL}/actualizaciones
AppCopyright={#MyAppCopyright}

; Directorios
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=.\installer_output
OutputBaseFilename=SoftSE_Setup_v{#MyAppVersion}

; Compresion
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; Permisos
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=commandline

; Apariencia
WizardStyle=modern
WizardSizePercent=100
DisableWelcomePage=no
ShowLanguageDialog=auto

; EULA y licencia
LicenseFile=assets\installer\EULA.txt

; Graficos del instalador (descomenta cuando tengas los archivos)
; WizardImageFile=assets\installer\banner.bmp
; WizardSmallImageFile=assets\installer\header.bmp
; SetupIconFile=assets\installer\icon.ico

; Desinstalador
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Otros
DisableProgramGroupPage=yes
AllowNoIcons=yes
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
spanish.LaunchAfterInstall=Ejecutar {#MyAppName} al finalizar
english.LaunchAfterInstall=Launch {#MyAppName} after installation

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Ejecutable principal
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Archivo de configuracion
Source: "dist\config.json"; DestDir: "{app}"; Flags: ignoreversion

; Crear estructura de carpetas (con archivos vacios para mantener estructura)
Source: "dist\data\estudios\*"; DestDir: "{app}\data\estudios"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist
Source: "dist\data\fotos\*"; DestDir: "{app}\data\fotos"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist
Source: "dist\export\*"; DestDir: "{app}\export"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

; README y documentacion
Source: "README.md"; DestDir: "{app}"; DestName: "LEAME.txt"; Flags: ignoreversion isreadme

[Dirs]
; Asegurar que los directorios existan con permisos correctos
Name: "{app}\data"; Permissions: users-full
Name: "{app}\data\estudios"; Permissions: users-full
Name: "{app}\data\fotos"; Permissions: users-full
Name: "{app}\export"; Permissions: users-full

[Icons]
; Menu Inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"

; Escritorio (opcional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Ejecutar despues de instalar (opcional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchAfterInstall}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Eliminar archivos creados durante el uso
Type: filesandordirs; Name: "{app}\data"
Type: filesandordirs; Name: "{app}\export"
Type: files; Name: "{app}\license.dat"
Type: files; Name: "{app}\empresas.json"
Type: files; Name: "{app}\*.log"

[Code]
// Codigo Pascal para validaciones adicionales

function InitializeSetup(): Boolean;
begin
  Result := True;
  // Aqui puedes agregar validaciones previas a la instalacion
  // Por ejemplo, verificar version de Windows, etc.
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Acciones post-instalacion
    // Por ejemplo, crear archivos de configuracion iniciales
  end;
end;

// Mostrar mensaje al terminar
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    // Mensaje personalizado al finalizar
  end;
end;
