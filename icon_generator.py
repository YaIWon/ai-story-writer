# icon_generator.py

import os
import json
import base64
from typing import Dict, List, Any
from datetime import datetime

class IconGenerator:
    def __init__(self, output_dir: str = "outputs/icons"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_browser_extension_icons(self) -> Dict[str, str]:
        """Generate all browser extension icons"""
        print("🎨 Generating browser extension icons...")
        
        icon_sizes = {
            '16': '16x16',
            '32': '32x32', 
            '48': '48x48',
            '128': '128x128'
        }
        
        generated_icons = {}
        
        for size, dimensions in icon_sizes.items():
            icon_path = self._generate_single_icon(size, dimensions)
            generated_icons[size] = icon_path
            print(f"✅ Generated {dimensions} icon: {os.path.basename(icon_path)}")
        
        return generated_icons
    
    def _generate_single_icon(self, size: str, dimensions: str) -> str:
        """Generate a single icon file"""
        # Create SVG icon content
        svg_content = self._create_svg_icon(dimensions)
        
        # Save as SVG
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"icon_{size}_{timestamp}.svg"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        # Also create PNG placeholder
        png_filename = f"icon_{size}_{timestamp}.png"
        png_filepath = os.path.join(self.output_dir, png_filename)
        self._create_png_placeholder(png_filepath, dimensions)
        
        return filepath
    
    def _create_svg_icon(self, dimensions: str) -> str:
        """Create SVG icon content"""
        width, height = map(int, dimensions.split('x'))
        
        svg_template = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7E22CE;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="15" fill="url(#gradient)"/>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="{width//4}" 
        fill="white" text-anchor="middle" dy=".3em" font-weight="bold">AI</text>
</svg>'''
        
        return svg_template
    
    def _create_png_placeholder(self, filepath: str, dimensions: str):
        """Create PNG placeholder file"""
        # In a real implementation, this would convert SVG to PNG
        # For now, create a metadata file
        metadata = {
            'dimensions': dimensions,
            'generated_at': datetime.now().isoformat(),
            'type': 'browser_extension_icon',
            'format': 'png',
            'note': 'Placeholder - convert SVG to PNG in production'
        }
        
        metadata_filepath = filepath.replace('.png', '.json')
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def get_icon_manifest(self) -> Dict[str, str]:
        """Get icon manifest for browser extension"""
        icons = self.generate_browser_extension_icons()
        
        manifest = {
            "icons": {},
            "generated_at": datetime.now().isoformat()
        }
        
        for size, path in icons.items():
            manifest["icons"][size] = os.path.basename(path)
        
        return manifest
