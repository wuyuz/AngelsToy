import json
import os
from uuid import uuid4
import requests # 爬虫课程

from Config import COVER_PATH, MUSIC_PATH, MongoDB

header={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
}

DATA = '{"ret":200,"msg":"声音播放数据","data":{"uid":0,"albumId":424529,"sort":1,"pageNum":1,"pageSize":30,"tracksAudioPlay":[{"index":30,"trackId":7713678,"trackName":"新年恰恰","trackUrl":"/ertong/424529/7713678","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":92,"src":"https://fdfs.xmcdn.com/group12/M00/3B/B2/wKgDXFWcw12y8TanAAtkIsI9320251.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":29,"trackId":7713564,"trackName":"我的快乐style","trackUrl":"/ertong/424529/7713564","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":155,"src":"https://fdfs.xmcdn.com/group8/M01/3B/D1/wKgDYFWcwlKzWOleABNA26oG9m0575.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":28,"trackId":7713768,"trackName":"鱼儿水中游","trackUrl":"/ertong/424529/7713768","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":114,"src":"https://fdfs.xmcdn.com/group11/M07/3C/12/wKgDa1WcxH-yUx0yAA4jOCnkzoo604.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":27,"trackId":7713763,"trackName":"祝你圣诞快乐","trackUrl":"/ertong/424529/7713763","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":91,"src":"https://fdfs.xmcdn.com/group13/M0A/3C/07/wKgDXVWcxJOxETOJAAtXC0jV-tQ007.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"7月前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":26,"trackId":7713762,"trackName":"祖国祖国我们爱你","trackUrl":"/ertong/424529/7713762","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":113,"src":"https://fdfs.xmcdn.com/group9/M06/3B/EA/wKgDZlWcxJSQzwcfAA4N0BoDMdY241.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":25,"trackId":7713760,"trackName":"最美的图画","trackUrl":"/ertong/424529/7713760","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":92,"src":"https://fdfs.xmcdn.com/group14/M00/3C/07/wKgDZFWcxLrzVVEcAAthUHuW9o8311.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":24,"trackId":7713757,"trackName":"愿望","trackUrl":"/ertong/424529/7713757","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":115,"src":"https://fdfs.xmcdn.com/group10/M05/3B/C0/wKgDaVWcxJGzJ7uSAA47_grnQu0333.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":23,"trackId":7713756,"trackName":"异想天开","trackUrl":"/ertong/424529/7713756","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":242,"src":"https://fdfs.xmcdn.com/group13/M04/3C/13/wKgDXlWcxCujLknpAB361yR0knM330.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":22,"trackId":7713682,"trackName":"雪宝宝","trackUrl":"/ertong/424529/7713682","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":80,"src":"https://fdfs.xmcdn.com/group12/M00/3B/B3/wKgDXFWcw3rzzAXUAAn2_rd_TSs416.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":21,"trackId":7713681,"trackName":"洗澡歌","trackUrl":"/ertong/424529/7713681","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":103,"src":"https://fdfs.xmcdn.com/group16/M04/3B/F0/wKgDalWcwovDamwPAAzWCE1KPhg634.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":20,"trackId":7713679,"trackName":"校园的早晨","trackUrl":"/ertong/424529/7713679","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":170,"src":"https://fdfs.xmcdn.com/group7/M0A/3C/83/wKgDWlWcw4ayhRYzABUJGT5KiYk025.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":19,"trackId":7713676,"trackName":"摇篮曲","trackUrl":"/ertong/424529/7713676","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":141,"src":"https://fdfs.xmcdn.com/group13/M00/3C/11/wKgDXlWcw4bg7pJVABFuZE2it5M023.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":18,"trackId":7713675,"trackName":"幸福的一家","trackUrl":"/ertong/424529/7713675","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":98,"src":"https://fdfs.xmcdn.com/group12/M00/3B/BA/wKgDW1Wcw3mzthSOAAwwJKKstIo183.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":17,"trackId":7713673,"trackName":"小马车","trackUrl":"/ertong/424529/7713673","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":71,"src":"https://fdfs.xmcdn.com/group11/M06/3C/14/wKgDbVWcwtOgeKw_AAjTUUqlrKg930.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":16,"trackId":7713670,"trackName":"小蚂蚁","trackUrl":"/ertong/424529/7713670","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":62,"src":"https://fdfs.xmcdn.com/group11/M06/3C/14/wKgDbVWcwtXQ0dlHAAe1eRxnsE0477.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":15,"trackId":7713665,"trackName":"小红帽","trackUrl":"/ertong/424529/7713665","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":110,"src":"https://fdfs.xmcdn.com/group15/M0B/3C/33/wKgDZVWcwv2it2_0AA2pv_mYNFU658.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":14,"trackId":7713664,"trackName":"小玉米","trackUrl":"/ertong/424529/7713664","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":98,"src":"https://fdfs.xmcdn.com/group7/M0A/3C/7E/wKgDX1Wcw13z8c8YAAwzfb-5DTc863.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":13,"trackId":7713663,"trackName":"小猪猪","trackUrl":"/ertong/424529/7713663","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":201,"src":"https://fdfs.xmcdn.com/group7/M0A/3C/7F/wKgDX1Wcw2_AiWYsABjbdVPaqLY570.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":12,"trackId":7713662,"trackName":"小猪小猪肥嘟嘟","trackUrl":"/ertong/424529/7713662","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":79,"src":"https://fdfs.xmcdn.com/group7/M0A/3C/83/wKgDWlWcw2yBPuHdAAnSUqLNF0g598.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":11,"trackId":7713660,"trackName":"小毛驴","trackUrl":"/ertong/424529/7713660","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":91,"src":"https://fdfs.xmcdn.com/group12/M04/3B/B1/wKgDXFWcwvKzSpMUAAthUBlZLzc281.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":10,"trackId":7713656,"trackName":"小小发型师","trackUrl":"/ertong/424529/7713656","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":77,"src":"https://fdfs.xmcdn.com/group14/M06/3C/1C/wKgDY1Wcw0_AUxG7AAmWOfM875o604.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":9,"trackId":7713655,"trackName":"小宝贝","trackUrl":"/ertong/424529/7713655","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":145,"src":"https://fdfs.xmcdn.com/group15/M0B/3C/32/wKgDaFWcwtaisdS-ABIEA9keU18436.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":8,"trackId":7713654,"trackName":"小孩应把卫生讲","trackUrl":"/ertong/424529/7713654","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":95,"src":"https://fdfs.xmcdn.com/group15/M0B/3C/33/wKgDZVWcwvaT_e8oAAvfdhfXJNQ861.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":7,"trackId":7713653,"trackName":"小喇叭","trackUrl":"/ertong/424529/7713653","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":85,"src":"https://fdfs.xmcdn.com/group12/M03/3B/B1/wKgDXFWcwtzgy3BgAAqLJj1ijho574.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":6,"trackId":7713652,"trackName":"小可爱","trackUrl":"/ertong/424529/7713652","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":214,"src":"https://fdfs.xmcdn.com/group12/M03/3B/B8/wKgDW1WcwvHzL1FEABqFFMJa4L4742.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":5,"trackId":7713649,"trackName":"学走路","trackUrl":"/ertong/424529/7713649","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":73,"src":"https://fdfs.xmcdn.com/group12/M00/3B/BA/wKgDW1Wcw4zBISExAAkms7-Of3Q290.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":4,"trackId":7713648,"trackName":"学唱数字歌","trackUrl":"/ertong/424529/7713648","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":113,"src":"https://fdfs.xmcdn.com/group12/M00/3B/B2/wKgDXFWcw2mgNQIdAA4EE3MzTKU976.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":3,"trackId":7713647,"trackName":"学习雷锋好榜样","trackUrl":"/ertong/424529/7713647","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":68,"src":"https://fdfs.xmcdn.com/group12/M00/3B/BA/wKgDW1Wcw4fQ7JWWAAh7UKT5m7c703.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":2,"trackId":7713644,"trackName":"一只哈巴狗","trackUrl":"/ertong/424529/7713644","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":86,"src":"https://fdfs.xmcdn.com/group9/M08/3B/CA/wKgDYlWcw5HTULbSAAq9BqdgRXQ509.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true},{"index":1,"trackId":7713643,"trackName":"一双小小手","trackUrl":"/ertong/424529/7713643","trackCoverPath":"//imagev2.xmcdn.com/group9/M04/3B/E1/wKgDZlWcvRKwSOIMAAD3201gPxc590.jpg","albumId":424529,"albumName":"【一千零一夜】经典儿歌","albumUrl":"/ertong/424529/","anchorId":9216785,"canPlay":true,"isBaiduMusic":false,"isPaid":false,"duration":62,"src":"https://fdfs.xmcdn.com/group13/M00/3C/12/wKgDXlWcw5GzJ1NgAAfMZ7UShYY633.m4a","hasBuy":true,"albumIsSample":false,"sampleDuration":0,"updateTime":"2年前","createTime":"4年前","isLike":false,"isCopyright":true,"firstPlayStatus":true}],"hasMore":true}}'
data = json.loads(DATA)  # 转换格式
audio_list = data["data"]["tracksAudioPlay"]  #获取所有有用的数据，音频连接
# print(audio_list)

