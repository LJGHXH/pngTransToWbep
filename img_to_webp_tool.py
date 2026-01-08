from PIL import Image
import os

# 输出目录
output_base_folder = './webp_output/'

# 如果输出目录不存在，则创建
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

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

    # 默认值
    new_height = 756
    fps = 1
    quality = 75
    # 获取参数
    args = input("参数：")
    args = args.split(',')
    if len(args) == 1:
        args = args[0].split('，')
    if len(args) == 3:
        new_height = int(args[0])
        fps = int(args[1])
        quality = int(args[2])

    print(f"将输出 高度{new_height}、帧数{fps}、画质{quality} 的webp到 ./webp_output/ 目录下")

    # 遍历当前目录下的所有文件夹
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            image_folder = os.path.join(root, dir_name)

            # 获取所有 PNG 图片文件名，并按数字顺序排序
            image_files = sorted(
                [f for f in os.listdir(image_folder) if f.endswith('.png')],
                key=lambda x: int(os.path.splitext(x)[0])
            )

            # 如果没有 PNG 文件，跳过该文件夹
            if not image_files:
                continue

            # 打开所有图片，调整大小，并存储在一个列表中
            images = []
            for file in image_files:
                img_path = os.path.join(image_folder, file)
                with Image.open(img_path).convert('RGBA') as img:
                    # 获取原始尺寸
                    original_width, original_height = img.size
                    # 计算新的宽度，保持宽高比
                    new_width = int(original_width * (new_height / original_height))
                    # 调整大小
                    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                    images.append(resized_img)

            # 输出文件路径，使用文件夹名称作为文件名
            output_path = os.path.join(output_base_folder, f'{dir_name}.webp')

            # 将图片保存为 WebP 动画
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=1000 // fps,  # 每帧的持续时间（毫秒），20帧每秒
                loop=0,  # 无限循环
                format='WEBP',
                quality=quality
            )

            print(f"WebP 动画已保存到 {output_path}")
