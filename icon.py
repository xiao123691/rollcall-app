from PIL import Image, ImageDraw

img = Image.new('RGB', (512, 512), color=(30, 60, 120))
draw = ImageDraw.Draw(img)

draw.text((200, 200), '🎲', font_size=120)
draw.text((200, 350), '班级管理', fill='white', font_size=40)

img.save('icon.png')
print("图标已创建")
