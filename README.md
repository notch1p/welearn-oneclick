## **WelearnFinishALL**

Based on [this repo](https://gitee.com/xxxhhy/welearn-curriculum-finsh).

## Changes

- fixed that the script fails on macOS due to the maximum line length is 1024(Kernel Restriction) which is smaller than the cookies itself.
- Aside from authenticating w/ Cookies, Username & Password login is made possible again (essentially we're getting the cookies from normal login).

## Usage

**TL;DR**	Pass the cookies thru command line or create a file named `cookies.txt` and paste your cookies in it.

- `python finishIt.py`: pass your credentials interactively

...or you can pass by argument

- `--user, -u {USERNAME:PASSWORD}`: pass by credentials

```shell
python -u evan:123456
```



- `--parse, -p {COOKIES}` : pass directly by raw format cookies as shown below

```shell
python -p paste-your-cookies-here
```

  

<img src="https://flexio.blob.core.windows.net/notch1p/2023/09/f562409b874c1da366abbf75535f11fd.png" alt="Raw cookies" style="zoom:50%;" />

**Notice**	As stated above, on macOS one should just input their username & password instead of pasting them directly in the terminal(otherwise the string would be cut off). but if you have to use Raw Cookies from clipboard or files, try *command substitution*:

```shell
python finishIt.py --parse "$(cat {PATH-TO-COOKIES})" # from a file
python finishIt.py --parse "$(pbpaste)" # from clipboard
```



**-----Original README-----**

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
