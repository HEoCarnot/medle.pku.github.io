# TOUHOU Medle

请访问：[**fantasyguide.cn/medle/**](https://fantasyguide.cn/medle/)

榆木华佬的原网址：[**medle.akashiya.top**](https://medle.akashiya.top/)（已停服）

鸣谢榆木华！

曲库为东方曲的旋律猜谜游戏，每日更新~

TOUHOU melody puzzle game (available in en/zh)

此版本的特性：

1. 若作答次数超过7次，无论是答错还是答对，都无法再显示答案页面。也就是说，如果没有答对，绝对不会显示答案。
2. language.js中修改了部分项目。

## 面向小白的部署、出题教程

后面这些以数字开头的文件，只要输入一个数字，再按 `Tab`键，即可自动补全

### 部署

1. 安装Node.js
2. 运行 `0. install medle.bat`（可能需要管理员权限）
3. 运行 `9. create folders（不会覆盖已有数据）.ba`t以创建所需要的谜题文件夹
4. 如果出题想要使用辅助工具，需要安装python以及包：ruamel.yaml, music21，也可以使用打包好的exe（不推荐，文件太大了，需要的话去下面的网盘链接里找一找）

### 出题

1. 运行 `1. run medle.bat`
2. 使用宿主或者打谱软件扒谱，导出一份XXX.mid文件，放在puzzles\midi内，建议mid包含拍号、调号、速度信息
3. 运行 `python "2. midi2tune.py" -n XXX`，还有些选项可以通过 `-h`查看，之后puzzles\unhandled内有了一个XXX.yml
4. 对这个.yml进行处理（具体处理方法见 `puzzle_maker.md`），然后 `python "3. puzzle_maker.py" -n XXX`，也有一些选项可以通过 `-h`查看
5. 剪辑MP3音频，放在puzzles\reveal内，并且调整回放偏移量
6. 点击1.步骤中命令行内的网址，并且选择这一个谜题，检查是否有问题
7. 无误的话可以在[网盘链接](https://disk.pku.edu.cn/#/link/AB98C421790DE568D6EC606E5BD2F6AF)内提交puzzles\内的最终yml和音频mp3（打包成一个压缩包）

## [zh] 服务端程序

安装 Node.js，然后运行：

```
npm install
npm run start
```

源码在**木兰公共许可证**下分发，许可证文本见 [COPYING.MulanPubL.md](COPYING.MulanPubL.md)；也可选择遵循 **GNU Affero 通用公共许可证**，文本见 [COPYING.AGPL.md](COPYING.AGPL.md)。

钢琴声音来自 [Salamander Grand Piano](https://sfzinstruments.github.io/pianos/salamander)；字体来自 [Varela Round](https://fonts.google.com/specimen/Varela+Round)、[Font Awesome](https://fontawesome.com/) 与 [Rounded M+](http://jikasei.me/font/rounded-mplus/about.html)。上述资源以及谜题中音乐的作者对作品保留其声明的权利。

## [en] The Server Application

Install Node.js, and then run

```
npm install
npm run start
```

The source code is distributed under the **Mulan Public License**, the text of which is at [COPYING.MulanPubL.md](COPYING.MulanPubL.md); alternatively, follow the **GNU Affero General Public License**, the text of which is at [COPYING.AGPL.md](COPYING.AGPL.md).

The piano samples are from [Salamander Grand Piano](https://sfzinstruments.github.io/pianos/salamander); fonts from [Varela Round](https://fonts.google.com/specimen/Varela+Round), [Font Awesome](https://fontawesome.com/), and [Rounded M+](http://jikasei.me/font/rounded-mplus/about.html). The authors of these resources as well as those of the music in the puzzles reserve all rights they have declared.
