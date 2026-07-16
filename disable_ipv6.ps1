# Disable IPv6 on all network adapters
# Must be run as Administrator

#Requires -RunAsAdministrator

Write-Host "Disabling IPv6 on all network adapters..." -ForegroundColor Yellow

Get-NetAdapter | ForEach-Object {
    Disable-NetAdapterBinding -Name $_.Name -ComponentID ms_tcpip6 -ErrorAction SilentlyContinue
    Write-Host "  [$($_.Name)] IPv6 disabled." -ForegroundColor Green
}

# Also disable via registry for full system-wide effect
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters"
Set-ItemProperty -Path $regPath -Name "DisabledComponents" -Value 0xFF -Type DWord -Force

Write-Host ""
Write-Host "IPv6 has been disabled. A system restart is recommended." -ForegroundColor Cyan
