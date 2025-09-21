Param(
    [string]$ProjectPath = '01-foundations/projects/lexer-playground'
)

if (-not (Test-Path $ProjectPath)) {
    Write-Error "[build] Project directory not found: $ProjectPath"
    exit 1
}

Push-Location $ProjectPath
try {
    if (Test-Path 'Makefile') {
        make all
    } elseif (Test-Path 'Cargo.toml') {
        cargo build
    } elseif (Test-Path 'package.json') {
        npm run build
    } else {
        Write-Warning '[build] No recognised build configuration; extend build.ps1 as needed.'
    }
} finally {
    Pop-Location
}
