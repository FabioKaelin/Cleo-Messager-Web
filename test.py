import platform
versionsString = platform.python_version()
versionsArray = versionsString.split(".")
versionsString2 = versionsArray[0] + "." + versionsArray[1]
print(versionsString2)

versionsString3 = platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1]
print(platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1])