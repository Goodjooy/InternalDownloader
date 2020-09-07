# -*- coding: utf-8 -*-
# @Author: FrozneString
# @Date:   2020-08-28 15:01:24
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:28:58
import math
import os
import re
import time
#from struct_class import ThreadData
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from contextlib import closing

import requests

from struct_class import DownloadCtrl, ThreadData
from theard_work import downloader


class ZeroDownloadError(Exception):
    pass 
re_charset = re.compile(r'^(?:charset=)(.+?)$')

def bit_transfrom(bit, var=2, edge=0.9):
    b2kb = bit/1024
    kb2mb = b2kb/1024
    mb2gb = kb2mb/1024
    gb2tb = mb2gb/1024

    if b2kb <= edge:
        return f"{round(bit,var)} B/S\t\t"
    elif b2kb > edge and kb2mb <= edge:
        return f"{round(b2kb,var)} KB/S\t\t"
    elif kb2mb > edge and mb2gb <= edge:
        return f"{round(kb2mb,var)} MB/S\t\t"
    elif mb2gb > edge and gb2tb <= edge:
        return f"{round(mb2gb,var)} GB/S\t\t"
    else:
        return f"{round(gb2tb,var)} TB/S\t\t"


def work_fff(url="https://dl-hdslb-com.oss-cn-shanghai.aliyuncs.com/bili/bililive/win/Livehime-Win-beta-3.19.2.1737.exe",
             timeout=100,
             params=None,
             headers=None,
             save_path="out",
             cookies={}
             ):
    url = url
    timeout = timeout
    params = params
    headers = headers
    # 单次下载的字节
    chunk_size = 1024
    # 最多线程数
    theard_size = 16
    # 总工作次数
    total_work_count = 0
    # 文件类型
    file_type = None
    file_ex = None
    file_encode = None
    # 是否可分块
    split_downlaod = False
    # 分块尺寸
    each_size = 0
    file_size = 0
    # 请求头
    res = requests.get(url=url, timeout=timeout, stream=True,
                       params=params, headers=headers, cookies=cookies)
    try:
        res_headers = res.headers
        # print(res_headers)
        # 文件类型处理
        file_type_temp = res_headers.get("Content-Type")
        temp_2 = file_type_temp.split(";")
        file_type = temp_2[0].split("/")[0]
        file_ex = temp_2[0].split("/")[1]
        if len(temp_2) == 1:
            file_encode = None
        else:
            re_group = re_charset.match(temp_2[1].strip())
            if re_group is None:
                file_encode = None
            else:
                file_encode = re_group.group(1)
        # 是否支持分块下载
        if res_headers.get("Accept-Ranges") is not None:
            split_downlaod = True

        # 文件尺寸处理
        file_size = res_headers.get("Content-Length")
        if file_size is None:
            file_size = 0

            each_size = 0
        else:

            each_size = math.ceil(int(file_size)/theard_size)
    finally:
        res.close()

    thread_group = {}
    err_group = []
    target_path = os.path.join(save_path, "temp_files")
    os.makedirs(target_path, exist_ok=True)
    # 生成range
    if split_downlaod:
        for i in range(theard_size):
            start = each_size*i
            if i == theard_size-1:
                end = int(file_size)-1
            else:
                end = start+each_size-1

            temp = ThreadData(i)

            temp.range = (start, end)
            temp.path = os.path.join(target_path, f"temp-{i}.tmp")
            thread_group[i] = temp

        def updata(downloaded, thread_count, is_done):
            thread_group[thread_count].downloaded_size = downloaded
            thread_group[thread_count].is_done = is_done

        def err(thread):
            err_group.append(thread_group[thread])

        task_group = []
        # 启动线程池
        with ThreadPoolExecutor(theard_size) as tp:
            for i in range(theard_size):
                temp = tp.submit(downloader, i, url,
                                 thread_group[i], updata, err, timeout, cookies)
                task_group.append(temp)

            zero_speed_time = 0
            need_reset = False
            old_size = 0
            while len(list(filter(lambda x: not x.is_done, thread_group.values()))):
                down = 0
                for j in thread_group.values():
                    down += j.downloaded_size

                add_bits = down-old_size
                speed = bit_transfrom((add_bits)/0.25, 1, 1)
                print(
                    f'downloading \t[{down}/{file_size}]\t【{round(100*(down/int(file_size)),4,)}%】\t{speed}', end="\r")
                time.sleep(0.25)
                old_size = down
                if int(down) == int(file_size):
                    print()
                    break
                if add_bits == 0:
                    zero_speed_time += 1
                if add_bits != 0:
                    zero_speed_time = 0
                if zero_speed_time >= 10:
                    need_reset = True
                if need_reset:
                    # 开始重新分配任务
                    # break
                    pass
            print()
            print("处理重置任务")

            # 循环，直到所有重置任务完成
            while True:
                break

        # 合并文件
        print("合并文件中")
        lenth = 0
        file_name = os.path.basename(url)
        if os.path.splitext(file_name)[1] == '':
            file_name += f".{file_ex}"
        file_path = os.path.join(save_path, file_name)
        with open(file_path, "wb") as fp:
            for f in thread_group.values():
                f = f.path
                with open(f, "rb") as temp:
                    data = temp.read()
                    lenth += len(data)
                    fp.write(data)
        print("完成")

    else:
        print(f"\"{url}\" 不支持多线程下载")

