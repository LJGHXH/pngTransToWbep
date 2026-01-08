import sys
import os
from PIL import Image


# ================= 路径兼容性修复 =================
def get_resource_path():
    if getattr(sys, 'frozen', False):
        # 打包后的路径 (dist/main.app/Contents/MacOS/main)
        exec_path = os.path.dirname(sys.executable)
        if 'Contents/MacOS' in exec_path:
            # 返回 .app 所在的那个文件夹路径
            return os.path.dirname(os.path.dirname(os.path.dirname(exec_path)))
        return exec_path
    else:
        # 源代码运行路径
        return os.path.dirname(os.path.abspath(__file__))


# 锁定当前工作目录，防止 macOS 默认指向根目录
BASE_DIR = get_resource_path()
os.chdir(BASE_DIR)

# 输出目录设为绝对路径
output_base_folder = os.path.join(BASE_DIR, 'webp_output')

if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)
# =================================================

print("import LAN\n")

print("""
使用方法：
请将该程序放在已经按照数字顺序命名好的文件夹之外
    例：目录 “imgs转webp/萝卜笔/”中存储着“1.png, 2.png, 3.png, ...”等图片，
    那么将该程序放在“imgs转webp/”下即可

可按顺序输入转换参数：压缩后的高度值,帧数,画质 （默认值: 756,1,75）
    例：输入 “666,24,90”（注意，画质建议在70~95之间）
    即可得到高度666（宽度会等比缩放）、帧率24、画质为原图的90%的webp动态图
不输入参数直接按下Enter运行将按默认值运行
""")

while True:
    new_height, fps, quality = 756, 1, 75
    args = input("参数：").strip()

    if args:
        try:
            parts = args.replace('，', ',').split(',')
            if len(parts) == 3:
                new_height, fps, quality = map(int, parts)
        except ValueError:
            print("参数格式错误，将使用默认值。")

    print(f"将输出到: {output_base_folder}")

    # 遍历当前目录，只看一级子文件夹，避免深入系统敏感目录
    for dir_name in os.listdir(BASE_DIR):
        image_folder = os.path.join(BASE_DIR, dir_name)

        # 排除隐藏文件夹、输出文件夹和非文件夹对象
        if not os.path.isdir(image_folder) or dir_name.startswith('.') or dir_name == 'webp_output':
            continue

        try:
            # 过滤隐藏文件并排序
            image_files = sorted(
                [f for f in os.listdir(image_folder) if f.lower().endswith('.png') and not f.startswith('.')],
                key=lambda x: int(os.path.splitext(x)[0])
            )
        except Exception as e:
            print(f"跳过文件夹 {dir_name}: 文件名非数字或无权限 ({e})")
            continue

        if not image_files:
            continue

        images = []
        try:
            for file in image_files:
                img_path = os.path.join(image_folder, file)
                with Image.open(img_path).convert('RGBA') as img:
                    original_width, original_height = img.size
                    new_width = int(original_width * (new_height / original_height))
                    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                    images.append(resized_img)

            if images:
                output_path = os.path.join(output_base_folder, f'{dir_name}.webp')
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:],
                    duration=1000 // fps,
                    loop=0,
                    format='WEBP',
                    quality=quality
                )
                print(f"✅ 成功生成: {output_path}")
        except Exception as e:
            print(f"❌ 处理 {dir_name} 时出错: {e}")
