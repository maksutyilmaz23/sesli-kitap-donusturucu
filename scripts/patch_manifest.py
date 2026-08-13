import re

path = "android/app/src/main/AndroidManifest.xml"
with open(path) as f:
    content = f.read()

perms = [
    "android.permission.FOREGROUND_SERVICE",
    "android.permission.WAKE_LOCK",
    "android.permission.FOREGROUND_SERVICE_DATA_SYNC",
]
insertion = ""
for p in perms:
    if p not in content:
        insertion += f'    <uses-permission android:name="{p}" />\n'
if insertion:
    content = content.replace("<application", insertion + "    <application", 1)


def patch_service(match):
    tag = match.group(0)
    if "foregroundServiceType" in tag:
        return tag
    if tag.endswith("/>"):
        return tag[:-2] + ' android:foregroundServiceType="dataSync" />'
    return tag[:-1] + ' android:foregroundServiceType="dataSync">'


content = re.sub(r"<service\b[^>]*ForegroundService[^>]*/?>", patch_service, content)

with open(path, "w") as f:
    f.write(content)

print("Patched AndroidManifest.xml")
for line in content.splitlines():
    if "FOREGROUND_SERVICE" in line or "ForegroundService" in line:
        print(line)
