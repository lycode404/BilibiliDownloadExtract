'''
Bilibili缓存文件提取器 V0.4
批量提取(Android端)缓存中的视频和弹幕
支持的功能：
弹幕提取、m4s合并成mp4、mkv、单个blv转mp4、mkv
存在的问题：
不支持多个blv
后续更新计划：
优化文件命名（命名视频时加上分p序号，统一视频与番剧命名方式）
视频转码进程结束后检查视频是否存在（是否导出成功）
'''
import os
import json
import shutil
import subprocess

videoformat = input('请选择输出视频格式(mp4/mkv):')
workpath = 'workpath'
outpath = 'savepath'

videolist=os.listdir(workpath)

for video in videolist:
    videopath = workpath + '\\' + video
    subvideolist=os.listdir(videopath)
    for subvideo in subvideolist:
        subvideopath = workpath + '\\' + video + '\\' + subvideo
        #读json文件获取视频信息
        jsonfile = open(subvideopath + '\\' + 'entry.json','r',encoding='utf-8')
        jsonobj = json.load(jsonfile)
        videoname = jsonobj['title']
        try:
            subname = jsonobj['page_data']['part']
        except:
            subname = ' '
        try:  
            bvid = jsonobj['bvid']
        except:#按照番剧读取每集标题
            bvid = ''
            subname = jsonobj['ep']['index']+'_'+jsonobj['ep']['index_title']
            

        for x in r'\/:*?"<>|':#去掉非法字符
            videoname = videoname.replace(x,'')
            subname = subname.replace(x,'')
        #拷贝弹幕文件
        if os.path.exists(os.getcwd()+'\\'+subvideopath + '\\' + 'danmaku.xml'):
            shutil.copyfile(os.getcwd()+'\\'+subvideopath + '\\' + 'danmaku.xml', os.getcwd()+'\\'+outpath + '\\' + videoname+'_'+subname+'_'+bvid+'.xml')

        for subvideodir in os.listdir(subvideopath):
            if os.path.isdir(subvideopath + '\\' + subvideodir):
                subvideorealpath = subvideopath + '\\' + subvideodir
                blvmode = False
                blvlist = []
                #m4s改成mp4,blv改成flv
                if os.path.isfile(subvideorealpath + '\\' + '0.blv'):
                    for x in os.listdir(subvideorealpath):
                        if '.blv' in x:
                            blvlist.append(x)
                    for x in blvlist:
                        os.rename(subvideorealpath + '\\' + x, subvideorealpath + '\\' + os.path.splitext(x)[0]+'.flv')
                    blvmode = True
                if os.path.isfile(subvideorealpath + '\\' + 'audio.m4s'):
                    os.rename(subvideorealpath + '\\' + 'audio.m4s', subvideorealpath + '\\' + 'audio.mp4')
                if os.path.isfile(subvideorealpath + '\\' + 'video.m4s'):
                    os.rename(subvideorealpath + '\\' + 'video.m4s', subvideorealpath + '\\' + 'video.mp4')
                #合成
                if videoformat=='mkv':
                    if blvmode:
                        if len(blvlist)>1:
                            print(subvideorealpath,'存在多个blv文件，请手动合并。')
                        else:
                            subp = subprocess.Popen(r'"{}" -y -i "{}" -c copy "{}"'.format(os.getcwd()+'\\tools\\ffmpeg.exe',os.getcwd()+'\\'+subvideorealpath + '\\' + blvlist[0].replace('.blv','.flv'),os.getcwd()+'\\'+outpath+'\\'+videoname+'_'+subname+'_'+bvid+'.mkv'),shell=True)
                    else:
                        subp = subprocess.Popen(r'"{}" -o "{}" "{}" "{}"'.format(os.getcwd()+'\\tools\\mkvmerge.exe',os.getcwd()+'\\'+outpath+'\\'+videoname+'_'+subname+'_'+bvid+'.mkv',os.getcwd()+'\\'+subvideorealpath + '\\' + 'video.mp4',os.getcwd()+'\\'+subvideorealpath + '\\' + 'audio.mp4'),shell=True)
                else:
                    if blvmode:
                        if len(blvlist)>1:
                            print(subvideorealpath,'存在多个blv文件，请手动合并。')
                        else:
                            subp = subprocess.Popen(r'"{}" -y -i "{}" -c copy "{}"'.format(os.getcwd()+'\\tools\\ffmpeg.exe',os.getcwd()+'\\'+subvideorealpath + '\\' + blvlist[0].replace('.blv','.flv'),os.getcwd()+'\\'+outpath+'\\'+videoname+'_'+subname+'_'+bvid+'.mp4'),shell=True)
                    else:
                        subp = subprocess.Popen(r'"{}" -add "{}#trackID=1:par=1:1:name=" -add "{}:name=" -new "{}"'.format(os.getcwd()+'\\tools\\MP4Box.exe',os.getcwd()+'\\'+subvideorealpath + '\\' + 'video.mp4',os.getcwd()+'\\'+subvideorealpath + '\\' + 'audio.mp4',os.getcwd()+'\\'+outpath+'\\'+videoname+'_'+subname+'_'+bvid+'.mp4'),shell=True)
                subp.wait(1000000000000000)
                #把扩展名改回去
                if os.path.isfile(subvideorealpath + '\\' + 'audio.mp4'):
                    os.rename(subvideorealpath + '\\' + 'audio.mp4', subvideorealpath + '\\' + 'audio.m4s')
                if os.path.isfile(subvideorealpath + '\\' + 'video.mp4'):
                    os.rename(subvideorealpath + '\\' + 'video.mp4', subvideorealpath + '\\' + 'video.m4s')
                if blvmode:
                    for x in blvlist:
                        os.rename(subvideorealpath + '\\' + x.replace('.blv','.flv'), subvideorealpath + '\\' + x)
