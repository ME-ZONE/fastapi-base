Write-Host "Checking Alembic heads on Windows..." -ForegroundColor Blue
$headsCount = (poetry run alembic history | Select-String -Pattern "\(head\)").Count
if ($headsCount -gt 1) {
    Write-Host "Multiple migration heads detected!" -ForegroundColor Red
    Write-Host "Fix using: alembic merge heads" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "Alembic migrations passed." -ForegroundColor Green
}