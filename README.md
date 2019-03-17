# BrickHit-Pygame
借鉴东方黑历史作-东方灵异传的游戏模式，重制简化版的‘打砖块’游戏。

### 待完成的功能：

* 弹幕攻击系统
* 特殊砖块复刻
* 关卡复刻
* 分数系统
* Bomb攻击

### 废弃的功能：

* Boss战


* 重力影响
* 特殊击球模式
* 超时全屏随机弹攻击

### 待新增的功能：

* 弹幕：免伤（时）、爆破攻击单位（子弹\灵力球）


## 文件说明

`frame.Block.py` 

* 具备发球系统、碰撞系统、生命值
* 仅初始化所有砖块(完成后重复第一关)
* 分数只与碰撞与否有关

`alpha.Block.level.py`

* 添加关卡系统
* 添加新砖块(HP2,不可破坏,虫洞)
* 修复同时击中多个砖块、从侧面击中时的碰撞问题(暂定)

`Reform.frame.OOP.py`

* 以OOP重构了部分代码
* 碰撞部分使用`pygame.sprite` 代替坐标逻辑判断
* 外部文件： `ball_static.png`