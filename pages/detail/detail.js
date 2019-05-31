Page({
  data: {
    headImg: '',
    title: '',
    des: ''
  },
  onLoad: function(options){
    var that = this;
    var imgUrl = options.url;
    var des = options.des;
    var name = options.name;
    that.setData({
      headImg: imgUrl,
      des: des,
      title: name
    })
  }
})