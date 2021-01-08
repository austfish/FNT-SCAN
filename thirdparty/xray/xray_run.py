import queue
import simplejson
import threading
import subprocess
import requests
import warnings
warnings.filterwarnings(action='ignore')

def get_data():
	with open('./1.json','r',encoding='utf8')as fp:
		json_data = json.load(fp)
		print('这是文件中的json数据：',json_data)

def main():
	cmd = ["./xray_windows_amd64.exe", "webscan", "--listen","127.0.0.1:7777", "--json-output","1.json"]
	rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = rsp.communicate()
	# try:
	# 	result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
	# except:
	# 	return
	# req_list = result["req_list"]
	# sub_domain = result["sub_domain_list"]
	# print(data1)
	# print("[crawl ok]")
	# try:
	# 	for subd in sub_domain:
	# 		opt2File2(subd)
	# except:
	# 	pass
	print("[scanning]")

if __name__ == '__main__':
	main()
