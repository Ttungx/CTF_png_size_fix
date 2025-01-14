import os
import sys
import struct
import binascii


# 获取PNG文件CRC值的函数
def calculate_png_crc(file_path):
    try:
        with open(file_path, 'rb') as file:
            # 读取 PNG 文件的内容
            png_data = file.read()
            # 读取从第 30 位到第 33 位的 CRC 值（注意这里的索引是从 0 开始）
            crc_data = png_data[29:33]
            # 将读取到的字节数据转换为整数
            crc = struct.unpack('>I', crc_data)[0]
            return crc
    except FileNotFoundError:
        print(f"Error: 文件 '{file_path}' 未找到，请检查文件路径是否正确。")
        return None
    except Exception as e:
        print(f"Error: 发生错误 {str(e)}，请检查文件是否为有效的 PNG 文件。")
        return None


# 通过指定CRC值来纠正图片的宽高
def correct_png_dimensions(target_file, target_crc):
    try:
        with open(target_file, "rb") as f:
            crcbp = bytearray(f.read())  # 读取文件内容并存储为可修改的字节数组

        found = False
        print("正在遍历宽高数据，寻找匹配的 CRC 值...")
        # 遍历可能的宽度和高度，这里假设范围在 0 到 4095 之间
        for i in range(4096):
            for j in range(4096):
                data = crcbp[12:16] + struct.pack('>i', i) + struct.pack('>i', j) + crcbp[24:29]
                crc32 = binascii.crc32(data) & 0xffffffff
                if crc32 == target_crc:
                    print(f"已找到匹配的宽高: 宽度={i}, 高度={j}")
                    print(f"十六进制: 宽度={hex(i)}, 高度={hex(j)}")
                    found = True
                    break
            if found:
                break

        if found:
            # 创建新文件的名称
            base_name = os.path.basename(target_file)
            dir_name = os.path.dirname(target_file)
            new_file_name = os.path.join(dir_name, os.path.splitext(base_name)[0] + "_v2.png")

            # 修改图片的宽度和高度
            modified_crcbp = crcbp[:16] + struct.pack('>i', i) + struct.pack('>i', j) + crcbp[24:]

            # 将修改后的内容保存到新文件
            with open(new_file_name, "wb") as f:
                f.write(modified_crcbp)
            print(f"新图片已保存为: \"{new_file_name}\"")
        else:
            print("未找到匹配的宽高。请检查输入的 PNG 文件是否有效。")
    except FileNotFoundError:
        print(f"Error: 文件 '{target_file}' 未找到，请检查文件路径是否正确。")
    except ValueError:
        print(f"Error: 得到的 CRC 值无效，请检查输入。")
    except Exception as e:
        print(f"Error: 发生错误 {str(e)}，请确保文件为有效的 PNG 文件。")


def main():
    if len(sys.argv) != 2:
        print("用法: python [脚本] [目标 PNG 文件路径]")
        print("示例: python png_crc_correct.py image.png")
        sys.exit(1)

    target_file = sys.argv[1]

    # 获取 CRC 值
    print(f"正在获取文件 '{target_file}' 的 CRC 值...")
    crc = calculate_png_crc(target_file)
    if crc is not None:
        print(f"获取到的 CRC : {hex(crc)}")
        # 使用获取到的 CRC 值纠正 PNG 宽高
        correct_png_dimensions(target_file, crc)
    else:
        print("获取 CRC 值失败，请检查文件是否为有效的 PNG 文件。")


if __name__ == "__main__":
    main()
