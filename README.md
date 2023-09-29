## **WelearnFinishALL**

Based on [this repo](https://gitee.com/xxxhhy/welearn-curriculum-finsh).

fixed that the script fails on macOS due to the maximum line length is 1024(Kernel Restriction) which is smaller than the cookies itself.

**Usage**	Pass the cookies thru command line or create a file named `cookies.txt` and paste your cookies in it.

**Notice**	As stated above, on macOS one should store the cookies in a file instead of pasting them directly in the terminal(otherwise the string would be cut off). but if you have to use clipboard, try this:

```bash
pbcopy | python ./WelearnCurriculumFinish.py # pass by command line
```

Manually specify `cookies.txt` path:

```bash
cat {PATH-TO-COOKIES} - | python ./WelearnCurriculumFinish.py # DONOT forget the DASH
```

`-`is treated as `stdin` so that when piping the cookies to the script it does not end with an EOF.

**-----Original README Below-----**

> ## 简介
>
> * 输入账号密码或cookie登录并一键完成课程
> * 可以选择课程
> * 可指定每章节正确率
> * 已完成和未开放的章节会自动跳过
>
> * 有些朋友不会获取cookies,特推出此教程[welearn获取cookies教程](https://v.youku.com/v_show/id_XNTkwNTQwOTc4MA==.html)
>
> ## 更新日志
>
> ### ` 0.7dev`
> * 更新了软件内部说明, 登陆模块晚一点再更新
>
> ### ` 0.6dev`
> * 感谢@[yccd01](https://gitee.com/yccd01)提供的pr修复了登陆模块 
>
> ### ` 0.5dev` 
>
> * 修复了上个版本链接错误
> * 修复了一些逻辑错误
>
> ### `0.4dev`
> * 会跳过未开放的章节了
> * 支持cookie登录了
> * 可以指定或随机正确率
>
> ### `0.3dev`
> * 更pythonic（感谢SSmJaE大佬）
> * 支持学习指定单元了
>
> ### `0.2dev`
> * 支持更多课程
> * 优化代码
>
> ### `0.1dev`
> * 敲出首个版本的代码
