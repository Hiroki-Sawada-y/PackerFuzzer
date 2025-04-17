# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
from lib.ApiCollect import Apicollect
from lib.Database import DatabaseType
from lib.common.CreatLog import creatLog, logs
from lib.common.cmdline import CommandLines
from lib.Controller import Project
from lib.common.readConfig import ReadConfig
import os
from lib.ParseJs import ParseJs
from lib.vulnTest import vulnTest
from lib.common.utils import Utils
from lib.getApiText import ApiText
from lib.ApiCollect import Apicollect
from lib.Database import DatabaseType
from lib.FuzzParam import FuzzerParam
from lib.CheckPacker import CheckPacker
from lib.PostApiText import PostApiText
from lib.common.beautyJS import BeautyJs
from lib.Recoverspilt import RecoverSpilt
from lib.CreateReport import CreateReport
from lib.getApiResponse import ApiResponse
from lib.LoadExtensions import loadExtensions
from lib.reports.CreatWord import Docx_replace
from lib.common.CreatLog import creatLog,log_name,logs


class PackUrls:
    def __init__(self):
        self.options = CommandLines().cmd()
        self.codes = {}
        self.config = ReadConfig()
        self.project_tag = logs
        self.log = creatLog().get_logger()
        self.tmp_dir = os.path.join('tmp', self.project_tag)
        os.makedirs(self.tmp_dir, exist_ok=True)

    def sanitize_filename(self, url):
        # URL哈希标识生成
        return url.replace('://', '_').replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_')

    def run(self):
        with open('urls.txt', 'r') as f:
            urls = [url.strip() for url in f if url.strip()]

        for url in urls:
            try:
                projectTag = f"{logs}_{self.sanitize_filename(url)}"
                DatabaseType(projectTag).createDatabase()
                if self.options.silent != None:
                    print("[TAG]" + projectTag)
                # 核心处理流程
                #Project(url, self.options).parseStart()  # 启动项目解析
                ParseJs(projectTag, url, self.options).parseJsStart()  # 解析JS文件

                path_log = os.path.abspath(log_name)
                path_db = os.path.abspath(DatabaseType(projectTag).getPathfromDB() + projectTag + ".db")
                creatLog().get_logger().info("[!] " + Utils().getMyWord("{db_path}") + path_db)  #显示数据库文件路径
                creatLog().get_logger().info("[!] " + Utils().getMyWord("{log_path}") + path_log) #显示log文件路径
                checkResult = CheckPacker(projectTag, url, self.options).checkStart()
                if checkResult == 1 or checkResult == 777: #打包器检测模块
                    if checkResult != 777: #确保检测报错也能运行
                        creatLog().get_logger().info("[!] " + Utils().getMyWord("{check_pack_s}"))
                    RecoverSpilt(projectTag, self.options).recoverStart()
                else:
                    creatLog().get_logger().info("[!] " + Utils().getMyWord("{check_pack_f}"))
                Apicollect(projectTag, self.options).apireCoverStart()                # 收集API

                '''
                # 打包器检测模块
                # 显示数据库和日志路径
                path_log = os.path.abspath(log_name)
                path_db = os.path.abspath(DatabaseType(projectTag).getPathfromDB() + projectTag + ".db")
                creatLog().get_logger().info("[!] " + Utils().getMyWord("{db_path}") + path_db)
                creatLog().get_logger().info("[!] " + Utils().getMyWord("{log_path}") + path_log)
                '''
                
                '''
                # URL哈希标识生成
                safe_name = self.sanitize_filename(url)
                
                # 安全目录创建
                url_dir = os.path.join(self.tmp_dir, safe_name)
                # 安全目录创建
                os.makedirs(url_dir, exist_ok=True)
                target_file = os.path.join(url_dir, f'{safe_name}_apis.txt')
                open(target_file, 'a').close()
                collector = Apicollect(url, self.options)
                collector.apiViolentCollect(target_file)
                self.log.info(f'成功处理URL: {url}')
            '''
            except Exception as e:
                self.log.error(f'处理URL失败 {url}: {str(e)}')

if __name__ == '__main__':
    PackUrls().run()