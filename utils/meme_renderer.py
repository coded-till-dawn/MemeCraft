import os
from PIL import Image, ImageDraw, ImageFont

def load_font(font_path, size):
    """
    Attempts to load the specified font. Falls back to default if not found.
    """
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        try:
            # Try a standard Windows font if specific one fails
            return ImageFont.truetype("arial.ttf", size)
        except OSError:
            # Fallback to default PIL font (very small, but works)
            return ImageFont.load_default()

def draw_text_with_outline(draw, position, text, font, text_color="white", outline_color="black", outline_width=2):
    """
    Draws text with a black outline (stroke) at the given position.
    """
    x, y = position
    
    # Draw outline
    # We draw the text multiple times with slight offsets to simulate a stroke
    # Newer PIL versions support stroke_width, but this is the classic compatible way
    # or we can use the stroke_width parameter if available (PIL > 4.2.0)
    
    draw.text((x, y), text, font=font, fill=text_color, stroke_width=outline_width, stroke_fill=outline_color)

def render_meme(img, top_text, bottom_text, font_size=None, text_color="white", outline_color="black", outline_width=2, padding=30):
    """
    Renders text onto an existing PIL Image object.
    """
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # Resolve font path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "static", "fonts", "impact.ttf")

    # Calculate Font Size if not provided
    if not font_size:
        font_size = int(height * 0.1)
        
    font = load_font(font_path, font_size)

    # Helper to wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    # Draw Top Text
    if top_text:
        lines = wrap_text(top_text.upper(), font, width - 20)
        y_text = padding
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x_text = (width - w) / 2
            draw_text_with_outline(draw, (x_text, y_text), line, font, text_color, outline_color, outline_width)
            y_text += h + 5

    # Draw Bottom Text
    if bottom_text:
        lines = wrap_text(bottom_text.upper(), font, width - 20)
        total_height = 0
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h)
            total_height += h + 5
        
        y_text = height - total_height - padding
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            x_text = (width - w) / 2
            draw_text_with_outline(draw, (x_text, y_text), line, font, text_color, outline_color, outline_width)
            y_text += line_heights[i] + 5

    return img
