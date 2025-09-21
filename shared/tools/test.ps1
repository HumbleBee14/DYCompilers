Param(
    [string]$ProjectPath = '01-foundations/projects/lexer-playground'
)

if (-not (Test-Path $ProjectPath)) {
    Write-Error "[test] Project directory not found: $ProjectPath"
    exit 1
}

Push-Location $ProjectPath
try {
    if (Test-Path 'pytest.ini' -or (Test-Path 'tests' -and Test-Path 'requirements.txt')) {
        python -m pytest
    } elseif (Test-Path 'Cargo.toml') {
        cargo test
    } elseif (Test-Path 'package.json') {
        npm test
    } else {
        Write-Warning '[test] No recognised test configuration; extend test.ps1 as needed.'
    }
} finally {
    Pop-Location
}
