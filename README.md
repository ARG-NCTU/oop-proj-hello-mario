進入docker後輸入下列指令即可進入遊戲:
```
source require.sh
```
```
python3 main.py
```
若還是有ALSA的問題的話試試看輸入
```
aplay -l
```
看是否有正確安裝並識別音頻設備

有的話輸入
```
export AUDIODEV=hw:2,0
```
```
speaker-test -D hw:2,0 -t wav -c 2
```
測試聲音

有聲音的話就可以ctrl-c出來執行main.py