import subprocess

def get_hostname_ip():
	try:
		ip_raw = subprocess.check_output(["hostname","-I"])
		ip_byte = ip_raw.decode()

		ip_list = []
		i = 0
		do = True
		while do ==True:
			if ip_byte[i] == ' ':
				do = False
				break
			else:
				ip_list.append(ip_byte[i])
			i += 1
		ip = "".join(ip_list)
		#print(ip_list)
		#print()
		#print(ip)
	except:
		ip = '0.0.0.0'
	return(ip)
