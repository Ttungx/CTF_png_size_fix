# CTF_png_size_fix
一个用于CTF比赛中恢复png图片宽高的脚本

恢复原理：
</br>
1.通过读取文件中的字节，提取 CRC 值。
2.生成不同宽度和高度组合的 PNG 数据块，并计算它们的 CRC32 校验和。
3.如果某个宽高组合的 CRC 值与目标 CRC 值匹配，就确认这个宽高组合是正确的。
4.最后，修改 PNG 文件中的宽高信息并保存为新的 PNG 文件。

使用方法：</br>
cmd/终端中输入"python pngsizefix.py [filename]"

示例：<br>
题目图片：<br> 来自BaseCTF2024 week2 《前辈什么的最喜欢了》
<br>
![image](https://github.com/user-attachments/assets/411338d4-392c-4d02-a760-1a90ee013b9f)
<br>
输入命令后回车<br>
![image](https://github.com/user-attachments/assets/615e03a8-28e3-4855-8fdf-0182c9ff7a27)
<br>
即可得到flag<br>
![test_v2](https://github.com/user-attachments/assets/b4f3bd47-166b-4c53-9438-bbac7009a18b)