"""
trackName
trackCoverPath 图片地址 http协议头
albumName
src 歌曲内容地址
"""

content_list = []

for content_info in audio_list:
    content = {
        "title":content_info.get("trackName"),
        "zhuanji":content_info.get("albumName"),
        "cover":"",
        "music":"",
    }

    file_name = uuid4()
    cover_res = requests.get("http:"+content_info.get("trackCoverPath")) #拼接图片地址
    cover_file_name = f"{file_name}.jpg"  #生成唯一名
    cover_file_path = os.path.join(COVER_PATH,cover_file_name)
    with open(cover_file_path,"wb") as fc :
        fc.write(cover_res.content)

    music_res = requests.get(content_info.get("src"))
    music_file_name = f"{file_name}.mp3"
    music_file_path = os.path.join(MUSIC_PATH, music_file_name)
    with open(music_file_path, "wb") as fm:
        fm.write(music_res.content)

    # MongoDB 很快 - json存储 - 不用原生sql语句 - 数据存储方便
    # 数据后期 非常方便 - 用户画像(用户的操作日志) == 钱
    content["cover"] = cover_file_name
    content["music"] = music_file_name

    content_list.append(content)

MongoDB.Content.insert_many(content_list)
# 优势 一次数据库操作 即可完成 全部内容添加
# 劣势 在29个 断掉了 全部结束 Try Exception F
