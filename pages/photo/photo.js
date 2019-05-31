var app = getApp();
var Util = require('../../utils/util.js');
Page({
  data: {
    globalData: {
      appid: 'wxd4e0e047d21a49a6',
      secret: 'fc1723ed52bd55847919f050e4dd4782',
    },
    tip_text: [
      "请先授权登录",
      "拍摄时请确保待识别主体清晰",
      "尽量使主体占图片大部分区域"
    ],
    userGlobal: null,
    canIUse: true
  },
  onLoad: function(){
    var that = this;
    var user = wx.getStorageSync('user') || {};
    if(user.openid){
      that.setData({
        userGlobal: user,
        canIUse: false
      })
    }
  },
  getInfo: function(){
    var that = this;
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
              //console.log(result.data);
              var obj = {};
              obj.openid = result.data.openid;
              wx.setStorageSync('user', obj);
              that.setData({
                userGlobal: obj,
                canIUse: false
              });
              wx.showToast({
                title: '授权成功',
                icon: 'success',
                duration: 2000
              });
            }
          });
        }
        else {
          console.log('获取用户code失败');
        }
      }
    });
  },
  takePhoto: function(){
    var that = this;
    var user = wx.getStorageSync('user') || {};
    if (!user.openid) {
      wx.showModal({
        title: '提示',
        content: '请点击授权登录',
        success(res) {
          if (res.confirm) {
            console.log('确定')
          } else if (res.cancel) {
            console.log('取消')
          }
        }
      })
    }
    else{
      wx.chooseImage({
        count: 1,
        sizeType: ['original', 'compressed'],
        sourceType: ['album', 'camera'],
        success: function (res) {
          var timestamp = Date.parse(new Date());
          var tempFilePaths = res.tempFilePaths;
          wx.showLoading({
            title: '识别中',
          });
          wx.uploadFile({
            url: 'https://www.animalidentify.top:5000/recognition',
            filePath: tempFilePaths[0],
            name: 'file',
            header: {
              "Content-Type": "multipart/form-data",
              'accept': 'application/x-www-form-urlencoded',
            },
            formData: {
              "name": that.data.userGlobal.openid
            },
            success: function (res) {
              wx.hideLoading();
              var datastr = JSON.stringify(res.data);
              wx.navigateTo({
                url: '../detect/detect?result=' + datastr                          
              });
            }
          });
        }
      });
    }
  },
  bindGetUserInfo(e) {
    var that = this;
    that.setData({
      userInfoGlobal: e.detail.userInfo
    });
    wx.setStorageSync('userInfo', that.data.userInfoGlobal);
    this.getInfo();
  }
})