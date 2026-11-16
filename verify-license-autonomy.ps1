# verify-license-autonomy.ps1
# Druga roka (§0.47) + sebe-preglej-vedno (§0.49) v obliki kode.
# Preverja vse 17 repov pod C:\Users\Luka\Documents\Arhiv\Git\
# da vsaka licenca (ali semeno) ujema hash kanonske LICENSE.md v Atmavictu (0.1560 × 10⁴).
# Deluje brez mreže, brez GitHuba, brez vmesnika.

$ErrorActionPreference = "Stop"
$root = 'C:\Users\Luka\Documents\Arhiv\Git'
$canonicalHash = 'A2C34E8C10CFD8232A929BC0F0E895DAAA6CDDE8F301B5995026543630B782DA'
$canonicalVersion = '0.1560 × 10⁴'
$report = @()

function Test-LicenseFile {
    param([string]$repo, [string]$filePath, [string]$expectedHash, [string]$label)
    $full = Join-Path $repo $filePath
    if (-not (Test-Path $full)) {
        $report += [PSCustomObject]@{
            Repo = (Split-Path $repo -Leaf)
            File = $filePath
            Label = $label
            Status = 'MISSING'
            Detail = "Datoteka $filePath ne obstaja v repolu"
        }
        return
    }
    $hash = (Get-FileHash -Path $full -Algorithm SHA256).Hash
    $match = ($hash -eq $expectedHash)
    $report += [PSCustomObject]@{
        Repo = (Split-Path $repo -Leaf)
        File = $filePath
        Label = $label
        Status = if ($match) { 'OK' } else { 'DRIFT' }
        Detail = if ($match) { "Hash ujema kanonsko verzijo $canonicalVersion" } else { "Hash $hash NE ujema kanonskega $expectedHash" }
    }
}

$repos = Get-ChildItem -Directory -Path $root | Where-Object { Test-Path (Join-Path $_.FullName '.git') } | Sort-Object Name

foreach ($r in $repos) {
    $dir = $r.FullName
    $repoName = $r.Name

    # Atmavictu: kanonska LICENSE.md
    if ($repoName -eq 'Atmavictu') {
        Test-LicenseFile -repo $dir -filePath 'LICENSE.md' -expectedHash $canonicalHash -label 'Kanonska LICENSE.md'
        # Preveri še LINEAGE vnos 0.1560
        $lin = Join-Path $dir 'LICENSE-LINEAGE.md'
        if (Test-Path $lin) {
            $content = Get-Content -Path $lin -Raw
            if ($content -match '0\.1560 × 10⁴') {
                $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-LINEAGE.md'; Label = 'Lineage 0.1560'; Status = 'OK'; Detail = 'Lineage vnos 0.1560 obstaja' }
            } else {
                $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-LINEAGE.md'; Label = 'Lineage 0.1560'; Status = 'DRIFT'; Detail = 'Lineage vnos 0.1560 manjkajoč' }
            }
        }
    }
    # Sestre: preveri LICENSE-SEED.md + LICENSE-MANIFEST.json
    elseif (@('Aplikacija','DelozaZivot','EnglishVarient','Mucilnica-modrosti','ontolo-ko-jedro','OntoMatematika','SYMBOLON-KATHOLIKON','ZAKONODAJACLOVEKA') -contains $repoName) {
        $seedHash = (Get-ChildItem -Path $dir -Filter 'LICENSE-SEED.md' -File | ForEach-Object { (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash }) -join ','
        # Seed hash se ne ujema kanonskega (seme je drugačno besedilo), ampak mora obstajat
        if (Test-Path (Join-Path $dir 'LICENSE-SEED.md')) {
            $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-SEED.md'; Label = 'Seme obstaja'; Status = 'OK'; Detail = 'LICENSE-SEED.md je prisoten v repolu' }
        } else {
            $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-SEED.md'; Label = 'Seme manjkajoče'; Status = 'MISSING'; Detail = 'LICENSE-SEED.md ni v repolu' }
        }
        if (Test-Path (Join-Path $dir 'LICENSE-MANIFEST.json')) {
            $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-MANIFEST.json'; Label = 'Manifest obstaja'; Status = 'OK'; Detail = 'LICENSE-MANIFEST.json je prisoten v repolu' }
        } else {
            $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-MANIFEST.json'; Label = 'Manifest manjkajoč'; Status = 'MISSING'; Detail = 'LICENSE-MANIFEST.json ni v repolu' }
        }
        # Preveri da manifest sklicuje na kanonsko verzijo
        $man = Join-Path $dir 'LICENSE-MANIFEST.json'
        if (Test-Path $man) {
            $content = Get-Content -Path $man -Raw
            if ($content -match $canonicalHash) {
                $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-MANIFEST.json'; Label = 'Manifest sklicuje na kanonsko'; Status = 'OK'; Detail = "Manifest vsebuje kanonski hash $canonicalHash" }
            } else {
                $report += [PSCustomObject]@{ Repo = $repoName; File = 'LICENSE-MANIFEST.json'; Label = 'Manifest brez kanonskega sklica'; Status = 'DRIFT'; Detail = 'Manifest ne vsebuje kanonskega hash-a' }
            }
        }
    }
    # .github-workflows: ostaja kot most (kopija kanonskega LICENSE.md)
    elseif (($repoName -eq '.github-workflows')) {
        Test-LicenseFile -repo $dir -filePath 'LICENSE.md' -expectedHash $canonicalHash -label 'Mirror (most)'
    }
    # Ostali reposki (ni v semenu-distribuciji): opozorilo, ne napaka
    else {
        $hasLic = Get-ChildItem -Path $dir -Filter 'LICENSE*' -File | Where-Object { $_.FullName -notlike '*node_modules*' -and $_.Extension -ne '.bin' -and $_.Extension -ne '.exe' }
        if (-not $hasLic) {
            $report += [PSCustomObject]@{ Repo = $repoName; File = '(none)'; Label = 'Brez licence (ni v distribuciji)'; Status = 'INFO'; Detail = 'Rep brez LICENSE datoteke, ni del semena-distribucije' }
        } else {
            $report += [PSCustomObject]@{ Repo = $repoName; File = ($hasLic | Select-Object -First 1).Name; Label = 'Obstaja LICENSE* (ni v distribuciji)'; Status = 'INFO'; Detail = 'Rep ima LICENSE datoteko, ni v semenu-distribuciji' }
        }
    }
}

# Izpis poročila
$report | Format-Table -AutoSize -Wrap

$drifts = $report | Where-Object { $_.Status -eq 'DRIFT' -or $_.Status -eq 'MISSING' }
if ($drifts.Count -gt 0) {
    Write-Output ""
    Write-Output "⚠ NAJDENI DRIFT / MISSING ($($drifts.Count)) — preveri in popravi pred pushom:"
    $drifts | Format-Table -AutoSize -Wrap
    exit 1
} else {
    Write-Output ""
    Write-Output "✓ VSI REPOJI OK — licenca same sebe gradijo (avtonomija dosežena lokalno)"
    exit 0
}