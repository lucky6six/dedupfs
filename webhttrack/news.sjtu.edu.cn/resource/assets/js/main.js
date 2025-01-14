    // 设置头部链接
    var SetHeadLink = function(){
        $('.navbar .navbar-nav > li').removeClass('active');
        var $info = $('.channelinfo').text();
        if ($info == '交大要闻') {
            $('.navbar .navbar-nav > li:nth-child(2)').addClass('active');
        } else if ($info == '媒体聚焦') {
            $('.navbar .navbar-nav > li:nth-child(3)').addClass('active');
        } else if ($info == '探索发现') {
            $('.navbar .navbar-nav > li:nth-child(4)').addClass('active');
        } else if ($info == '专题专栏') {
            $('.navbar .navbar-nav > li:nth-child(5)').addClass('active');
        } else if ($info == '综合新闻') {
            $('.navbar .navbar-nav > li:nth-child(6)').addClass('active');
        } else if ($info == '活力校园') {
            $('.navbar .navbar-nav > li:nth-child(7)').addClass('active');
        } else if ($info == '首页') {
            $('.navbar .navbar-nav > li:nth-child(1)').addClass('active');
        }
    };

    // 首页学术讲座幻灯片
    var NewsBox = function () {
        //if ($(".newsbox1").length) {
            //$(".newsbox1").bootstrapNews({
               // newsPerPage: 4,
                ////autoplay: true,
                //pauseOnHover: true,
                //direction: 'up',
                //newsTickerInterval: 3000,
                //onToDo: function () {
                    //console.log(this);
                //}
            //});
        //};
    };

    // 幻灯片
    var OwlCarousel = function () {
        // science-slider
        if ($('.ColumnSlider').length) {
            $('.ColumnSlider').owlCarousel({
                items: 3,
                margin: 0,
                stagePadding: 0,
                smartSpeed: 1000,
                loop: true,
                autoplay: true,
                autoplayTimeout: 3000,
                autoplayHoverPause: true,
                nav: false,
                responsive: {
                    0: {
                        items: 2,
                        dots: true
                    },
                    768: {
                        items: 3,
                        dots: false
                    }
                }
            });
        };
    };

    // 溢出省略
    var Dotdot = function () {
        
        setTimeout(function () {
            $('.dot').dotdotdot({
                watch: 'window'
            });
        },0);
        
    };

    //新闻列表显示样式切换
    var CookieView = function () {

        $('.changeView a').click(function () {
            var view = $(this).data('view');
            $(this).parent().addClass('active').siblings().removeClass('active');
            $('[data-view-change]').attr('class','list-card-' + view);
            setTimeout(function () {
                autoImg();
                $('.dot').dotdotdot({
                    watch: 'window'
                });
            },1);
            return false;
        });

        if ($('.changeView').length) {
            var viewStr = $('.changeView .active a').attr('data-view');
            if ($.cookie('view')) {
                var c = $.cookie('view');
                $('.tools-box [data-view='+ c +']').parent().addClass('active').siblings().removeClass('active');
                $('[data-view-change]').attr('class','list-card-' + $.cookie('view'));
            }else {
                $.cookie('view', viewStr, { expires: 1 });
            };
            $('.changeView a').click(function () {
                $.cookie('view', $(this).attr('data-view'), { expires: 1 });
            });
        };
    };

    // IE8,IE9 INPUT输入框提示
    var RunSetValue = function(){
        var browser=navigator.appName;
        var trim_Version=navigator.appVersion.split(";")[1].replace(/[ ]/g,"");
        if(browser=="Microsoft Internet Explorer" && (trim_Version=="MSIE8.0" || trim_Version=="MSIE9.0")) {
            $.each($('input[type=password]'), function(index, val) {
                if (typeof($(this).attr('placeholder')) !== 'undefined') {
                    var remind = '<span class="remind-pwd">'+ $(this).attr('placeholder') +'</span>';
                    $(this).parent().append(remind);
                }
                $('.remind-pwd').click(function(event) {
                    $(this).addClass('hidden');
                    $(this).siblings('input').focus();
                });
                $(this).focus(function(event) {
                    if (!$(this).siblings('.remind-pwd').hasClass('hidden')) {
                        $(this).siblings('.remind-pwd').addClass('hidden');
                    }
                });
                $(this).blur(function(event) {
                    if ($.trim($(this).val()) == "" || $.trim($(this).val()) == null) {
                        $(this).siblings('.remind-pwd').removeClass('hidden');
                    }
                });
            });
            $.each($('input[type=text],textarea'), function(index, val) {
                var str = $(this).attr('placeholder');
                var val_bool = $.trim($(this).val()) == "" ? 1 : 0;
                if (val_bool) {
                    $(this).val(str);
                };
                $(this).focus(function(event) {
                    if ($.trim($(this).val()) == str) {
                        $(this).val('');
                    }
                });
                $(this).blur(function(event) {
                    if ($.trim($(this).val()) == "" || $.trim($(this).val()) == null) {
                        $(this).val(str);
                    }
                });
            });
        }
    };
    
    //添加图片
    var NewsImage = function () {
        function image() {
            addImage();
        }
        
        var imageArr = [{
            title: "新民网",
            url: "/resource/static/shjd/assets/img/article-source/xmw.png"
        },{
            title: "新民晚报",
            url: "/resource/static/shjd/assets/img/article-source/xmwb.png"
        },{
            title: "中国科学报",
            url: "/resource/static/shjd/assets/img/article-source/5zgkxb.png"
        },{
            title: "人民网",
            url: "/resource/static/shjd/assets/img/article-source/rmw.png"
        },{
            title: "人民日报",
            url: "/resource/static/shjd/assets/img/article-source/rmrb.png"
        },{
            title: "光明网",
            url: "/resource/static/shjd/assets/img/article-source/gmw.png"
        },{
            title: "光明日报",
            url: "/resource/static/shjd/assets/img/article-source/gmrb.jpg"
        },{
            title: "经济日报",
            url: "/resource/static/shjd/assets/img/article-source/17jjrb.png"
        },{
            title: "澎湃新闻",
            url: "/resource/static/shjd/assets/img/article-source/pp.png"
        },{
            title: "央广网",
            url: "/resource/static/shjd/assets/img/article-source/ygw.png"
        },{
            title: "中国新闻网",
            url: "/resource/static/shjd/assets/img/article-source/zgxww.png"
        },{
            title: "解放日报",
            url: "/resource/static/shjd/assets/img/article-source/jfrb.png"
         },{
            title: "上观新闻",
            url: "/resource/static/shjd/assets/img/article-source/sgxw.png"
        },{
            title: "东方网",
            url: "/resource/static/shjd/assets/img/article-source/dfw.png"
        },{
            title: "中青在线",
            url: "/resource/static/shjd/assets/img/article-source/zqzx.png"
        },{
            title: "新华网",
            url: "/resource/static/shjd/assets/img/article-source/4xhw.png"
        },{
            title: "文汇报",
            url: "/resource/static/shjd/assets/img/article-source/whb.png"
        },{
            title: "文汇",
            url: "/resource/static/shjd/assets/img/article-source/whb.png"
        },{
            title: "中国教育新闻网",
            url: "/resource/static/shjd/assets/img/article-source/zgjyxww.png"
        },{
            title: "中国科技网",
            url: "/resource/static/shjd/assets/img/article-source/zgkjw.png"
        },{
            title: "新闻晨报",
            url: "/resource/static/shjd/assets/img/article-source/xwcb.png"
        },{
            title: "劳动报",
            url: "/resource/static/shjd/assets/img/article-source/ldb.png"
        },{
            title: "上海科技报",
            url: "/resource/static/shjd/assets/img/article-source/shkjb.png"
        },{
            title: "上海发布",
            url: "/resource/static/shjd/assets/img/article-source/shfb.png"
        },{
            title: "上海热线",
            url: "/resource/static/shjd/assets/img/article-source/shrx.png"
       },{
            title: "扬子晚报网",
            url: "/resource/static/shjd/assets/img/article-source/yzwb.png"
        },{
            title: "中国青年报",
            url: "/resource/static/shjd/assets/img/article-source/zgqnb.png"
        },{
            title: "看看新闻",
            url: "/resource/static/shjd/assets/img/article-source/kkxw.png"
        },{
            title: "中央电视台",
            url: "/resource/static/shjd/assets/img/article-source/cctv.png"
        },{
            title: "中央电视台·视频",
            url: "/resource/static/shjd/assets/img/article-source/cctv.png"
        },{
            title: "央视网",
            url: "/resource/static/shjd/assets/img/article-source/1ysw.jpg"
        },{
            title: "央视影音",
            url: "/resource/static/shjd/assets/img/article-source/2ysyy.jpg"
        },{
            title: "新华社",
            url: "/resource/static/shjd/assets/img/article-source/3xhs.jpg"
        },{
            title: "科学网",
            url: "/resource/static/shjd/assets/img/article-source/6kxw.jpg"
        },{
            title: "China Daily",
            url: "/resource/static/shjd/assets/img/article-source/7ChinaDaily.jpg"
        },{
            title: "CGTN",
            url: "/resource/static/shjd/assets/img/article-source/8CGTN.jpg"
        },{
            title: "SHINE",
            url: "/resource/static/shjd/assets/img/article-source/9SHINE.jpg"
        },{
            title: "文汇网",
            url: "/resource/static/shjd/assets/img/article-source/10whw.png"
        },{
            title: "文汇APP",
            url: "/resource/static/shjd/assets/img/article-source/11whapp.jpg"
        },{
            title: "周到上海",
            url: "/resource/static/shjd/assets/img/article-source/12zdsh.png"
        },{
            title: "青年报",
            url: "/resource/static/shjd/assets/img/article-source/13qnb.png"
        },{
            title: "ICS",
            url: "/resource/static/shjd/assets/img/article-source/14ICS.png"
        },{
            title: "环球时报",
            url: "/resource/static/shjd/assets/img/article-source/15hqsb.jpg"
        },{
            title: "环球网",
            url: "/resource/static/shjd/assets/img/article-source/16hqw.jpg"
        },{
            title: "中国经济网",
            url: "/resource/static/shjd/assets/img/article-source/18zgjjw.jpg"
        },{
            title: "第1财经",
            url: "/resource/static/shjd/assets/img/article-source/19dycj.png"
        },{
            title: "东方财经",
            url: "/resource/static/shjd/assets/img/article-source/20dfcj.jpg"
        },{
            title: "光明号",
            url: "/resource/static/shjd/assets/img/article-source/gmh.jpg"
        },{
            title: "光明日报光明号",
            url: "/resource/static/shjd/assets/img/article-source/gmrbgmh.jpg"
        },{
            title: "人民号",
            url: "/resource/static/shjd/assets/img/article-source/rmh.jpg"
        },{
            title: "人民日报人民号",
            url: "/resource/static/shjd/assets/img/article-source/rmrbrmh.jpg"
        },{
            title: "新华号",
            url: "/resource/static/shjd/assets/img/article-source/xhh.jpg"
        }
	
        ];
        
        function addImage() {
            $('div.source').find("img").remove();
            for (var i = 0; i < imageArr.length; i++){
                $(".source p.img, .source p.img-tag").each(function () {
                    var _tit = $.trim(imageArr[i].title);
                    var _url = $.trim(imageArr[i].url);
                    if ($.trim($(this).text()) == _tit) {
                        $(this).before("<img src=\"" + imageArr[i].url + "\" alt=\"\"/>");
                        $(this).hide();
                        //return false;
                    }
                });     
            }
        }
        if($(".source").length){
            image();
        }
    };

    //手机端导航 & hover下拉
    var RunManiNav = function () {
        //响应式导航--infinitypush.js
        function responsive() {
            if ($(window).width() <= 767) {
                // console.log('mobile navigation');
                $('#mobile-navigation').infinitypush({
                    offcanvasleft: false
                });
                $('body').addClass('mobile');
                $('body').removeClass('desktop');

            } else {
                // console.log('desktop navigation');
                $('#mobile-navigation').infinitypush({
                    destroy: true
                });
                $('body').removeClass('mobile');
                $('body').addClass('desktop');
            }

        }
        function windowResize() {
            $(window).resize(function () {
                responsive();
            });
        }
        responsive();
        windowResize();

        //主导航菜单固定在顶部--stickUp.js
        $(document).ready(function () {
            $('.stickUp-Nav').stickUp();
        });

        //导航 dropdown 鼠标划过自动下拉菜单
        if($(window).width() > 767) {
            if ($('.desktop .dropdown').length) {
                $(".dropdown").hover(
                    function () {
                        $(this).addClass('open');
                        $('.dropdown-menu', this).hide().stop(true, true).fadeIn(300);
                    },
                    function () {
                        $(this).removeClass('open');
                        $('.dropdown-menu', this).stop(true, true).fadeOut(50);
                    }
                );
            };
        }
    };
    
    // 日期选择
    var Calendar = function () {
        function formatDateTime(Date) {
            var _year = Date.getFullYear();
            var _month = Date.getMonth();
            var _date = Date.getDate();
            _month = _month + 1;
            if(_month < 10){_month = "0" + _month;}
            if(_date<10){_date="0"+_date  }
            return  _year + "-" + _month + "-" + _date;
        }

        $(".date-picker").datetimepicker({
            weekStart: 1,
            startView: 2,
            minView: 2,
            maxView: 2,
            language: 'zh-CN',
            format: 'yyyy-mm-dd'
        }).on('changeDate',function(ev) {
        	var curDay = $(".date-picker").data("datetimepicker").getDate();
        	curDay = formatDateTime(curDay);
        	var param1 = curDay;
			window.open("http://search.sjtu.edu.cn/search-report/lectureSearch?searchStartDate="+param1+"&searchEndDate="+param1);
        	event.stopPropagation();
        });

        // 讲座搜索日期选择
        $(".search-date-picker").datetimepicker({
            weekStart: 1,
            startView: 2,
            minView: 2,
            maxView: 2,
            language: 'zh-CN',
            format: 'yyyy-mm-dd',
            autoclose: true
        });
    };

    // eCharts搜索关键字
    var keywords = function () {
        var ec = document.getElementById('eCharts-add');
        if (ec) {
            var myChart = echarts.init(ec);
            var option = {
                tooltip: {},
                series: [ {
                    type: 'wordCloud',
                    gridSize: 2,
                    sizeRange: [12, 50],
                    rotationRange: [0, 0],
                    shape: 'circle',

                    textStyle: {
                        normal: {
                            color: function () {
                                return 'rgb(' + [
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160)
                                ].join(',') + ')';
                            }
                        },
                        emphasis: {
                            shadowBlur: 10,
                            shadowColor: '#333'
                        }
                    },
                    data: [{
                        name: '闵行校区',
                        value: 10,
                    }, {
                        name: '徐汇校区',
                        value: 9
                    }, {
                        name: '闵行校区图书信息楼',
                        value: 5
                    }, {
                        name: '闵行校区老行政楼',
                        value: 4
                    }, {
                        name: '化学A楼',
                        value: 4
                    }, {
                        name: '交大徐汇校区浩然高科大厦',
                        value: 3
                    }, {
                        name: '上海交通大学徐汇校区中院',
                        value: 3
                    }, {
                        name: '化工学院',
                        value: 3
                    }, {
                        name: '闵行校区法学楼',
                        value: 2
                    }, {
                        name: '闵行校区木兰楼',
                        value: 1
                    }, {
                        name: '生物药学楼',
                        value: 1
                    }, {
                        name: '闵行校区陈瑞球楼',
                        value: 1
                    }, {
                        name: '闵行校区理科群楼',
                        value: 1
                    }]
                } ]
            };
            myChart.setOption(option);
        };
    };

    // 百度地图
    var BaiduMap = function () {
        //创建和初始化地图函数：
        function initMap() {
            createMap(); //创建地图
        }

        //创建地图函数：
        function createMap() {
            var keyword = $(".LectureAdd").html();
            var start = keyword.indexOf("：");
            keyword = keyword.substring(start+1);
            if(keyword.split(" ")[0].trim().length > keyword.split("&nbsp")[0].trim().length) {
            	keyword = keyword.split("&nbsp")[0].trim();
            }else{
            	keyword = keyword.split(" ")[0].trim();
            }
            for(var i = 0; i < markerArr.length; i++){
                var json = markerArr[i];
                if(json.title.trim() == keyword){
                var p0 = json.point.split(",")[0];
                var p1 = json.point.split(",")[1];
                    var map = new BMap.Map("baiduMap"); //在百度地图容器中创建一个地图
                    var point = new BMap.Point(p0, p1); //定义一个中心点坐标
                    map.centerAndZoom(point, 19); //设定地图的中心点和坐标并将地图显示在地图容器中
                    window.map = map; //将map变量存储在全局
                }
            }
            if(window.map) {
            	setMapEvent(); //设置地图事件
                addMapControl(); //向地图添加控件
                addMarker(); //向地图中添加marker
            }else{
            	$(".map").remove();
            }
        }

        //地图事件设置函数：
        function setMapEvent() {
            map.enableDragging(); //启用地图拖拽事件，默认启用(可不写)
            map.enableScrollWheelZoom(); //启用地图滚轮放大缩小
            map.enableDoubleClickZoom(); //启用鼠标双击放大，默认启用(可不写)
            map.enableKeyboard(); //启用键盘上下左右键移动地图
        }

        //地图控件添加函数：
        function addMapControl() {
            //向地图中添加缩放控件
            var ctrl_nav = new BMap.NavigationControl({
                anchor: BMAP_ANCHOR_TOP_LEFT,
                type: BMAP_NAVIGATION_CONTROL_LARGE
            });
            map.addControl(ctrl_nav);
            //向地图中添加缩略图控件
            var ctrl_ove = new BMap.OverviewMapControl({
                anchor: BMAP_ANCHOR_BOTTOM_RIGHT,
                isOpen: 0
            });
            map.addControl(ctrl_ove);
            //向地图中添加比例尺控件
            var ctrl_sca = new BMap.ScaleControl({
                anchor: BMAP_ANCHOR_BOTTOM_LEFT
            });
            map.addControl(ctrl_sca);
        }
        
        //标注点数组
        var markerArr = [{
            title: "徐汇校区新建楼",
            content: "上海市徐汇区广元西路55号",
            point: "121.439859,31.204789",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}     
        },{
            title: "徐汇校区新上院",
            content: "上海市徐汇区广元西路55号",
            point: "121.440696,31.206037",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}  
        },{
            title: "徐汇校区东上院",
            content: "上海市徐汇区广元西路55号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}  
        },{
            title: "徐汇校区老图书馆",
            content: "上海市徐汇区广元西路55号",
            point: "121.4423,31.205291",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}  
        },{
            title: "徐汇校区钱学森图书馆",
            content: "上海市徐汇区广元西路55号",
            point: "121.441866,31.207393",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "徐汇校区包兆龙图书馆",
            content: "上海市徐汇区广元西路55号",
            point: "121.439497,31.206204",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "徐汇校区浩然高科大厦",
            content: "上海市徐汇区广元西路55号",
            point: "121.441362,31.204347",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "徐汇校区哲生馆",
            content: "上海市徐汇区广元西路55号",
            point: "121.439413,31.206571",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "徐汇校区工程馆",
            content: "上海市徐汇区广元西路55号",
            point: "121.440186,31.206869",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "徐汇校区安泰经管学院",
            content: "上海市徐汇区广元西路55号",
            point: "121.439427,31.205988",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}            
        },
        
        
        {
            title: "闵行校区老行政楼",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区陈瑞球楼",
            content: "上海市闵行区东川路800号",
            point: "121.444351,31.031091",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区图书信息楼",
            content: "上海市闵行区东川路800号",
            point: "121.443772,31.032305",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区化学A楼",
            content: "上海市闵行区东川路800号",
            point: "121.436501,31.030176",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区化学B楼",
            content: "上海市闵行区东川路800号",
            point: "121.435645,31.030078",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区第五餐饮大楼",
            content: "上海市闵行区东川路800号",
            point: "121.447887,31.030191",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区东中院",
            content: "上海市闵行区东川路800号",
            point: "121.443979,31.029662",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区木兰楼",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区生物药学楼",
            content: "上海市闵行区东川路800号",
            point: "121.449638,31.036315",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区化工学院",
            content: "上海市闵行区东川路800号",
            point: "121.435645,31.030078",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区法学楼",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区菁菁堂",
            content: "上海市闵行区东川路800号",
            point: "121.436099,31.024403",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区人文学院",
            content: "上海市闵行区东川路800号",
            point: "121.445767,31.028272",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区凯原法学院",
            content: "上海市闵行区东川路800号",
            point: "121.445551,31.030083",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区外国语学院",
            content: "上海市闵行区东川路800号",
            point: "121.446216,31.028207",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区李政道图书馆",
            content: "上海市闵行区东川路800号",
            point: "121.432954,31.031812",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区光明体育馆",
            content: "上海市闵行区东川路800号",
            point: "121.433901,31.025308",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区密西根学院",
            content: "上海市闵行区东川路800号",
            point: "121.445703,31.030314",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区生命学院",
            content: "上海市闵行区东川路800号",
            point: "121.449667,31.036337",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区机械与动力工程学院高田会堂",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区文选医学大楼",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区软件大楼",
            content: "上海市闵行区东川路800号",
            point: "121.448749,31.028691",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区微电子楼",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        },{
            title: "闵行校区理科群楼",
            content: "上海市闵行区东川路800号",
            point: "",
            isOpen: 0,
            icon: {w: 21,h: 21,l: 0,t: 0,x: 6,lb: 5}
        }];
        
        //创建marker
        function addMarker() {
            var keyword = $(".LectureAdd").html();
            var start = keyword.indexOf("：");
            keyword = keyword.substring(start+1);
			if(keyword.split(" ")[0].trim().length > keyword.split("&nbsp")[0].trim().length) {
            	keyword = keyword.split("&nbsp")[0].trim();
            }else{
            	keyword = keyword.split(" ")[0].trim();
            }
            for (var i = 0; i < markerArr.length; i++) {
                var json = markerArr[i];
                if(json.title.trim() == keyword){
                    $("#p").html(keyword);
                    var p0 = json.point.split(",")[0];
                    var p1 = json.point.split(",")[1];
                    var point = new BMap.Point(p0, p1);
                    var iconImg = createIcon(json.icon);
                    var marker = new BMap.Marker(point, {
                        icon: new BMap.Icon("http://api.map.baidu.com/lbsapi/createmap/images/icon.png",
                            new BMap.Size(20, 25), {
                                imageOffset: new BMap.Size('-46', '-21')
                            })
                    });
                    var iw = createInfoWindow(i);
                    var label = new BMap.Label(json.title, {
                        "offset": new BMap.Size(json.icon.lb - json.icon.x + 25, -10)
                    });
                    marker.setLabel(label);
                    map.addOverlay(marker);
                    label.setStyle({
                        borderColor: "#808080",
                        color: "#333",
                        cursor: "pointer"
                    });

                    (function () {
                        var index = i;
                        var _iw = createInfoWindow(i);
                        var _marker = marker;
                        _marker.addEventListener("click", function () {
                            this.openInfoWindow(_iw);
                        });
                        _iw.addEventListener("open", function () {
                            _marker.getLabel().hide();
                        })
                        _iw.addEventListener("close", function () {
                            _marker.getLabel().show();
                        })
                        label.addEventListener("click", function () {
                            _marker.openInfoWindow(_iw);
                        })
                        if (!!json.isOpen) {
                            label.hide();
                            _marker.openInfoWindow(_iw);
                        }
                    })()
                }
            }
        }
        //创建InfoWindow
        function createInfoWindow(i) {
            var json = markerArr[i];
            var iw = new BMap.InfoWindow("<b class='iw_poi_title' title='" + json.title + "'>" + json.title +
                "</b><div class='iw_poi_content'>" + json.content + "</div>");
            return iw;
        }
        //创建一个Icon
        function createIcon(json) {
            var icon = new BMap.Icon("http://app.baidu.com/map/images/us_mk_icon.png", new BMap.Size(json.w,
                json.h), {
                imageOffset: new BMap.Size(-json.l, -json.t),
                infoWindowOffset: new BMap.Size(json.lb + 5, 1),
                offset: new BMap.Size(json.x, json.h)
            })
            return icon;
        }

        if($('#baiduMap').length) {
            initMap(); //创建和初始化地图
        };
    };

    // 滚动条
    var NiceScroll = function () {
        $('body,.scroll').niceScroll({
            // 常用参数，更多参数设置参阅 https://github.com/inuyaksa/jquery.nicescroll
            cursorcolor: '#C8171E', // 颜色 默认 #424242
            cursoropacitymin: 0, // 最小透明度 默认 0
            cursoropacitymax: .7, // 最大透明度 默认 1
            cursorwidth: '8px', // 宽度 默认 5px
            cursorborder: '0', // 边框 默认 '1px solid #fff'
            cursorborderradius: '8px', // 圆角大小 默认 5px
            scrollspeed: 60, // 滚动速度 默认 60
            mousescrollstep: 40, // 鼠标滚动速度 默认 40
            // emulatetouch: true,          // 鼠标拖拽 默认 false
            background: '', // 滚动条背景 默认 无
            horizrailenabled: false, // 水平滚动条 默认 true
            zindex: 100000 // 设置元素 z-index 默认 auto
        });
    };
    
    return {
        init: function () {
            SetHeadLink();
            NewsBox();
            OwlCarousel();
            Dotdot();
            CookieView();
            RunSetValue();
            NewsImage();
            RunManiNav();
            Calendar();
            keywords();
            BaiduMap();
            NiceScroll();
        }
