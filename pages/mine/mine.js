Page({
  data: {
    animalNum: 0,
    mine_info: '物种收集',
    rest_text: '',
    records: [],
    globalData: {
      appid: 'wxd4e0e047d21a49a6',
      secret: 'fc1723ed52bd55847919f050e4dd4782',
    },
  },
  onShow: function () {
    var that = this;
    var that = this;
    var user = wx.getStorageSync('user') || {};
    wx.request({
      url: 'https://www.animalidentify.top:5000/record',
      method: 'GET',
      data: {
        name: user.openid
      },
      success: function (result) {
        //console.log(result.data);
        var temp = result.data;
        for(var i = 0; i < temp.length; i++){
          var group = temp[i].date.split('-');
          temp[i].date = group[0] + '年' + group[1] + '月';
        }
        that.setData({
          records: temp
        });
      }
    });
  },
  turnList: function(){
    var user = wx.getStorageSync('user') || {};
    if(!user.openid){
      wx.login({
        success: function (res) {
          if (res.code) {
            var d = that.data.globalData;
            var codeTemp = res.code;
            wx.request({
              url: 'https://www.animalidentify.top:5000/session',
              method: 'GET',
              data: {
                appid: d.appid,
                secret: d.secret,
                code: codeTemp
              },
              success: function (result) {
                var obj = {};
                obj.openid = result.data.openid;
                wx.setStorageSync('user', obj);
                that.setData({
                  userGlobal: obj,
                });
                wx.navigateTo({
                  url: '../list/list?id=' + obj.openid
                });
              }
            });
          }
          else {
            wx.showModal({
              title: '提示',
              content: '请前往识别页授权登录',
              success(res) {
                if (res.confirm) {
                  console.log('确定')
                } else if (res.cancel) {
                  console.log('取消')
                }
              }
            })
          }
        }
      });
    }
    else{
      wx.navigateTo({
        url: '../list/list?id=' + user.openid
      });
    }
  },
  turnDetail: function (event) {
    var that = this;
    wx.request({
      url: 'https://www.animalidentify.top:5000/detail',
      method: 'GET',
      data: {
        name: event.target.dataset.animal
      },
      success: function (result) {
        //console.log(result.data);
        var temp = result.data.des[0];
        wx.navigateTo({
          url: '../detail/detail?des=' + temp + '&url=' + event.target.dataset.url + '&name=' + event.target.dataset.animal,
        })
      }
    });
  }
})
