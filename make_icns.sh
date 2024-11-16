#!/bin/bash

# Create temporary iconset directory
mkdir YouTube_Downloader.iconset

# Convert SVG to PNG files of different sizes
for size in 16 32 64 128 256 512; do
    sips -Z $size app_icon.svg --out YouTube_Downloader.iconset/icon_${size}x${size}.png
    if [ $size -le 256 ]; then
        sips -Z $((size*2)) app_icon.svg --out YouTube_Downloader.iconset/icon_${size}x${size}@2x.png
    fi
done

# Create ICNS file
iconutil -c icns YouTube_Downloader.iconset

# Clean up
rm -rf YouTube_Downloader.iconset
