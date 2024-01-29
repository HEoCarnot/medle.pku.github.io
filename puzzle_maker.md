# Puzzle maker !!

方便地制作具有复杂重复的medle谜题！

## 使用方法(mode=1，折叠部分重复音符)

1. 先根据时值填写完整的乐谱，不要写任何重复（如 `puzzles\unhandled`内的 `FLWz.yml`所示），文件内至少要有 `tune:`入口，每行的列表长度为2（midi2tune可以完成这一步的工作）
2. 根据你的需要，在你需要折叠的相同音符后面添加一个字符（折叠好后如 `puzzles\unhandled`内的 `FLW.yml`所示，可以是任意字符），不需要折叠的部分不需要更改，并且命名为 `XXX.yml`，放在 `puzzles\unhandled`内，每行列表最长为3
3. 在 `puzzles`文件夹之外运行 `"3. puzzle_maker.exe"`，命令为

```
"3. puzzle_maker.exe" -n XXX
```

4. 折叠好的 `.yml`为 `puzzles\`内的 `XXX.yml`（如 `puzzles\`内的 `FLW.yml`所示）。

TRY IT OUT：修改 `puzzles\unhandled\FLW.yml`，然后运行

```
"3. puzzle_maker.exe" -n FLW
```

再点击页面左上角问号，翻到最下面的“显示隐藏关”，看看FLW，有没有你想要的效果？

## 使用方法(mode=2，完全指定播放顺序和折叠方式)

1. 先根据时值填写完整的乐谱，不要写任何重复（如 `puzzles\unhandled`内的 `RIDz.yml`所示），文件内至少要有 `tune:`入口，每行的列表长度为2（midi2tune可以完成这一步的工作）
2. 根据你的需要，在每一个音符后面都添加一个数字，表明这个音符将会出现在第几个泡泡内（折叠好后如 `puzzles\unhandled`内的 `RID.yml`所示，最好是数字，会根据所填的数字从小到大排序），并且命名为 `XXX.yml`，每行列表长度均为3
3. 在 `puzzles`文件夹之外运行 `"3. puzzle_maker.exe"`，命令为

```
"3. puzzle_maker.exe" -n XXX -m 2
```

4. 折叠好的 `.yml`为 `puzzles\`内的 `XXX.yml`（如 `puzzles\`内的 `RID.yml`所示）。

TRY IT OUT：修改 `puzzles\unhandled\DDC.yml`，然后运行

```
"3. puzzle_maker.exe" -n DDC -m 2 
```

再点击页面左上角问号，翻到最下面的“显示隐藏关”，看看FLW，有没有你想要的效果？
