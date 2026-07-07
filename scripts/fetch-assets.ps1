$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$imgDir = Join-Path $root "images"
$fontDir = Join-Path $root "fonts"
New-Item -ItemType Directory -Force -Path $imgDir | Out-Null
New-Item -ItemType Directory -Force -Path $fontDir | Out-Null

$images = @{
  "logo.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/LOGO-798x800.png"
  "hero-1.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/hero-1.jpg"
  "hero-2.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/hero-2.jpg"
  "product.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/product.jpg"
  "recipe-grill.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/grill.jpg"
  "recipe-roast.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/roast.jpg"
  "recipe-stir-fry.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/stir-fry.jpg"
  "gallery-1.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/gallery-1.jpg"
  "gallery-2.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/gallery-2.jpg"
  "gallery-3.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/gallery-3.jpg"
  "gallery-4.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/gallery-4.jpg"
  "article-1.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/article-1.jpg"
  "article-2.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/article-2.jpg"
  "article-3.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/article-3.jpg"
  "contact-values-card.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/Back_Business-card_3.5X2_Vistaprint-01.jpg"
  "contact-business-card.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/Front_Business-card_3.5X2_Vistaprint-01.jpg"
  "product-main.webp" = "https://suwanneebellfarms.com/wp-content/uploads/2024/01/product.jpg"
}

foreach ($entry in $images.GetEnumerator()) {
  $dest = Join-Path $imgDir $entry.Key
  try {
    Invoke-WebRequest -Uri $entry.Value -OutFile $dest -UseBasicParsing -TimeoutSec 60
    Write-Host "Downloaded $($entry.Key)"
  } catch {
    Write-Warning "Failed $($entry.Key): $($_.Exception.Message)"
  }
}

$fontUrls = @{
  "playfair-display-v37-latin-regular.woff2" = "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2"
  "playfair-display-v37-latin-600.woff2" = "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFiD-vYSZviVYUb_rj3ij__anPXDTLYgFE_.woff2"
  "playfair-display-v37-latin-700.woff2" = "https://fonts.gstatic.com/s/playfairdisplay/v37/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM.woff2"
}

foreach ($entry in $fontUrls.GetEnumerator()) {
  $dest = Join-Path $fontDir $entry.Key
  try {
    Invoke-WebRequest -Uri $entry.Value -OutFile $dest -UseBasicParsing -TimeoutSec 60
    Write-Host "Downloaded font $($entry.Key)"
  } catch {
    Write-Warning "Failed font $($entry.Key): $($_.Exception.Message)"
  }
}

Write-Host "Done."