def downloader(thread_count, url, thread_data, updata, err, timeout=10, cookies={}):
    t_range = thread_data.range
    headers = {'Range': 'bytes=%d-%d' % (t_range[0], t_range[1])}
    dwonloaded_size = 0
    is_done = False
    try:
        with closing(requests.get(url, headers=headers, stream=True, timeout=timeout, cookies=cookies)) as target:
            chunk_size = 1024
            target_headers = target.headers
            size = target_headers.get("Content-Length")
            # 请求完成，开始写入
            try:
                # 打开文件，while循环，下载完成后退出
                fp = open(thread_data.path, "wb")
                # 下载迭代器，None为有数据就写入
                data_iter = target.iter_content(chunk_size=chunk_size)
                while True:
                    try:
                        a = time.time()
                        data = next(data_iter)
                        b = time.time()
                    except StopIteration:
                        break
                    else:
                        # 如果数据长度为0，触发错误，退出
                        if len(data) == 0:
                            raise ZeroDownloadError("下载的数据大小为0！")
                        # 写入数据
                        dwonloaded_size += len(data)
                        fp.write(data)

                        if dwonloaded_size == size:
                            is_done = True
                        updata(dwonloaded_size, thread_count, is_done)
            finally:
                # 等待文件写入完成
                fp.flush()
                os.fsync(fp)
                fp.close()

        updata(dwonloaded_size, thread_count, is_done)
    except Exception as info:
        print(info)
        err(thread_count)
    finally:
        return dwonloaded_size, t_range


def main(url, save):
    pass

