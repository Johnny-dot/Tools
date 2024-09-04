环境设置
	确认安装jre-6u45-windows-i586.exe并将...Java\jdk1.6.0_19\bin加到系统环境变量中。

生成apk
1.设置参数
	修改config.bat
	storename 	签名keystore库名
	storepass 	keystore的密码

	aliasname	keystore中的条目名
	keypass		条目的密码

	days		keystore的时效

	package 	应用包名（相同包名的apk在机器上安装后会覆盖）
	output 		输出的apk名
2.生成keystore(若已有则跳过)
	运行genkey.bat，填写相关内容后生成%keyname%.keystore（最后确认y）
3.生成apk
	运行auto-gen-apk.bat

项目相关文件
res
	apk的图片，apk名字等修改在这里
assets
	项目资源放到这里
AndroidManifest.xml
	横/竖屏

如更新引擎，请更新
	1.lib文件夹
	2.classes.dex
