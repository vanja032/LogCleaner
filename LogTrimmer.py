import subprocess
import time
import os

last_trimmed = 0
backup_num = 5

def trimmer():
    nodine_log_path = "/home/inery-node/inery.setup/master.node/blockchain/nodine.log"
    log_storage = "/log_storage"
    time_created = time.time()
    oldest_file = ""
    return_nodine_size = subprocess.Popen(["sudo", "du", "-hs", nodine_log_path], stdout=subprocess.PIPE)
    size_text = return_nodine_size.communicate()[0].decode()
    size_f = size_text.split("\t")[0]
    if (float(size_f[:-1]) > 200 and size_f[-1] == "G") or ((time.time() - last_trimmed) > 432000):
        for root, dirs, files in os.walk(log_storage):
            if len(files) >= backup_num:
                for file in files:
                    if file.endswith(".zip"):
                        if os.path.getctime(os.path.join(root, file)) < time_created:
                            oldest_file = os.path.join(root, file)
                            time_created = os.path.getctime(os.path.join(root, file))
                if oldest_file != "":
                    subprocess.run(["sudo", "rm", "-rf", oldest_file])
        oldest_file = ""
        subprocess.run(["sudo", "zip", "-r", log_storage + "/nodinelog" + str(time.time()) + ".zip", nodine_log_path])
        subprocess.run(["truncate", "-s", "0", nodine_log_path])

if name == "main":
    while(True):
        try:
            trimmer()
        except:
            pass
        time.sleep(3600)
