Page({
  data: {
    resList: [],
    listText: ''
  },
  onLoad: function(options){
    var that = this;
    var id = options.id;
    wx.request({
      url: 'https://www.animalidentify.top:5000/record_kind',
      method: 'GET',
      data:{
        name: id
      },
      success: function (result) {
        //console.log(result.data);
        var temp = result.data;
        that.setData({
          listText: temp.length,
          resList: temp
        });
      }
    });
  }
})