if __name__ == "__main__"and False:
    cookie = {
        "BDUSS": "I4VGJ0MWxVYWx4dU8xQkhIaVFQLWRVRlc2MnVvSnhVRzhGNE02QkZ3ek9XbXhmSUFBQUFBJCQAAAAAAAAAAAEAAAAkQYUjd3lxenl5OTgzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM7NRF~OzURfUG"

    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    #target = input("输入目标网址：\t")
    #save = input("输入保存路径：\t")
    target = "https://pkg.biligame.com/games/mrfz_1.1.80_20200818_034434_d5bd5.apk"
    save = "./aaaa"
    d = DownloadCtrl(target, save)
    d.cookies = cookie
    d.headers = headers
    d.thread_num = 16
    d.read_timeout = 10
    d.initial_download()
    d.start_download()
    dd = {"A":
          {'Date': 'Tue, 25 Aug 2020 07:03:55 GMT',
           'Content-Type': 'application/octet-stream',
           'Connection': 'keep-alive',
           'x-bs-file-size': '1062558879',
           'x-bs-meta-crc32': '2127565706',
           'Cache-Control': 'max-age=259200',
           'ETag': '8b6f2251791edb7ec49de4306ba3e215',
           'x-bs-client-ip': 'MTEwLjgxLjgwLjc2',
           'Content-Length': '1062558879',
           'x-bs-request-id': 'MTAuMTM0LjM0LjE2NjoyMTgwOjU1MTEyNTc2MTAwOTI2NzM2MDE6MjAyMC0wOC0yNSAxNTowMzo1NA==',
           'Content-Disposition': 'attachment;filename="SenrenBanka_Steam_Patch_v101.7z"',
           'Content-MD5': '8b6f2251791edb7ec49de4306ba3e215',
           'superfile': '2',
           'Accept-Ranges': 'bytes',
           'Last-Modified': 'Tue, 25 Feb 2020 08:23:40 GMT',
           'Server': 'POMS/CloudUI 1.0'}
          }
   # BAIDUID	77FFD77B7C26C1A5F407D5C66542675A:FG=1
   # 	BIDUPSID	77FFD77B7C26C1A5685E014F572B81C3		PSTM	1596710605	.baidu.com	/	2088-08-24T13:57:33.639Z	14				Medium	PANWEB	1	.pan.baidu.com	/	2021-08-09T02:55:09.771Z	7				Medium	BDCLND	Sra%2FUQ29ab0FYNPFVSYsU1es6Y18H7OX9PlGmMuPr6M%3D	.pan.baidu.com	/	2020-09-12T00:58:53.759Z	54				Medium	BDORZ	B490B5EBF6F3CD402E515D22BCDA1598	.baidu.com	/	2020-08-26T08:30:03.943Z	37				Medium	BDUSS	16Z0NZdVZSdndEU0IyTTlnZzhuZU55VEtWRFhYN25rcXRSWVhZcEM4S2hRbXhmSUFBQUFBJCQAAAAAAAAAAAEAAAAkQYUjd3lxenl5OTgzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKG1RF-htURfUy	.baidu.com	/	会话	197	✓			Medium	BDUSS_BFESS	16Z0NZdVZSdndEU0IyTTlnZzhuZU55VEtWRFhYN25rcXRSWVhZcEM4S2hRbXhmSUFBQUFBJCQAAAAAAAAAAAEAAAAkQYUjd3lxenl5OTgzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKG1RF-htURfUy	.baidu.com	/	会话	203	✓	✓	None	Medium	STOKEN	ef9763edd4b6aceb9da936798dc9504869434e82ea9adf15bf552c43df064ac5	.pan.baidu.com	/	2020-09-24T06:54:28.451Z	70	✓			Medium	SCRC	a7afedf54a06fbab4ef6b09ecf6c9cce	.pan.baidu.com	/	2020-09-24T06:54:28.452Z	36	✓			Medium	Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0	1598173285,1598252456,1598252458,1598338469	.pan.baidu.com	/	2021-08-25T08:27:46.000Z	82				Medium	delPer	0	.baidu.com	/	会话	7				Medium	PSINO	7	.baidu.com	/	会话	6				Medium	Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0	1598344067	.pan.baidu.com	/	会话	50				Medium	PANPSC	12050909226146976753%3AKkwrx6t0uHDAtJNsGV0Wi4YFB6Yu73HpHV2beobRI3GyderVeN3AzxM4dDjxBdlpZzdYMQXAWf%2FuczPXh9vxj%2BMXgoqh%2F54j879VQip9KUe9gPFKL%2FgAW9NRP5A5EemHkL2qAeJq7%2BV1Lxzud0jMsTEZmK5RR4JqhfSnrP2UPxXuD7k8za9a6w%3D%3D	.pan.baidu.com	/	2020-08-26T08:27:47.158Z	227	✓			Medium	H_PS_PSSID		.baidu.com	/	会话	10				Medium


# 16Z0NZdVZSdndEU0IyTTlnZzhuZU55VEtWRFhYN25rcXRSWVhZcEM4S2hRbXhmSUFBQUFBJCQAAAAAAAAAAAEAAAAkQYUjd3lxenl5OTgzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKG1RF
