import datetime
import re
import subprocess

result = subprocess.run(['wsl', 'ps', 'aux'],  capture_output=True, text=True)
report_lines = ["Отчёт о состоянии системы:"]
lines = result.stdout.strip().split('\n')
users = []
cpu = 0
mem = 0
proc_mem = ""
proc_cpu = ""
max_mem = 0
max_cpu = 0
for line in lines[1:]:
    match = re.match(r'^(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)', line)
    if match:
        #if users.count(match.group(1)) == 0:
        users.append(match.group(1))
        cpu += float(match.group(3))
        mem += float(match.group(4))
        if float(match.group(4)) > max_mem:
            max_mem = float(match.group(4))
            proc_mem = match.group(11)
        if float(match.group(3)) > max_cpu:
            max_cpu = float(match.group(3))
            proc_cpu = match.group(11)
users_string = ""
for user in list(set(users)):
    users_string = users_string + user + ", "
users_string = users_string[:-2]

report_lines.append("Пользователи системы: " + users_string)
report_lines.append("Процессов запущено: " + str(len(lines)-1))
report_lines.append("")
report_lines.append("Пользовательских процессов: ")
for user in list(set(users)):
    report_lines.append(user + ": " + str(users.count(user)))

report_lines.append("")
report_lines.append("Всего памяти используется: " + str(mem) + "%")
report_lines.append("Всего CPU используется: " + str(cpu) + "%")
report_lines.append("Больше всего памяти использует: " + proc_mem)
report_lines.append("Больше всего CPU использует: " + proc_cpu)

print("\n".join(report_lines))

filename = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
with open(filename, "w") as f:
    f.write("\n".join(report_lines))