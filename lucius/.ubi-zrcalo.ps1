$zrc = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*zrcalo-server.py*' }
if ($zrc) {
  $zrc | ForEach-Object { Write-Output ("najden: PID " + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force }
} else { Write-Output 'ni najden' }
