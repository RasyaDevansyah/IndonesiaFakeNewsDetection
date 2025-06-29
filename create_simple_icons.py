#!/usr/bin/env python3
"""
Create simple PNG icons for the Chrome extension using Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, text="🔍", bg_color=(102, 126, 234), text_color=(255, 255, 255)):
    """Create a simple icon with text"""
    # Create image with gradient-like background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect (simple version)
    for i in range(size):
        # Interpolate between two colors
        r = int(bg_color[0] + (i / size) * (118 - bg_color[0]))
        g = int(bg_color[1] + (i / size) * (75 - bg_color[1]))
        b = int(bg_color[2] + (i / size) * (162 - bg_color[2]))
        draw.rectangle([0, i, size, i+1], fill=(r, g, b, 255))
    
    # Add white border
    draw.rectangle([0, 0, size-1, size-1], outline=(255, 255, 255, 255), width=2)
    
    # Try to add text (emoji or simple text)
    try:
        # For larger icons, try to use emoji
        if size >= 48:
            # Create a simple magnifying glass icon
            center = size // 2
            radius = size // 4
            
            # Draw magnifying glass circle
            draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                        outline=(255, 255, 255, 255), width=3)
            
            # Draw handle
            handle_start = center + radius - 5
            handle_end = handle_start + radius
            draw.line([handle_start, handle_start, handle_end, handle_end], 
                     fill=(255, 255, 255, 255), width=3)
            
            # Add "FN" text for Fake News
            font_size = max(8, size // 8)
            try:
                # Try to use a system font
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            text = "FN"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2 + size // 3
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        else:
            # For small icons, just use a simple circle with "F"
            center = size // 2
            radius = size // 3
            draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                        outline=(255, 255, 255, 255), width=2)
            
            font_size = max(6, size // 4)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            text = "F"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
            
    except Exception as e:
        print(f"Warning: Could not add text to {size}x{size} icon: {e}")
    
    return img

def main():
    """Create all required icon sizes"""
    print("🎨 Creating Chrome Extension Icons...")
    print("=" * 40)
    
    # Create chrome-extension directory if it doesn't exist
    os.makedirs('chrome-extension', exist_ok=True)
    
    # Icon sizes needed for Chrome extension
    sizes = [16, 48, 128]
    
    for size in sizes:
        try:
            icon = create_icon(size)
            filename = f"chrome-extension/icon{size}.png"
            icon.save(filename, 'PNG')
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Failed to create icon{size}.png: {e}")
    
    print("\n🎉 Icon creation completed!")
    print("You can now load the Chrome extension.")

if __name__ == "__main__":
    main() 