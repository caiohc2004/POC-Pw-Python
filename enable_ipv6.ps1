# Enable IPv6 on all network adapters
# Must be run as Administrator

#Requires -RunAsAdministrator

Write-Host "Enabling IPv6 on all network adapters..." -ForegroundColor Yellow

Get-NetAdapter | ForEach-Object {
    Enable-NetAdapterBinding -Name $_.Name -ComponentID ms_tcpip6 -ErrorAction SilentlyContinue
    Write-Host "  [$($_.Name)] IPv6 enabled." -ForegroundColor Green
}

# Also re-enable via registry (remove the DisabledComponents key or set to 0)
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters"
Set-ItemProperty -Path $regPath -Name "DisabledComponents" -Value 0x00 -Type DWord -Force

Write-Host ""
Write-Host "IPv6 has been enabled. A system restart is recommended." -ForegroundColor Cyan
