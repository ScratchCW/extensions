import os
import zipfile
import json
from tqdm import tqdm
import shutil

"""
将此目录下的所有.sb3（Scratch项目文件）中TurboWarp扩展地址修改为https://extensions.scratch-cw.top/下的扩展（差别是原来的是英文，这个目录下的是中文）
具体步骤：
1.遍历每个.sb3文件
2.使用zipfile解压至文件夹temp（若存在则删除文件夹及其内容）
3.打开temp\project.json，使用json解析其内容存储字典到变量project
4.找到project["extensionURLs"]，若不存在则跳过此文件（也不可能不存在）；否则存储值到extensions变量
5.遍历extensions的所有值，替换其中的所有`https://extensions.turbowarp.org/`为`https://extensions.scratch-cw.top/`
6.将project转回json字符串，写入temp\project.json（ensureANSI=False）
7.将temp压缩为zip文件，覆盖原文件
8.删除temp文件夹
9.回到步骤1，直到遍历完毕
10.输出“完成”
注意：
请使用tqdm库显示转换、解压等操作的进度
"""
def main():
    # 获取当前目录下所有.sb3文件
    sb3_files = [f for f in os.listdir('.') if f.endswith('.sb3')]
    
    # 使用tqdm显示处理进度
    for sb3_file in tqdm(sb3_files, desc="处理.sb3文件"):
        # 步骤2：使用zipfile解压至文件夹temp（若存在则删除文件夹及其内容）
        temp_dir = 'temp'
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # 解压文件
        with zipfile.ZipFile(sb3_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            for file in tqdm(file_list, desc=f"解压 {sb3_file}", leave=False):
                zip_ref.extract(file, temp_dir)
        
        # 步骤3：打开temp\project.json，使用json解析其内容存储字典到变量project
        json_path = os.path.join(temp_dir, 'project.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            project = json.load(f)
        
        # 步骤4：找到project["extensionURLs"]，若不存在则跳过此文件；否则存储值到extensions变量
        if 'extensionURLs' not in project:
            continue
        extensions = project["extensionURLs"]
        
        # 步骤5：遍历extensions的所有值，替换其中的所有`https://extensions.turbowarp.org/`为`https://extensions.scratch-cw.top/`
        for key in extensions:
            extensions[key] = extensions[key].replace('https://extensions.turbowarp.org/', 'https://extensions.scratch-cw.top/')
        
        # 步骤6：将project转回json字符串，写入temp\project.json（ensure_ascii=False）
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(project, f, ensure_ascii=False)
        
        # 步骤7：将temp压缩为zip文件，覆盖原文件
        with zipfile.ZipFile(sb3_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        # 步骤8：删除temp文件夹
        shutil.rmtree(temp_dir)
    
    # 步骤10：输出“完成”
    print("完成")

if __name__ == "__main__":
    main()
