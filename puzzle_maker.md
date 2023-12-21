# Puzzle maker !!

方便地制作具有复杂重复的medle谜题！

## 使用方法(mode=1，折叠部分重复音符)

1. 先根据时值填写完整的乐谱，不要写任何重复（如 `FLWz.yml`所示），文件内至少要有 `tune:`入口，每行的列表长度为2
2. 根据你的需要，在你需要折叠的相同音符后面添加一个字符（如 `FLWu.yml`所示，可以是任意字符），不需要折叠的部分不需要更改，并且命名为 `XXXu.yml`，每行列表最长为3
3. 在 `puzzles`文件夹之外运行 `python "3. puzzle_maker.py"`，命令为

```
python "3. puzzle_maker.py" -n XXX
```

4. 折叠好的 `.yml`为 `XXX.yml`（如 `FLW.yml`所示）。

## 使用方法(mode=2，完全指定播放顺序和折叠方式)

1. 先根据时值填写完整的乐谱，不要写任何重复（如 `RIDz.yml`所示），文件内至少要有 `tune:`入口，每行的列表长度为2
2. 根据你的需要，在每一个音符后面都添加一个数字，表明这个音符将会出现在第几个泡泡内（如 `RIDu.yml`所示，最好是数字，会根据所填的数字从小到大排序），并且命名为 `XXXu.yml`，每行列表长度均为3
3. 在 `puzzles`文件夹之外运行 `python "3. puzzle_maker.py"`，命令为

```
python "3. puzzle_maker.py" -n XXX -m 2
```

4. 折叠好的 `.yml`为 `XXX.yml`（如 `RID.yml`所示）。

## 命令行参数

运行 `python "3. puzzle_maker.py" -h`可得。

```
python "3. puzzle_maker.py" -n <name> [-m <mode>] [-d <directory>]
or: python "3. puzzle_maker.py" --name=<name> [--mode=<mode>] [-dir=<directory>]
Defaults:
  name: 001
  mode: 1
  directory: ./puzzles/
```
