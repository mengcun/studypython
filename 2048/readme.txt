1.curses库引用报错解决办法：
curses库( ncurses )提供了控制字符屏幕的独立于终端的方法。
curses是大多数类似于UNIX的系统（包括Linux）的标准部分，而且它已经移植到 Windows 和其它系统。
首先这个问题产生的根本原因是curses库不支持windows。
所以我们在下载完成python后（python 是自带 curses 库的），
虽然在python目录\Lib中可以看到curses库，但其实我们是不能使用的。
在提示的文件 __init__ 文件中也确实可以找到 from _curses import *  这句话。
要解决这个问题，我们就需要使用一个unofficial curses（非官方curses库）来代替 python 自带的curses库。也就是 whl 包。

1.到这里下载与自己python版本对应的 whl 包（win64位对应curses-2.2+utf8-cp27-cp27m-win_amd64.whl）
https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses

2.打开cmd窗口然后cd到下载的whl目录，直接输入命令pip install curses-2.2+utf8-cp27-cp27m-win_amd64.

3.打开conda，cd到2048.py脚本文件的位置，输入python 2048.py 运行查看。

4.本实验的详细解释：
https://www.shiyanlou.com/courses/368/labs/1172/document