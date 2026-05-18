param(
    [Parameter(Mandatory = $true)]
    [string]$WorkbookPath,
    [Parameter(Mandatory = $true)]
    [string]$RangeAddress,
    [Parameter(Mandatory = $true)]
    [string]$OutputPng
)

$ErrorActionPreference = "Stop"

$resolvedWorkbook = (Resolve-Path -LiteralPath $WorkbookPath).Path
$outputDir = Split-Path -Parent $OutputPng
if (-not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$excel = $null
$workbook = $null
$chartObject = $null

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    $workbook = $excel.Workbooks.Open($resolvedWorkbook, 0, $true)
    $worksheet = $workbook.Worksheets.Item(1)
    $window = $excel.ActiveWindow
    if ($window -ne $null) {
        try { $window.Zoom = 170 } catch {}
        try { $window.DisplayGridlines = $false } catch {}
        try { $window.DisplayHeadings = $false } catch {}
    }
    $range = $worksheet.Range($RangeAddress)

    $range.CopyPicture(1, -4147)
    $chartObject = $worksheet.ChartObjects().Add(
        0,
        0,
        [Math]::Max($range.Width * 2.2, 400),
        [Math]::Max($range.Height * 2.2, 240)
    )
    $chart = $chartObject.Chart
    $chart.ChartArea.Clear()
    try { $chart.PlotArea.Format.Line.Visible = $false } catch {}
    $chart.Paste() | Out-Null
    $chart.Export($OutputPng) | Out-Null
}
finally {
    if ($chartObject -ne $null) {
        try { $chartObject.Delete() | Out-Null } catch {}
    }
    if ($workbook -ne $null) {
        try { $workbook.Close($false) | Out-Null } catch {}
    }
    if ($excel -ne $null) {
        try { $excel.Quit() | Out-Null } catch {}
    }

    if ($chartObject -ne $null) {
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($chartObject) | Out-Null
    }
    if ($workbook -ne $null) {
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
    }
    if ($excel -ne $null) {
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }

    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
