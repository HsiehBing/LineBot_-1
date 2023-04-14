## 說明: 此機器人是根據HsiehBing/FLASK_SQL的延伸，使line群組裡面的人可以開團，報名參加活動，並串接MySQL

## 功能說明

* "!開團"可以開團中間用;分隔，範例如下：\n!開團;2023-4-13;時間1430,地點:台南高商,人數:上限27、未滿14流團;名字(可不輸入)\n使用"!活動"可以看開團的活動
*** 開團日期需要在當天或當天以後的日期，日期過了會自動不顯示 ***\
* "!活動"查看該群組中所舉辦的活動

* 指令"+"、"+1"、"+人名"可以報名

* 指令"-"、"-1"、"-人名"可以取消報名

* 指令"~"可以查看功能說明

* 指令"DeleteAllDatasFromTable"可以刪除該群組內的活動

* 指令"DeleteDatasFromTableInThisGroup"會將所有群組的資料刪除

### 功能對照

  | 代碼                              | python file | 說明                  |  備註    |
  | :----:                           | :----:       | :----                 |:----:   |
  | !開團                             | OgzFF.py    | 開活動                 |         |
  | !比賽                             | OgzFC.py    | 開比賽                 | 還沒做   |
  | !活動                             | DspAtt.py   | 查詢活動資料與報名人員  |          |
  | + +1 +名字                        | ATG.py      | 報名                   |         |
  | - -1 -名字                        | CFG.py      | 取消報名               |          |
  | DeleteAllDatasFromTable          |              | 刪除該line群活動資料    |         |
  | DeleteDatasFromTableInThisGroup  |              | 刪除所有line群活動資料  |          |


## 相關設定

* 需要串接MySQL，並在Databases中開啟一tesbdb的資料庫


## 設計細節說明


## 待完成/未完成事項

1.兩個群組開同一團
2.一個群組開兩團以上
3.人數到達上限之後轉項目欄轉成候補
4.目前的人物增減會因為資料型態導致","影響判斷，目前先以在讀取時刪除空格處理
5.MVC分離
6.+2,-2的設定
## 參考資料
1.MySQL檢查設定狀態
https://ithelp.ithome.com.tw/articles/10221541
2. MySQL中文顯示不出來解決方案
https://zhuanlan.zhihu.com/p/60605885

