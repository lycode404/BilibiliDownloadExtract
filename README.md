# BilibiliDownloadExtract
可批量从Bilibili(Android)缓存文件中提取MP4/MKV格式的视频以及弹幕  
首页只上传了python代码，用户请在Release界面下载完整程序。
### 使用方法
1.把安卓端Bilibili的视频缓存文件(/Android/data/tv.danmaku.bili/download/)拷贝到workpath文件夹内。  
2.运行run.bat。(直接运行main.py也行，但是不方便查看程序运行结果)。  
3.按照提示输入mp4或者mkv（小写）然后回车选择输出视频格式。(个人建议选择mkv格式)  
4.等待程序运行结束后即可在savepath文件夹中找到视频以及弹幕文件。
### 原理
参考了小丸工具箱的工作原理，通过调用ffmpeg等工具合并音视频，并通过读取json文件获取视频标题、BV号等信息（用于命名输出文件）。  
  
PS:这是作者在备考计算机二级的时候整出来的巅（癫）峰（疯）之作，代码确实写的很烂，但是作者实在是没时间优化这个代码了。如果使用中发现有什么问题，那就……自己动手修复一下吧🤣。
