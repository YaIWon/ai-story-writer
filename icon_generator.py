import os
import json
from datetime import datetime

class IconGenerator:
    """Real icon generator that creates actual SVG files"""
    
    def __init__(self, output_dir: str = "outputs/icons"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_all_icons(self):
        """Generate all browser extension icons"""
        print("🎨 Generating real browser extension icons...")
        
        icons = {}
        sizes = [16, 32, 48, 128]
        
        for size in sizes:
            icon_path = self._create_svg_icon(size)
            icons[str(size)] = icon_path
            print(f"✅ Generated {size}x{size} icon")
        
        self._create_icon_manifest(icons)
        return icons
    
    def _create_svg_icon(self, size):
        """Create actual SVG icon file"""
        filename = f"icon{size}.svg"
        filepath = os.path.join(self.output_dir, filename)
        
        svg_content = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg{size}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4F46E5"/>
      <stop offset="50%" stop-color="#7E22CE"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>
  </defs>
  <rect width="{size}" height="{size}" rx="{size//5}" fill="url(#bg{size})"/>
  <text x="50%" y="55%" font-family="Arial, sans-serif" font-size="{size//3}" 
        fill="white" text-anchor="middle" font-weight="bold">AI</text>
</svg>'''
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return filepath
    
    def _create_icon_manifest(self, icons):
        """Create icon manifest file"""
        manifest = {
            "name": "RawAI Creator Pro Icons",
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "icons": icons
        }
        
        manifest_path = os.path.join(self.output_dir, "icon_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)