Page({
  data: {
    swiperCurrent: 0,
    indicatorDots: true,
    autoplay: true,
    interval: 3000,
    duration: 800,
    circular: true,
    imgUrls: [
      '../../images/bar0.jpg',
      '../../images/bar1.jpg',
      '../../images/bar2.jpg'
    ],
    rate: [
      '../../images/no1.jpeg',
      '../../images/no2.jpeg',
      '../../images/no3.jpeg'
    ],
    recommens: []
  },
  //轮播图的切换事件
  swiperChange: function (e) {
    this.setData({
      swiperCurrent: e.detail.current
    })
  },
  //点击指示点切换
  chuangEvent: function (e) {
    this.setData({
      swiperCurrent: e.currentTarget.id
    })
  },
  onShow: function(){
    var that = this;
    wx.request({
      url: 'https://www.animalidentify.top:5000/home',
      method: 'GET',
      success: function (result) {
        var json = result.data;
        if (typeof json != 'object') {
          if (json != null) {
            json = json.replace("\ufeff", "")
            var ob = JSON.parse(json)
            that.setData({
              recommens: ob
            });
          }
        } 
        else {
          that.setData({
            recommens: json
          });
        }
        /*var temp = result.data;
        that.setData({
          recommens: temp
        });*/
      }
    });
  },
  turnDetail: function(event){
    var that = this;
    wx.request({
      url: 'https://www.animalidentify.top:5000/detail',
      method: 'GET',
      data: {
        name: event.target.dataset.name
      },
      success: function (result) {
        //console.log(result.data);
        var temp = result.data.des[0];
        wx.navigateTo({
          url: '../detail/detail?des=' + temp + '&url=' + event.target.dataset.url + '&name=' + event.target.dataset.name,
        })
      }
    });
  }
})