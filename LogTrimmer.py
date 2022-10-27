import subprocess
import time
import os
import datetime

last_trimmed = 0

def trimmer():
    global last_trimmed
    nodine_log_path = "/home/inery-node/inery.setup/master.node/blockchain/nodine.log"
    log_storage = "/log_storage"
    time_created = time.time()
    oldest_file = ""
    return_nodine_size = subprocess.Popen(["sudo", "du", nodine_log_path], stdout=subprocess.PIPE)
    size_text = return_nodine_size.communicate()[0].decode()
    size_f = size_text.split("\t")[0]
    subprocess.run(["echo", "Size of file ", str(size_f), "\n", "Last trimmed ", str(last_trimmed)])
    # 200GB =~ 210,000,000.00 KB
    if (float(size_f) > 210000000) or ((time.time() - last_trimmed) > 432000):
        for root, dirs, files in os.walk(log_storage):
            if len(files) >= 5:
                for file in files:
                    if file.endswith(".zip"):
                        if os.path.getctime(os.path.join(root, file)) < time_created:
                            oldest_file = os.path.join(root, file)
                            time_created = os.path.getctime(os.path.join(root, file))
                if oldest_file != "":
                    subprocess.run(["sudo", "rm", "-rf", oldest_file])
        oldest_file = ""
        subprocess.run(["sudo", "zip", "-r", log_storage + "/nodinelog" + str(time.time()) + ".zip", nodine_log_path])
        subprocess.run(["echo", "Backuped nodine.log file ", str(datetime.datetime.now())])
        subprocess.run(["truncate", "-s", "0", nodine_log_path])
        last_trimmed = time.time()

if __name__ == "__main__":
    while(True):
        try:
            trimmer()
        except Exception as e:
            print(e)
            pass
        time.sleep(3600)
