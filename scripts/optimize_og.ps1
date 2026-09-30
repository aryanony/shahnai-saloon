Add-Type -AssemblyName System.Drawing
$srcPath = Join-Path $PSScriptRoot "..\public\shahnaz-og.png"
$src = [System.Drawing.Image]::FromFile($srcPath)

$destW = 1200
$destH = [int]($src.Height * ($destW / $src.Width))
$bmp = New-Object System.Drawing.Bitmap $destW, $destH
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$g.DrawImage($src, 0, 0, $destW, $destH)
$g.Dispose()
$src.Dispose()

# Save optimized PNG
$outPng = Join-Path $PSScriptRoot "..\public\shahnaz-og.png"
$backupPng = Join-Path $PSScriptRoot "..\public\shahnaz-og-original.png"
Copy-Item $outPng $backupPng -Force

# Save high-quality JPG (quality 85 - optimal for WhatsApp & social platforms)
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
$encoderParams = New-Object System.Drawing.Imaging.EncoderParameters 1
$encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, [long]85)
$outJpg = Join-Path $PSScriptRoot "..\public\shahnaz-og.jpg"
$bmp.Save($outJpg, $codec, $encoderParams)

# Save as optimized PNG
$bmp.Save($outPng, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()

$pngSize = (Get-Item $outPng).Length
$jpgSize = (Get-Item $outJpg).Length
Write-Output "Optimized PNG: $pngSize bytes ($([math]::Round($pngSize / 1KB, 1)) KB)"
Write-Output "Optimized JPG: $jpgSize bytes ($([math]::Round($jpgSize / 1KB, 1)) KB)"
