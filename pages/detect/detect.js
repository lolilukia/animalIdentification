Page({
  data: {
    originalImage: '',
    res: [],
    resList: [],
    test:''
  },
  onLoad: function(options){
    var that = this;
    var resjson = JSON.parse((JSON.parse(options.result)));
    var originaljson = JSON.parse((JSON.parse(options.result))).url;
    var listjson = JSON.parse((JSON.parse(options.result))).list
    for (var i = 0; i < listjson.length; i++) {
      var score = (listjson[i].score * 100).toFixed(2);
      listjson[i].score = score + '%';
    }
    that.setData({
      res: resjson,
      originalImage: originaljson,
      resList: listjson
    });
  },
  turnDetail: function(event){
    var that = this;
    var temp = event.target.dataset.des;
    wx.navigateTo({
      url: '../detail/detail?des=' + temp + '&url=' + event.target.dataset.imgurl + '&name=' + event.target.dataset.kind,
    });
  }
});