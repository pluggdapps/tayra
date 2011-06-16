
/** reset.css *********************************************/

html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, font, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td {
	margin: 0;
	padding: 0;
	border: 0;
	outline: 0;
	font-weight: inherit;
	font-style: inherit;
	font-size: 100%;
	font-family: inherit;
	vertical-align: baseline;
}
/* remember to define focus styles! */
:focus {
	outline: 0;
}
body {
	line-height: 1;
	color: black;
	background: white;
}
ol, ul {
	list-style: none;
}
/* tables still need 'cellspacing="0"' in the markup */
table {
	border-collapse: separate;
	border-spacing: 0;
}
caption, th, td {
	text-align: left;
	font-weight: normal;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: "";
}
blockquote, q {
	quotes: "" "";
	margin: 10px 0 10px 20px;
}

/** tabcontent.css *********************************************/

.tabcontent .menu { list-style:none; width:182px; float:left; position: relative; left: 1px; z-index: 50; }
.tabcontent .menu li { margin-bottom:3px; width: 182px; height: 39px; font-weight: bold; background: url(/images/learnmore/section-tab-normal-top.gif) no-repeat left top; padding-top:4px;}
.tabcontent .menu li.isOn {background-image: url(/images/learnmore/section-tab-active-top.gif); }
.tabcontent .menu li.isOn:hover a { cursor:default; text-decoration:none;}
.tabcontent .menu li.multiline a { padding:0px 0 13px 12px; height: 30px;line-height:120%;}
.tabcontent .menu li a { display: block; padding: 8px 0 9px 12px; height: 23px; width: 170px; background: url(/images/learnmore/section-tab-normal-btm.gif) no-repeat left bottom; }
.tabcontent .menu li.isOn a {background: url(/images/learnmore/section-tab-active-btm.gif) no-repeat left bottom;}
.tabcontent .menu a.two-line { padding-top: 2px; padding-bottom: 16px; }

.tabcontent .content { float:left; position:relative; padding: 30px 60px; width: 586px; height:586px; margin-bottom:20px; min-height: 300px; font-size: 12px; line-height: 17px; color: #333333; background-color: #FFFFFF; border: 1px solid #C5DAE7; overflow:hidden; }
.tabcontent .content .topic { position:absolute; left: 1000px; top: 0; display:block;}
.tabcontent .content .topic.isOn {display:block; left:0; }
.tabcontent .content h2 { padding: 0 0 80px; font-size: 19px; line-height: 28px; font-weight: bold; }
.tabcontent .content h2.full { padding: 0 0 20px 0; width: 580px; }
.tabcontent .content h2.QOM { padding: 0 0 80px; width: 320px; font-size: 19px; line-height: 28px; font-weight: bold; }
.tabcontent .content h2.slim { padding: 0; }
.tabcontent .content h3 { font-size: 14px; line-height: 17px; font-weight: bold; color: #4E4E4E; }
.tabcontent .content p { padding: 0 0 20px 0; }
.tabcontent .content .disclaimer p { padding: 0; }
.tabcontent .content .video-watch-panel { float: right; }
.tabcontent .content a { font-weight: bold; }
.tabcontent .content a.noLeftPad { padding-left: 0 !important; }
.tabcontent .content a.magnify { background: url(/images/learnmore/icn_link.jpg) no-repeat right top; padding-right: 20px; padding-left:6px; }
.tabcontent .content .video-watch-panel a { font-weight: bold; font-size: 14px; line-height: 22px; }
.tabcontent .content .image-float { float: left;margin: 0 25px 0 0; width: 140px; height: 100px; clear:left; }
.tabcontent .content .image-float a { font-size: 11px; font-weight: bold; line-height:120%; display:inline-block; }

.tabcontent .content .pie-chart { background: url(/images/learnmore/pi-chart-icon.jpg) no-repeat center top; height:117px; }
.tabcontent .content .whats-left { background: url(/images/learnmore/whats-left-icon.jpg) no-repeat center top; }
.tabcontent .content .piggy-bank { background: url(/images/learnmore/piggybank.jpg) no-repeat center top; height:130px; }
.tabcontent .content .star-grey { background: url(/images/learnmore/star-grey-icon.jpg) no-repeat center top; }
.tabcontent .content .cash-envelope { background: url(/images/learnmore/cash-envelope-icon.jpg) no-repeat center top; }
.tabcontent .content .map-pin { background: url(/images/learnmore/map-pin-icon.jpg) no-repeat center top; }
.tabcontent .content .sms { background: url(/images/learnmore/sms-icon.jpg) no-repeat center top; }
.tabcontent .content .rates { background: url(/images/learnmore/rates.jpg) no-repeat center top; }
.tabcontent .content .bank { background: url(/images/learnmore/bank.jpg) no-repeat center top; }
.tabcontent .content .life-preserver-large { background: url(/images/learnmore/life_preserver_large.jpg) no-repeat center top; }
.tabcontent .content .life-preserver { background: url(/images/learnmore/life_preserver.jpg) no-repeat center top; }
.tabcontent .content .quicken-icon { background: url(/images/learnmore/quicken-logo-icon.jpg) no-repeat center top; }
.tabcontent .content .iphone-icon { background: url(/images/learnmore/iphone-icon.jpg) no-repeat center top; height:181px; }
.tabcontent .content .sm-people { background: url(/images/learnmore/sm-people-icon.jpg) no-repeat center top; }
.tabcontent .content .clock { background: url(/images/learnmore/clock-icon.jpg) no-repeat center top; }
.tabcontent .content .bar-graph { background: url(/images/learnmore/bar_graph.jpg) no-repeat center top; }
.tabcontent .content .globe { background: url(/images/learnmore/globe-icon.jpg) no-repeat center top; }
.tabcontent .content .computer-arrow { background: url(/images/learnmore/computer-arrow-icon.jpg) no-repeat center top; }
.tabcontent .content .computer-cd { background: url(/images/learnmore/computer-cd-icon.jpg) no-repeat center top; }
.tabcontent .content .turbotax-icon { background: url(/images/learnmore/turbotax-icon.jpg) no-repeat center top; }
.tabcontent .content .guarantee { background: url(/images/learnmore/guarantee.jpg) no-repeat center top; }
.tabcontent .content .cash-suitcase { background: url(/images/learnmore/cash-suitcase-icon.jpg) no-repeat center top; }
.tabcontent .content .upgrade { background: url(/images/learnmore/upgrade-box-shot.jpg) no-repeat center top; }
.tabcontent .content .rent-center { background: url(/images/learnmore/rent-center-box-shot.jpg) no-repeat center top; }
.tabcontent .content .rent-center-2 { background: url(/images/learnmore/rent-center-box-shot-2.jpg) no-repeat center top; }
.tabcontent .content .mobile-me { background: url(/images/learnmore/mobile-me-icon.jpg) no-repeat center top; }
.tabcontent .content .sched { background: url(/images/learnmore/schedule-icon.jpg) no-repeat center top; }
.tabcontent .content .computer-transfer { background: url(/images/learnmore/computer-transfer.jpg) no-repeat center top; }
.tabcontent .content .computer-printer { background: url(/images/learnmore/printer.jpg) no-repeat center top; }
.tabcontent .content .building { background: url(/images/learnmore/building.jpg) no-repeat center top; }
.tabcontent .content .compass { background: url(/images/learnmore/compass.jpg) no-repeat center top; }
.tabcontent .content .magnifying-glass { background: url(/images/learnmore/magnifying-glass.jpg) no-repeat center top; }
.tabcontent .content .paper-stack { background: url(/images/learnmore/paper-stack.jpg) no-repeat center top; }
.tabcontent .content .printer { background: url(/images/learnmore/printer.jpg) no-repeat center top; }

.tabcontent .content .fpo { background: url(/images/learnmore/fpo.jpg) no-repeat center top; }

.tabcontent .content .rounded-tl { position: absolute; top: 0; left: 0; width: 4px; height: 4px; background: url(/images/learnmore/rounded-top-left.gif) no-repeat left top; } 
.tabcontent .content .rounded-tr { position: absolute; top: -1px; right: -1px; width: 4px; height: 4px; background: url(/images/learnmore/rounded-top-right.gif) no-repeat left top; }
.tabcontent .content .rounded-bl { position: absolute; bottom: -1px; left: -1px; width: 4px; height: 4px; background: url(/images/learnmore/rounded-bottom-left.gif) no-repeat left top; }
.tabcontent .content .rounded-br { position: absolute; bottom: -1px; right: -1px; width: 4px; height: 4px; background: url(/images/learnmore/rounded-bottom-right.gif) no-repeat left top; }
.tabcontent .content .main { position: relative; top: 0; left: 0; }
.tabcontent .content .main-flippy-ul { margin: -15px 0 30px 180px; list-style: disc; }
.tabcontent .content .num-ref-text { margin: 0 0 20px 30px; list-style: decimal; font-size: 9px; }
.tabcontent .content .null-ref-text { margin: 0 0 5px 30px; list-style: none; font-size: 9px; }
.tabcontent .content .pre-ext-links { padding: 0; }
.tabcontent .content .ext-links { padding: 0 0 180px 180px; list-style: disc; }
.tabcontent .content .ext-links li { padding: 0 0 8px 0; vertical-align: top; }
.tabcontent .content .ext-links a { line-height: 17px; }

.tabcontent .content ul.bullets {list-style:disc; padding:10px 0 0 20px;}
.tabcontent .content ul.bullets li {padding-bottom:5px; }
.tabcontent .content ol.numbers {list-style:decimal; padding:10px 0 0 25px;}
.tabcontent .content ol.numbers li {padding-bottom:5px; }

.tabcontent .content ul.icon-list { margin:20px -20px 40px -10px; }
.tabcontent .content ul.icon-list li { float:left; width:154px;}
.tabcontent .content ul.icon-list li p {margin:0;}
.tabcontent .content ul.icon-list li strong {font-size:14px; }

.tabcontent .content .reward-list { float: left; width: 145px; }
.tabcontent .content .reward-list p { margin: 0; }
.tabcontent .content .reward-list strong { font-size: 14px; }

.tabcontent .content .topic .feature .feature-desc { width:418px; }
.tabcontent .content .topic .feature .feature-desc p { margin-bottom:0; }
.tabcontent .content .feature { margin-bottom:20px; }
.tabcontent .content .feature .feature-icon { float:left; width:166px; }
.tabcontent .content .feature .feature-desc { float:left; width:595px; }
.tabcontent .content .feature .feature-desc p { padding:0; }
.tabcontent .content .feature .clear { clear:both; line-height:1px; }

/** header.css *********************************************/

body { font-family: arial, verdana, san-serif; font-size: 12px; text-align: center; margin: 0 0 20px 0; padding: 0; color: #3a3a3a; }
a { text-decoration: none; color: #2264ac; }
a:hover { text-decoration: underline; }
p { margin: 10px 0; }
.arrow { font-weight: bold; padding-right: 14px; background: url(/images/blue-arrow-bullet.png) right 3px no-repeat; }
* html .arrow { font-weight: bold; padding-right: 14px; background: url(/images/blue-arrow-bullet.gif) right 3px no-repeat; }
.italic { font-style: italic; }
img { border: none; }
sup { font-size: 8px; line-height: 4px; font-weight: normal; vertical-align: super; }
.png { behavior: url(/js/iepngfix.htc); }
#pg .button { display:inline-block; margin:10px 0; background: url(/images/buttons/button-fade-blue-sprite.gif) 0 0 no-repeat; padding-left:5px; height:32px;}
* html #pg .button  { display:inline; }
#pg .button:hover {text-decoration:none; cursor:pointer; }
#pg .button .bg { background: url(/images/buttons/button-fade-blue-sprite.gif) right 0 no-repeat; padding:10px 20px 11px 15px; display:inline-block; }
* html #pg .button .bg { display:inline; }
#pg .button .arrow { font-weight:normal; }
#pg .button.green { display:inline-block; margin:10px 0; font-weight: bold; background: url(/images/buttons/button-green-sprite.gif) 0 0 no-repeat; padding-left:10px; height:44px; color:#FFFFFE; font-size:15px;line-height:15px;}
* html #pg .button.green { display:inline; }
#pg .button.green, x:-moz-any-link { line-height: 44px; } /* FF2 fixes */
#pg .button.green, x:-moz-any-link, x:default { line-height: 15px; }
#pg .button.green:hover {text-decoration:underline;}
#pg .button.green .bg { background: url(/images/buttons/button-green-sprite.gif) right 0 no-repeat; padding:13px 25px 15px 15px; display:inline-block; }
* html #pg .button.green .bg { display:inline; }

#pg .isOn {display:block; }
.content-header .tagline {color:#8f8c8c; font-size:12px; font-weight:bold; right:50px; top:22px; position:absolute; z-index:5;}

#bg { width: 100%; background: url(/images/pg-bg.jpg) top center no-repeat #fff; text-align: center; }
#pg { width: 950px; position: relative; margin: 0 auto; text-align: left; }
#pg-top { position: relative; z-index: 1; }
#pg-top h1.logo { display: block; position: absolute; top: 24px; left: 0px; width: 156px; height: 38px; background: url(/images/logo-sprites.gif) no-repeat; text-indent: -5000px; margin: 0px; }
#pg-top h1.logo a {display:block; width: 156px; height: 38px;}
#pg-top .nav { padding: 53px 10px 0 197px; }
#pg-top .nav ul { overflow: hidden; width: 100%; list-style: none; margin: 0; padding: 0; }
#pg-top .nav ul li { float: left; margin: 0; padding: 0; background: url(/images/nav-left.png) top left no-repeat; margin: 0 3px 0 0; padding: 0 0 0 5px; }
#pg-top .nav ul li a { float: left; display: block; background: url(/images/nav-right.png) top right no-repeat; padding: 13px 23px 13px 18px; font-weight: bold; font-size: 12px; }

.home #pg-top .nav ul li.home,
.basic #pg-top .nav ul li.basic,
.plan #pg-top .nav ul li.plan,
.invest #pg-top .nav ul li.invest,
.support #pg-top .nav ul li.support { background-position: 0% -120px; }
.products #pg-top .nav ul li.products { background-position: 0% -120px; }

.home #pg-top .nav ul li.home a,
.basic #pg-top .nav ul li.basic a,
.plan #pg-top .nav ul li.plan a,
.invest #pg-top .nav ul li.invest a,
.support #pg-top .nav ul li.support a { background-position: 100% -120px; }
.products #pg-top .nav ul li.products a { background-position: 100% -120px; }

#pg-top .cart-nav { position: absolute; top: 19px; left: 209px; overflow: hidden; }
#pg-top .cart-nav ul { float: left; list-style: none; margin: 0; padding: 0; }
#pg-top .cart-nav ul li { float: left; margin: 0; padding: 0; background: url(/images/cart-sprites.gif) 0 -60px no-repeat; margin: 0; padding: 0 0 0 8px; }
#pg-top .cart-nav ul li.first { background: none; }    
#pg-top .cart-nav ul li a { float: left; display: block; background: url(/images/cart-sprites.gif) 0 5px no-repeat; padding: 2px 10px 2px 11px; font-weight: bold; font-size: 12px; }
#pg-top .cart-nav ul li.cart a,
#pg-top .cart-nav ul li.cart a:hover { background-position: 0 -36px; padding-left: 14px }
#pg-top .cart-nav ul li.on a { background-position: 0 -15px; }

#pg-top .search { position: absolute; top: 10px; right: 0; }
#pg-top .search input { border: solid 1px #c2ccd2; -moz-border-radius: 5px; -webkit-border-radius: 5px; color: #999999; padding: 4px; font-size: 11px; font-weight: bold; }
#pg-top .search .go { border: none; vertical-align: -0.7em; margin-left: 2px; padding: 0; border: none; }

.has-pointer { cursor: pointer; }
.boldit { font-weight: bold; }
.video-link { float: left; margin-left: 10px; }
.invisible { display: none; }

.qucken_signin {float:right; font-size:12px; color:#3a3a3a}
.qsignin {background:transparent url(/images/bullet-sprites.gif) no-repeat scroll right 1px !important; padding-right: 12px !important; font-size:12px; line-height:13px;}
/** template.css *********************************************/

#pg-content { position: relative; margin: 0; padding: 0; background: #fff; -moz-border-radius: 3px; -webkit-border-radius: 3px; background: url(/images/content-top.png) top left no-repeat #fff; }
#pg-content .crumbs { margin: 0 18px 0; padding: 18px 0; overflow: hidden; font-size: 11px; color: #878686; }
#pg-content .crumbs ul { list-style: none; margin: 0; padding: 0; }
#pg-content .crumbs ul li { float: left; margin: 0; padding: 0 0 5px 5px; }
#pg-content .crumbs ul li a { float: left; margin: 0; padding: 0 10px 0 0; background: url(/images/bullet-sprites.gif) right -30px no-repeat; }
#pg-content .tip {background: url(/images/bullet-sprites.gif) left -60px no-repeat; padding:5px 0 0 23px; height:23px; display:inline-block; }
* html #pg-content .tip { display:inline; }

#pg-content .fine-print {font-size:11px;}
#pg-content .fine-print a {font-weight:normal; }
#pg-content .content-header { position: relative; padding: 0 30px 30px; }
#pg-content .feature-head { width: 890px; padding: 0 0 20px 0; background: url(/images/learnmore/feature-background-deluxe.jpg) no-repeat left bottom;  overflow: visible; }
#pg-content .feature-head-product { float: left; margin: 15px 0 0 0; padding: 0 0 0 30px; width: 195px; }
* html #pg-content .carousel .feature-head-product { padding-left: 0; }
#pg-content .product-image-online { position: absolute; bottom: 30px; left: 30px; }
#pg-content .product-image-mobile { position: absolute; bottom: 45px; }
* html #pg-content .product-image-online { bottom: 29px; }
#pg-content .feature-head .heading { margin-bottom: 0; }
#pg-content .feature-head .heading h2, #pg-content .feature-head .heading h5 { padding: 5px 0 0 0; width: 375px; font-weight: normal; }
#pg-content .feature-head .heading h2.longer, #pg-content .feature-head .heading h5.longer { width: 350px; }
#pg-content .feature-head-solo { padding: 0 40px; }
#pg-content .feature-head-left { float: left; padding: 30px 20px 0 0; width: 390px; }
#pg-content .feature-head-left2 { float: left; padding: 30px 0 0 0; width: 395px; }
#pg-content .feature-head-double-width { float: left; padding: 30px 0 0 10px; width: 640px; }
#pg-content .feature-head .feature-head-double-width strong { color: #FFFFFF; font-weight: bold; }
#pg-content .feature-head-double-s1 { position: relative; float: left; width: 290px; height: 160px; }
#pg-content .feature-head-double-bg1 { position: absolute; top: 0; left: 0; width: 290px; height: 160px; background: url(/images/learnmore/double-step-left.png) no-repeat left top; }
#pg-content .feature-head-double-cont1 { position: absolute; top: 0; left: 0; width: 290px; height: 160px; }
#pg-content .step-one-floater { position: absolute; top: -10px; left: -10px; width: 33px; height: 34px; background: url(/images/learnmore/step-one-dot.png) no-repeat left top; }
#pg-content .feature-head-double-s2 { position: relative; float: left; width: 330px; height: 160px; }
#pg-content .feature-head-double-bg2 { position: absolute; top: 0; left: 0; width: 330px; height: 160px; background: url(/images/learnmore/double-step-right.png) no-repeat left top; }
#pg-content .feature-head-double-cont2 { position: absolute; top: 0; left: 0; width: 330px; height: 160px; }
#pg-content .feature-head-double-para1 { padding: 15px 0 0 30px; width: 230px; font-size: 14px; line-height: 17px; color: #FFFFFF; }
#pg-content .feature-head-double-para2 { padding: 10px 0 0 30px; width: 230px; font-size: 12px; line-height: 14px; color: #FFFFFF; }
#pg-content .step-two-floater { position: absolute; top: -10px; left: -10px; width: 33px; height: 34px; background: url(/images/learnmore/step-two-dot.png) no-repeat left top; }
#pg-content .feature-head-double-signup { position: absolute; top: 100px; left: 30px; }
#pg-content .feature-head-double-download { position: absolute; top: 100px; left: 30px; }
#pg-content .feature-head-double-appstore { position: absolute; top: 90px; left: 155px; }
#pg-content .feature-head ul { padding: 10px 0 0 0; margin: 0 0 0 30px; list-style: disc outside; }
#pg-content .feature-head li { padding: 3px 0; font-size: 14px; line-height: 16px; color: #3A3A3A; }
#pg-content .feature-head-left .mint li {font-size:13px;line-height:15px;}
#pg-content .feature-head ul.no-bullet { margin: 0; list-style: none; }
#pg-content .feature-head ul.no-bullet li { margin: 0; list-style: none; }
#pg-content .feature-head strong { font-weight: bold; color: #3A3A3A; }
#pg-content .feature-important { padding-bottom: 10px; font-size: 16px; line-height: 22px; font-weight: bold; }
#pg-content ul.feature-important-list { font-size: 14px; padding: 0; margin: 0 0 0 25px; }
#pg-content .feature-head-right { float: left; width: 250px; }
#pg-content .feature-head .arrow { margin: 0 0 0 12px; font-size: 12px; line-height: 13px; font-weight: bold; }
#pg-content .feature-green-callout { width: 250px; margin: 0 0 5px 0; padding: 32px 0 0 0; }

#pg-content .feature-quicken-online-block { width: 216px; height:155px; margin: 0 0 5px 0; padding: 32px 0 0 0; background:url(/images/hub/BMM-quicken-online-background-block.png) no-repeat top left;}
#pg-content .feature-quicken-premier-block { width: 216px; height:193px; margin: -40px 0 5px 0; padding: 32px 0 0 0; background:url(/images/hub/quicken-premier-content-box.png) no-repeat top left;}

#pg-content .feature-green-callout .gc-inner-form { position: absolute; top: 50px; color: #FFFFFF; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer strong,
#pg-content .feature-green-callout .gc-inner-form li,
#pg-content .feature-green-callout .gc-inner-form a { color: #FFFFFF; display: block; padding: 0 0 0 10px; line-height:11px; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer { top:30px; padding:15px 20px; width:180px; top:30px; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer h3 { font-size:18px; line-height: 23px; padding:13px 0 7px 0; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer h3 .price { font-weight:bold; font-size:32px;}
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight {background: url(/images/learnmore/green-callout-hilight-top.gif) no-repeat left top; padding-top:3px; width:184px;}
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight .btm {background: url(/images/learnmore/green-callout-hilight-btm.gif) no-repeat left top; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight ul {list-style-type: none; list-style-image: none; padding:5px 10px 10px 10px; *padding-bottom:0px; width: 165px; margin:0;}
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight li {padding:0; font-size:11px; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight li .price-label {*float: left; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight li .price-label.rpm {float: left; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight li .price {float:right; }

#pg-content .feature-green-callout .gc-m {width: 172px; height:125px; background: url(/images/learnmore/green-callout-background-m.png) repeat-y left top; }
#pg-content .feature-green-callout .gc-top { width: 250px; height: 5px; background: url(/images/learnmore/green-callout-top.png) no-repeat left top; }
#pg-content .feature-green-callout .gc-bgs { width: 220px; background: url(/images/learnmore/green-callout-background.png) repeat-y left top; }
#pg-content .feature-green-callout .gc-gra { padding: 10px 0; width: 220px; min-height: 119px; background: url(/images/learnmore/green-callout-gradient.png) no-repeat left top; }
#pg-content .feature-green-callout .gc-bot { width: 250px; height: 11px; background: url(/images/learnmore/green-callout-bottom.png) no-repeat left bottom; }

#pg-content .feature-head-right .subline {line-height:16px; margin:0;}
#pg-content .feature-callout-sphere { position: absolute; top: 0; right: 32px; width: 100px; height: 95px; background: url(/images/learnmore/callout-star.png) no-repeat left top; }

#pg-content .promo-sphere-deluxe {width: 117px; height: 118px; background: url(/images/discount/burst-deluxe.png) no-repeat left top; }
#pg-content .promo-sphere-premier {width: 117px; height: 118px; background: url(/images/discount/burst-premier.png) no-repeat left top; }
#pg-content .promo-sphere-hb {width: 117px; height: 118px; background: url(/images/discount/burst-HB.png) no-repeat left top; }
#pg-content .promo-sphere-rpm {width: 117px; height: 118px; background: url(/images/discount/burst-RPM.png) no-repeat left top;  }
#pg-content .promo-sphere-general {width: 117px; height: 118px; background: url(/images/discount/burst-willmaker-only.png) no-repeat left top;  }
#pg-content .promo-sphere-10-off {width: 120px; height: 120px; background: url(/images/discount/10off-large.png) no-repeat left top; }

#pg-content .content-header .new-in-2010-sphere { position: absolute; top: 150px; left: 30px; width: 142px; height: 142px; background: url(/images/new-in-2010.png) no-repeat left top; }
#pg-content .content-header .new-in-2010-sphere-sm { position: absolute; top: 130px; left: 20px; width: 121px; height: 121px; background: url(/images/new-in-2010-sm.png) no-repeat left top; }
#pg-content .content-header .new-in-2010-sphere-underlined-sm { position: absolute; top: 130px; left: 20px; width: 121px; height: 121px; background: url(/images/new-in-2010-underlined-sm.png) no-repeat left top; }
#pg-content .content-header .quicken-2010-testimonial { position: absolute; top: 4px; left: 540px; width: 362px; height: 325px; background: url(/images/hub/quicken-2010-testimonial-bubble-home.png) no-repeat left top; }
#pg-content .content-header ul#new-features-list { position: relative; float: none; list-style-type: none; width: 540px; margin: 6px 0px 0px 20px; padding: 0; }
#pg-content .content-header ul#new-features-list li { float: none; background: url('/images/round-bullet.gif') no-repeat 0 0.4em; padding: 0 0 0 14px; width: 400px; height: 40px; margin: 0px 0px 10px 10px; }

#pg-content .feature-online-sphere { top: -30px; right: -30px; }
#pg-content .feature-head .magnify { background:transparent url(/images/learnmore/icn-magnify.gif) no-repeat scroll right top; padding:1px 18px 1px 6px;  }
#pg-content .feature-head .feature-price { padding: 0 0 0 15px; font-size: 30px; font-weight: bold; color: #FFFFFF; }
#pg-content .feature-head .strikethrough {text-decoration:line-through;padding: 0 0 0 15px;font-size:16px;color: #fff}
#pg-content .feature-head .feature-ttl { padding: 10px 0 10px 15px; font-size: 18px; font-weight: bold; color: #2f5419; }
#pg-content .feature-head .feature-options { padding: 10px 0 0 15px; font-size: 12px; font-weight: bold; color: #FFFFFF; }
#pg-content .feature-head .feature-options label { font-weight: normal; }
#pg-content .feature-head .feature-buynow { margin: 10px 0 0 0; width: 95px; height: 28px; border: 0; background: url('/images/buttons/bbm-buy-now-sm.gif') no-repeat left top; cursor:pointer; }
#pg-content .feature-head .feature-buynow-white { margin: 10px 0 0 0; width: 118px; height: 36px; border: 0; background: url('/images/buttons/buy-now-btn-silver.png') no-repeat left top; cursor:pointer; }
#pg-content .feature-head .feature-preorder-white { margin: 10px 0 0 0; width: 118px; height: 36px; border: 0; background: url('/includes/exp/fy10-772-strengthen-add-to-cart-buttons/images/buttons/pre-order-now-sm-white.png') no-repeat left top; cursor:pointer; }
#pg-content .feature-head .feature-preorder { margin: 10px 0 0 0; width: 115px; height: 28px; border: 0; background: url(/images/buttons/pre-order-now-sm.jpg) no-repeat left top; cursor:pointer;}
#pg-content .feature-head .feature-learnmore { margin: 10px 0 0 0; width: 96px; height: 28px; border: 0; background: url(/images/buttons/learn-more-sm-grn.png) no-repeat left top; }
#pg-content .feature-head .feature-addcart { margin: 10px 0 0 0; width: 95px; height: 28px; border: 0; background: url(/images/learnmore/add-to-cart-button.png) no-repeat left top; cursor:pointer; }
#pg-content .feature-head .feature-startfree { margin: 20px 0 5px 0; width: 140px; height: 28px; border: 0; background: url(/images/learnmore/start-free-button.png) no-repeat left top; }
#pg-content .feature-head .feature-startfree-gray-short { margin: 20px 0 5px 0; width: 140px; height: 36px; border: 0; background: url(/images/learnmore/start-free-button-gray-short.png) no-repeat left top; }
#pg-content .feature-head .feature-one-month-free-gray-long { margin: 20px 0 5px 0; width: 186px; height: 32px; border: 0; background: url(/images/learnmore/one-month-free-gray-long.png) no-repeat left top; }
#pg-content .feature-head .feature-signin { margin: 20px 0 5px 0; width: 140px; height: 28px; border: 0; background: url(/images/learnmore/sign-in-button.png) no-repeat left top; }
#pg-content .feature-white-callout { width: 250px; height: 71px; margin: 10px 0 10px 0; background: url(/images/learnmore/white-callout-background.png) no-repeat left top; }
#pg-content .feature-white-callout-m { width: 169px; height: 73px; margin: 10px 0 10px 0; background: url(/images/learnmore/white-callout-background-m.png) no-repeat left top; }
#pg-content .feature-white-callout-xl { width: 250px; height:75px; margin: 10px 0 10px 0; background: url(/images/learnmore/white-callout-background-xl.png) no-repeat left top; }
#pg-content .feature-white-callout-m p { padding:9px 5px 0 13px; line-height:14px; font-size:11px; margin:0;}
#pg-content .feature-head .card-side-copy { float: left; padding: 9px 10px 0 13px; width:185px; font-size: 11px; line-height: 13px; }
#pg-content .feature-head .card-side-copy a { font-size: 11px; line-height: 23px; font-weight: bold; }
#pg-content .feature-head .card-inset { float: left; margin: 0 5px 0 0; width: 38px; height: 26px; background: url(/images/learnmore/visa-card-mini.png) no-repeat left top; }
#pg-content .feature-head .subtext { margin: 17px 0 0 12px; font-size: 10px; }
#pg-content .feature-head h6 { padding: 0 0 6px 10px; font-size:18px; color:#2f5419; line-height:20px; font-weight:bold; }
#pg-content .clear { clear: both; }
#pg-content .clear-left { clear: left; }
#pg-content .clear-right { clear: right; }
#pg-content .push-header-links { position: relative; bottom: 30px; left: 645px; margin-bottom: -10px; width: 245px; text-align: right; }
#pg-content .push-header-links .arrow { margin: 0; font-size: 12px; line-height: 15px; font-weight: normal; }

#pg-content .content-front-bottom { margin: 0 auto; padding: 0 0 15px 0; width: 880px; }
#pg-content .content-front-bottom .fb-column-left { float: left; margin-right: 40px; width: 420px; }
#pg-content .content-front-bottom .fb-column-right { float: left; width: 420px; }
#pg-content .content-front-bottom h2 { padding: 14px 20px 0 20px; width: 380px; height: 28px; font-size: 15px; font-weight: bold; color: #232323; background: url(/images/home/ltblue-main-body-header.gif) no-repeat left top; }
#pg-content .content-front-bottom h3 { font-size: 15px; line-height: 17px; font-weight: bold; color: #0C549C; }
#pg-content .content-front-bottom h3.smaller { font-size: 13px; }
#pg-content .content-front-bottom p { color: #333333; font-size: 12px; line-height: 20px; margin-top:4px; }

#pg-content .content-front-bottom .inset-para { padding: 15px 20px; font-size: 12px; line-height: 20px; }
#pg-content .content-front-bottom .white-box { position: relative; overflow: hidden; margin-bottom: 15px; width: 420px; }
#pg-content .content-front-bottom .white-box-top { width: 420px; height: 6px; background: url(/images/home/white-box-top.gif) no-repeat left top; }
#pg-content .content-front-bottom .white-box-body { padding: 5px 15px; width: 390px; background: url(/images/home/white-box-bg.gif) repeat-y left top; }
#pg-content .content-front-bottom .white-box-body h3 { color:#000; margin-bottom:10px; }
#pg-content .content-front-bottom .white-box-body .offer-links { float: left; width: 220px; }
#pg-content .content-front-bottom .white-box-body .offer-links p { margin: 0px; padding-top: 4px; padding-bottom: 10px; }
#pg-content .content-front-bottom .white-box-body .offer-links p a { font-weight: bold; }
#pg-content .content-front-bottom .white-box-body .retailer-logo-links { float: left; width: 120px; padding-left: 40px; }
/*#pg-content .content-front-bottom .white-box-body .retailer-logo-links .retailer-logo-container { height: 40px; margin:0px; padding-top: 4px; padding-bottom: 10px; }*/
#pg-content .content-front-bottom .white-box-body .retailer-logo-links img { height: 47px; margin:0px; padding-top: 0px; padding-bottom: 7px; }
#pg-content .content-front-bottom .white-box-bottom { width: 420px; height: 8px; background: url(/images/home/white-box-bottom.gif) no-repeat left top; }
#pg-content .content-front-bottom .floating-quotes { position: absolute; top: 20px; right: 30px; width: 88px; height: 50px;  }
#pg-content .content-front-bottom .floating-iphone { position: absolute; top: 5px; right: 50px; width: 50px; height: 101px; }
#pg-content .content-front-bottom .floating-card { position: absolute; top: 15px; right: 25px; width: 104px; height: 69px;  }
#pg-content .content-front-bottom .centered-icon-float { float: left; width: 120px; padding: 0 15px; margin-bottom: 8px; text-align: center; }
#pg-content .content-front-bottom .centered-icon-float a { font-weight: bold; color: #4E4E4E; }
#pg-content .content-front-bottom .right-col-cap { width: 420px; height: 10px; background: url(/images/home/right-column-end.gif) no-repeat center top; }
#pg-content .content-front-bottom .right-col-post-link { width: 410px; padding-right: 10px; margin-bottom: 30px; font-size: 11px; text-align: right; }
#pg-content .content-front-bottom .right-col-post-link a { line-height: 15px; }
#pg-content .content-front-bottom .rc-gap { height: 20px; }
#pg-content .content-front-bottom .no-padding { margin-bottom: 0; }
#pg-content .content-front-bottom .inline-to-icon { vertical-align: top; }
#pg-content .content-front-bottom-cap { width: 950px; height: 20px; background: url(/images/footer-fade.gif) no-repeat left top; }
#pg-content .content-front-bottom-cap-dkblue { width: 950px; height: 8px; background: url(/images/learn-more-top-dk-blue.png) no-repeat left top; }
#pg-content .content-front-bottom .fb-column-left .rounded-box .middle {padding:10px 20px; }
#pg-content .content-front-bottom .fb-column-right .rounded-box .middle {padding:5px 15px; }
#pg-content .content-front-bottom .rounded-box h2 { font-size:17px; padding:0;background:none; width:auto;height:auto; line-height:120%; margin-bottom:13px; color:#0c549c;}
#pg-content .content-front-bottom .rounded-box p { line-height:140%; }
#pg-content .content-front-bottom .rounded-box a.arrow { line-height:16px; }
#pg-content .content-front-bottom .rounded-box a.after-btn { position:absolute; margin: 5px 0 0 15px; }
/* for staggared discount */ #pg-content .content-front-bottom .rounded-box .box-bg { position:absolute; margin: -20px 0 0 282px;}
/* for non-discount */ #pg-content .content-front-bottom .rounded-box .box-bg { position:absolute; margin: -30px 0 0 238px;}

#pg-content .content-front-bottom .rounded-box.mint .middle { background: url(/images/home/logo-mint-small.gif) no-repeat 270px 25px; }
#pg-content .content-front-bottom .rounded-box.mint h3 { padding-bottom:5px; }

#pg-content .content-inner { position: relative; margin: 0 36px; padding: 0 30px 30px; background: url(/images/content-bg.gif) top left repeat-x #bbdff4; }
#pg-content .content-inner-2 { position: relative; margin: 0 36px; padding: 0 30px 30px; background: url(/images/content-bg-2.gif) top left repeat-x #bbdff4; }
#pg-content .content-inner .search-support { margin: 0 0 34px 0; padding: 20px; border: solid 1px #c3e0f2; background: url(/images/search-support-bg.gif) top left repeat-x #edf6fb; -moz-border-radius: 5px; -webkit-border-radius: 5px; }
#pg-content .content-inner .col-wrapper { overflow: hidden; width: 100%; }
#pg-content .content-inner .col-wrapper .col-left { position: relative; float: left; width: 560px; padding-top: 30px; }
#pg-content .content-inner .col-wrapper .col-right { position: relative; float: right; width: 213px; padding-top: 30px; }
.col-right .rounded-box { width: 210px; margin-bottom: 30px; } 
#pg-content .content-inner .content-left { float:left; padding-bottom:30px; }
#pg-content .content-inner .content-right { float:right; }

#pg-content .inner-alt { padding: 0 0 0 0; margin: 0 30px; }
#content-inner-nav { float: left; width: 182px; }
#content-inner-body { float: left; width: 610px; }
#content-inner-nav { position: relative; left: 1px; z-index: 50; }
#content-inner-nav ul { width: 182px; overflow: hidden; }
#content-inner-nav li { padding: 0 0 0 12px; width: 170px; height: 44px; line-height: 37px; font-weight: bold; background: url(/images/learnmore/section-tab-normal.gif) no-repeat left top; }
#content-inner-nav li.isOn, #content-inner-nav li.active-nav { padding: 0 0 0 12px; width: 170px; height: 44px; line-height: 37px; font-weight: bold; background: url(/images/learnmore/section-tab-active.gif) no-repeat left top; }
#content-inner-nav a { display: block; }
#content-inner-nav .multiline { padding-top: 4px; line-height: 14px; }

.topic ul, .topic ol { margin: 8px 0 20px 20px; }
.topic li {line-height: 1.2;padding-bottom: 4px;} /* list-style: outside disc; -- on LI is invalid*/ 

.flippy-panel-wrapper { width: 3640px; height: 1187px; overflow: hidden; }
.content-inner-flippy { padding: 0 0 20px 0; width: 708px; overflow: hidden; position: relative; }
.flippy-panel { position: absolute; left: 0; top: 0; padding: 30px 30px 0 30px; width: 648px; min-height: 400px; font-size: 12px; line-height: 17px; color: #333333; background-color: #FFFFFF; }
.float-clear { display: block;min-width: 1px; }
.float-clear:after { content: "."; display: block; height: 0; visibility: hidden; clear: both; }
.flippy-end-cap { margin: 0; width: 708px; height: 4px; background: url(/images/learnmore/flippy-end-cap.png) no-repeat left top;}

.cross-promotion-unit, .more-business-solutions, .mac-specific-footer { float: left; padding: 0 18px 19px 7px; width: 192px; font-size: 12px; line-height: 18px; color: #333333; }
.cross-promotion-zone3 { float: right; }
.cross-promotion-unit .arrow { margin-top: 3px; margin-left:2px; line-height: 13px; display:inline-block; }
.cross-promotion-unit li { background: url(/images/bullet-sprites.gif) left -121px no-repeat; padding-left:10px; }
.cross-promotion-unit li a { font-weight:normal; }
.cross-promotion-title, .more-business-title, .mac-specific-footer-title { margin: 0 0 5px 0; font-size: 15px; font-weight: bold; color: #0C549C; }
.cross-promotion-pimg { float: left; margin: 0 10px 0 0; }
.more-business-solutions { width: 425px; }
.more-business-solutions a { font-weight: bold; }
.more-business-solutions .more-business-title { margin-bottom: 23px; }
.mac-specific-footer { padding-left: 185px; width: 600px; }

.heading { margin-bottom: 45px; }
.heading h1 { color: #306a0f; font-size: 28px; font-weight: bold; }
.heading h1 span { font-weight: normal; }
.heading h2, .heading h5 { font-size: 21px; color: #55aa00; }

.green-text { color:#598840; font-weight:bold;}

.kiplinger { color: #777; font-size: 14px; font-style: italic; }
.kiplinger img { vertical-align: -0.3em; }

#pg-content .col-left p { margin: 20px 0; font-size: 14px; line-height: 20px; }
#pg-content strong {font-weight:bold; }
#pg-content .col-left b { color: #0c549c; }
#pg-content .print-share { background: url(/images/print-share-sprites.gif) 0 -80px repeat-x; padding: 3px 10px; margin: 20px 0 10px; overflow: hidden; width: 155px; font-size: 12px; border: solid 1px #a8d4ed; -moz-border-radius: 3px; -webkit-border-radius: 3px; }
#pg-content .print-share a { display: block; float: left; width: 25px; padding-left: 30px; line-height: 24px;  }
#pg-content .print-share a.print { background: url(/images/print-share-sprites.gif) 0 0 no-repeat; margin-right: 25px; }
#pg-content .print-share a.share { background: url(/images/print-share-sprites.gif) 0 -40px no-repeat; margin-right: 0; }

#pg-content .content-box { width: 300px; margin: 20px 0; }

.stripe td,.stripe th {background: #f5f5f5}
#sysreqs table {width: 465px;margin: 0 0 50px 0;  border-top:  1px solid #cdcdcd; border-left: 1px solid #cdcdcd;font-size: 12px; float:left}
#sysreqs td,#sysreqs th {padding: 7px;border-right: 1px solid #cdcdcd; border-bottom: 1px solid #cdcdcd; vertical-align: middle; }
#sysreqs th {width:182px }
#sysreqs img {float:left; margin: 0 20px 0 15px; display:inline} 
#sysreqs h3 {margin: 0 0 20px 118px;color: #4e4e4e}

#pg-content .billboard .feature-head { background: none; }
#pg-content .billboard .feature-head-right { margin-right:10px;float: right; width: 250px;}
#pg-content .billboard .feature-head-left { padding-right:0; }
.cart-multiple input { margin: 2px 0 6px 3px; }
* html .cart-multiple input { margin: 0; }

.reg-page-content { padding: 30px; height: 400px; }
.reg-page-content h1 { margin: 0 0 10px 0; font-size: 22px; font-weight: bold; }
.reg-page-content h2 { margin: 0 0 30px 0; font-size: 16px; font-weight: bold; }
.reg-page-content p { }

#pg-content a.truste { position: relative; display: block; margin-right: 50px; width: 116px; height: 31px; float: left; background: url(/images/logo-sprites.gif) 0 -200px no-repeat;  text-indent: -5000px; }
#pg-content a.verisign { position: relative; display: block; margin: -12px 25px 0 0; width: 93px; height: 52px; float: left; background: url(/images/logo-sprites.gif) 0 -300px no-repeat;  text-indent: -5000px; }

#pg-content .retailer-box { float: left; width: 185px; }
#pg-content .retailer-box p { text-align: center; }
#pg-content .retailer-box .retailer-logo-staples { width: 170px; height: 80px; background: url(/images/home/retailer-logos-sprite.jpg) no-repeat left 0; }
#pg-content .retailer-box .retailer-logo-bestbuy { width: 170px; height: 80px; background: url(/images/home/retailer-logos-sprite.jpg) no-repeat 10px -80px; }
#pg-content .retailer-box .retailer-logo-officemax { width: 174px; height: 80px; background: url(/images/home/officemax-logo.png) no-repeat; position: relative; top: 25px; }
#pg-content .retailer-box .retailer-logo-officedepot { width: 174px; height: 80px; background: url(/images/home/office-depot-logo.png) no-repeat; position: relative; left: 10px; }

#pg-content .content-inner { position: relative; }
#pg-content .content-inner .quotebox { position: absolute; left: 0; top: 300px; width: 174px; }
#pg-content .content-inner .quotebox .quotebox-top { width: 174px; height: 14px; background: url(/images/learnmore/green-blurb-top.jpg) no-repeat left top; }
#pg-content .content-inner .quotebox .quotebox-body { padding: 0 15px; width: 144px; background-color: #DAF3BF; color: #2A5511; font: 15px Georgia, Times New Roman, Times, serif; font-style: italic; text-align: center; }
#pg-content .content-inner .quotebox .quotebox-bottom { width: 174px; height: 31px; background: url(/images/learnmore/green-blurb-bot.jpg) no-repeat left top; }
#pg-content .content-inner .quotebox .quotebox-byline { padding-left: 20px; color: #40791F; }

#pg-content .heading h1 sup { font-size:15px; vertical-align:sup; }

#pg-content .two-col .heading {margin:40px 0 25px 0; }
#pg-content .two-col .heading h1 {margin:0 0 10px 0; line-height:120%;}
#pg-content .two-col .content-right .heading { margin-bottom:15px;}
#pg-content .two-col .content-right .heading h4 { line-height:18px;}
#pg-content .two-col .content-right .heading p {line-height:18px; margin:5px 0 0 0;}
#pg-content .two-col h3 { font-size:16px; font-weight:bold; margin:20px 0 0 0;}
#pg-content .two-col .content-left{ width:555px;}
#pg-content .two-col .content-left p {line-height:20px;font-size:14px;}

#pg-content .two-col .content-right{ width:217px;}
#pg-content .two-col .content-right h4 { color:#0c549c; font-size:15px;font-weight:bold;}
#pg-content .two-col .content-right p { line-height:120%;}
#pg-content .two-col .content-right .rounded-box { width:226px; }
#pg-content .two-col .content-right .rounded-box .title { font-size:12px;line-height:120%;}
#pg-content .two-col .content-right .cross-promotion-title {color:#333333; }

#pg-content .rounded-box a.after-btn { position:absolute; margin: 5px 0 0 13px; padding-top:2px; }
#pg-content .two-col .strikethrough { text-decoration:line-through; display:inline-block; float:left;}
#pg-content .two-col .feature-price { font-size:14px; display:inline-block; padding-left:5px; }

/* AGENT LOGOUT LINK */
#agent-logout-holder { float: left; margin: 1px 10px 0 0; width: 63px; }
#agent-logout-holder a { color: #A54903; font-weight: bold; }
#agent-logout-holder a:hover { text-decoration: none; color: #B75B15; }

/* White buttons on green callouts, sitewide */


#pg-content .feature-head .feature-addcart-white-pulse-promo { margin: 2px 0px 0px 0px; width: 103px; height: 36px; border: 0; background: url('/images/buttons/add-to-cart-button-white.png') no-repeat left top; cursor:pointer; }
#pg-content .feature-head .feature-addcart-white { margin: 10px 0 0 0; width: 103px; height: 36px; border: 0; background: url('/images/buttons/add-to-cart-button-white.png') no-repeat left top; cursor:pointer; }
#pg-content .feature-head .feature-shoponline-white { margin: 10px 0 0 0; width: 159px; height: 32px; border: 0; background: url('/images/buttons/shop-online-btn-silver.png') no-repeat left top; cursor:pointer; margin-top:40px;}

/* Stripped out of Index Page */
.content-header .tagline { text-align:right; font-weight:none;}
.content-header .tagline h1 { color:#8F8C8C; font-size:12px; font-weight:bold; z-index:5; display:block; margin-bottom:10px;}

#pg .button.green .bg,
.button.green .bg { display:inline-block; padding:13px 30px 16px 20px; }

.billboard .topic p { margin:2px 0 12px 0; }

.rel 
{
	position: relative;
	z-index: inherit;
	zoom: 1; /* For IE6 */
	width: 190px;
}

.pod {display: block}
.pod-hover {display:none}

.hover .pod-hover {display:block}
.hover .pod {display: none}

#zone-2 {margin-left:33px}
#zone-2-pods {_zoom:1; min-width: 1px; margin: 14px 0 33px 0}
#zone-2-pods:after {content: "."; height: 0; display: block; clear:left;visibility:hidden}
.pod-deluxe, .pod-premier, .pod-homebiz, .pod-rental {width: 222px; float: left;}
.inner {background: url(/images/home/pod-body.jpg) 0 44px no-repeat;position:relative}
.pod, .pod-hover { width: 222px;height: 149px; }
.pod {padding-left:18px; width:204px; _padding-top: 6px ;*padding-top:6px}
.pod-hover {padding-left: 12px;width:210px;_padding-top: 10px;*padding-top:6px}
#zone-2 h2 {font-weight: bold;font-size:21px;color: #55aa00; margin-bottom: 5px;}
#zone-2 .helpMeChoose {font-size: 14px; }
.pod img {float:left;margin-right: 12px;  _display: inline}
.pod p {font-size: 13px; color: #3a3a3a;line-height: 18px; font-weight:bold;padding: 0 28px 0 5px;}
.pod-hover p {font-size: 13px; font-weight: bold; color: #3a3a3a; margin: 10px 0 0 5px}
.pod-hover ul {font-size:12px; list-style: disc outside; margin:10px 28px 6px 23px;line-height: 1.3; }
.pod-hover li {margin-bottom: 5px}
.inner h3 {line-height: 44px; height: 44px; color:#fff; font-size:16px; font-weight:bold; padding-left: 16px;background-repeat: no-repeat;background-position: 0 -3px}

.pod-bottom {background: url(/images/home/pod-bottom.jpg) 0 0 no-repeat; height: 12px; width: 222px; line-height:1px; font-size:1px}
.pod-deluxe h3 {background-image: url(/images/home/pod-deluxe-top.jpg)}
.pod-premier h3 {background-image: url(/images/home/pod-premier-top.jpg)}
.pod-homebiz h3 {background-image: url(/images/home/pod-homebiz-top.jpg)}
.pod-rental h3 {background-image: url(/images/home/pod-rental-top.jpg)}
.pod-learn-more {display: block; position: absolute; right:8px; bottom: 36px;_bottom: 20px;padding-right: 20px; height: 13px;line-height: 1.4}

.pod-deluxe .hover {background: url(/images/home/pod-deluxe-body-hover.jpg) 0 0 repeat-y}
 .pod-deluxe .hover .pod-bottom {background-image: url(/images/home/pod-deluxe-btm-hover.jpg)}

.pod-premier .hover {background: url(/images/home/pod-premier-body-hover.jpg) 0 0 repeat-y}
.pod-premier .hover  .pod-bottom {background-image: url(/images/home/pod-premier-btm-hover.jpg)}

.pod-homebiz .hover {background: url(/images/home/pod-homebiz-body-hover.jpg) 0 0 repeat-y}
.pod-homebiz .hover .pod-bottom {background-image: url(/images/home/pod-homebiz-btm-hover.jpg)}

.pod-rental .hover {background: url(/images/home/pod-rental-body-hover.jpg) 0 0 repeat-y}
.pod-rental .hover .pod-bottom {background-image: url(/images/home/pod-rental-btm-hover.jpg)}

/* BACK TEST STYLES */
#cta-offer { width:175px; }
#cta-offer p {
	font-size: 11px;
	font-weight: bold;
	color: #123700;
	padding: 0 0 5px 11px;
}
.free-shipping-lbl {
	font-size: 11px;
	padding:0px 5px 15px;
	font-weight: normal;
	}
#pg-content #cta-offer ul {
	margin-bottom: 0px;
	padding-top: 0px;
}
#pg-content #cta-offer li {
	display: list-item ;
	padding: 0px 0px 0px 0px ;
	margin-bottom:10px;
}
#cta-offer ul li a {
	font-size: 11px;
	color: #ffffff;
	text-decoration: underline;
	padding-left: 0px !important;
}
#cta-offer .bonus-value {
	font-style: italic;
	font-size: 10px;
	margin-left: 0px;
	font-weight: normal;
}
.bonus-value {
	font-style: italic;
}
.free-shipping-lbl {
	font-size: 11px;
	padding:0px 5px 0px !important;
	font-weight: normal;
	margin:5px 0 0 !important;
}

/* New User Promo */
.promo-newuser { background:url(/images/bg_quicken_newuser.png) 0 0 no-repeat; padding:25px 30px 0 30px;height:85px; width:340px;}
#pg-content .feature-head .heading .promo-newuser a { margin:0;}
#pg-content .feature-head .heading .promo-newuser h2,
#pg-content .promo-newuser h2 { background:none; padding:0; height:22px; color:#232323; font-size:15px; font-weight:bold; margin:0; width:auto;}

/* Quicken TSM LPs */
.bold { font-weight: bold; }
.qcc-tsm .breadcrumb-spacer { height:20px; }
.qcc-tsm .offer-limit { width:60px; font-weight:bold; padding-left:0px; }
.qcc-tsm .feature-head { _padding-bottom: 0px !important; }
.qcc-tsm .feature-head .clear { _height: 0px !important; _line-height: 0px !important; }
.qcc-tsm .feature-head-product { _height: 330px !important; _margin-top: 0px !important; _margin-bottom: -5px !important; }
.qcc-tsm .feature-head-product img { _margin-top: 20px !important; _margin-bottom: 0px !important; }
.qcc-tsm .feature-head-left { _width: 320px !important; }
.qcc-tsm .feature-head-left .heading { padding-top:16px; _padding-top: 14px; padding-left:76px; _padding-left: 14px !important; }
.qcc-tsm .feature-head-left .heading.default { padding-top:16px; padding-left:0px; }
.qcc-tsm .feature-head-left .heading.default h1 { font-size: 26px; }
.qcc-tsm #chase-cc-tn { position:absolute; z-index:5; top:-24px; right:16px; _right:36px; }
.fs-big-darkgreen { font-size:21px; font-weight:bold; color:#306a0f; }
.gray { color: #686868; }
.qcc-tsm #pg-content .feature-head-product { margin-top:24px;}
.qcc-tsm .hilight ul.btm li { padding: 4px 0px !important; }
.qcc-tsm .white-horizontal-line { line-height: 1px; font-size:10px; background-color:#9bb58c; height:1px; }
.qcc-tsm .hr-spacing { line-height: 1px; font-size:1px; height:1px; }
.qcc-tsm #yellow-swoosh-container { z-index:5; float:right; margin-right:-40px; margin-top:8px; }
.qcc-tsm #yellow-swoosh-container.deluxe-swoosh { z-index:5; float:right; margin-right:-37px; _margin-right: -32px; margin-top:10px; _margin-top: 8px; }
#pg-content .feature-green-callout .gc-inner-form.ltoffer h3{
    padding: 15px 10px 0 0px;
    top: 30px;
    width: 190px;
    font-weight: bold;
    font-size: 16px;
	line-height: 1.2em;
    padding-bottom: 10px;
}
#pg-content .feature-green-callout.rpm {
	margin-bottom: 0px;	
}
.rpm .price.2liner {
	padding-top: 1em; border: 1px solid red;
}
.qcc-tsm #pg-content .feature-green-callout .gc-inner-form.ltoffer .hilight ul {
	font-weight: bold;
}
/** carousel.css *********************************************/

.carousel {	}
.carousel .billboard 				{ height:313px; background: url(/images/hub/car-bg.jpg) no-repeat scroll left bottom; width: 890px; padding: 0 0 20px; position:relative; overflow:hidden;}
.carousel .billboard div 			{ position:absolute; top:1000px; font-size:15px; background-color:transparent }
.carousel .billboard div div		{ display:block; position:static; top:0; font-size:inherit; }
.carousel .billboard div.isOn		{ position:absolute;}
.carousel .billboard p 				{ color:#55aa00; font-size:21px; line-height:28px; margin-bottom:5px; }
.carousel .billboard .float 		{ position: absolute; top:0;}
.carousel .billboard .float.left 	{ left:0;}
.carousel .billboard .float.right 	{ right:0;}
.carousel .billboard h1, .carousel .billboard h4 			{ color:#306a0f; font-size:44px; font-weight:bold;width:421px; }
.carousel .billboard .button 		{ float:left; }
#pg .button.green 					{ margin-bottom:0; }
.carousel .billboard .arrow 		{ margin:25px 0 0 20px; position:absolute; }
.carousel .billboard .sub 			{ font-size:12px; color:#000; margin-left:10px; }
#pg-content .billboard strong 		{ color:#55aa00; font-weight:bold; }

.carousel .menu 					{ z-index:1; height:104px; width:810px; margin:-104px 0 0 40px; position:absolute; overflow:hidden; }
.carousel .menu img 				{ float:left; padding:0 10px 10px 5px; }
.carousel .menu p 					{ line-height:17px; margin:3px 0 0 0; }
.carousel .bg-menu 					{ display:none; z-index:0; position:absolute; margin:-130px 0 0 317px;}
.carousel ul 						{ width:10000px; list-style:none; position:absolute; }
.carousel .hub ul 					{ width:auto; list-style:none; position:relative; }

.carousel ul li 					{ padding:10px 5px 10px 15px; width:237px; height:73px; float:left; margin:0 16px 0 0; background-color:transparent; }
.carousel .hub ul li 				{ width:auto; height:auto; float:none; margin:0 0 0 0; padding:0 0 0 0; }

.carousel ul li.isOn 				{ cursor:default;}
.carousel ul li h3 					{ color:#0c549c; font-weight:bold; }
#pg-content .menu strong 			{ color:#3a3a3a; font-weight:bold; }

.carousel .control 					{ display:block; visibility:hidden; margin:0 20px 0 0; width:890px; height:115px; z-index:0; }
.carousel .control a 				{ width:40px; height:110px; }
.carousel .control a span 			{ display:none; }
.carousel .control a.prev 			{ float:left; background:url(/images/hub/carousel/car-previous.gif) left 40px no-repeat; }
.carousel .control a.next 			{ float:right; background:url(/images/hub/carousel/car-next.gif) left 40px no-repeat}
.carousel .control a.prev:hover 	{ background:url(/images/hub/carousel/car-previous-on.gif) left 40px no-repeat; }
.carousel .control a.next:hover 	{ background:url(/images/hub/carousel/car-next-on.gif) left 40px no-repeat}

.carousel .billboard .topic.hubs h1, .carousel .billboard .topic.hubs h4 				{ font-size:28px; padding:18px 0 13px 0;}
.carousel .billboard .topic.hubs p 					{ text-align:right; margin:0 20px 0 0; }
.carousel .billboard .topic.hubs p span 			{ width:200px; text-align:right; }
.carousel .billboard .topic.hubs .button 			{float:none; margin:7px 0;}
.carousel .billboard .topic.hubs .button span.bg 	{width:190px; text-align:center;}

.carousel .billboard .topic.hubs p, x:-moz-any-link { margin-bottom: 10px; } /* FF2 fixes */
.carousel .billboard .topic.hubs p, x:-moz-any-link, x:default { margin-bottom: 0; }
.carousel .billboard .topic.hubs .button, x:-moz-any-link { padding: 13px 0 13px 10px; }
.carousel .billboard .topic.hubs .button, x:-moz-any-link, x:default { padding: 0 0 0 10px; }


/** rounded-box.css *********************************************/

/** default rounded-box is white, no borders or bg fade **/
.rounded-box .top { overflow: auto; width: 100%; }
.rounded-box .top .left,
.rounded-box .top .right { position: relative; float: left; width: 50%; height: 5px; line-height: 0px; font-size: 0; }
.rounded-box .top .left { background: url(/images/rounded-box-sprites.png) 0 0 no-repeat; }
.rounded-box .top .right { background: url(/images/rounded-box-sprites.png) right 0 no-repeat; }
.rounded-box .middle { background: #fff; padding: 16px; font-size: 12px;  }
.rounded-box .middle .title { font-size: 15px; font-weight: bold; }
.rounded-box .middle a.title { display: block; font-size: 15px; font-weight: bold; }
.rounded-box .middle a.product-title { position: relative; display: block; font-size: 15px; font-weight: bold; padding: 0 0 30px 65px; background: url(/images/product-title-underline.png) bottom center no-repeat; }
.rounded-box .middle a.product-title .product-box { display: block; position: absolute; width: 54px; height: 100px; top: -50px; left: 0px; background: url(/images/product-box-sm-sprites.png) no-repeat; }
.rounded-box .middle a.product-title .product-box.basic { background-position: 0 0; }
.rounded-box .middle a.product-title .product-box.deluxe { background-position: 0 -120px; }
.rounded-box .middle a.product-title .product-box.premier { background-position: 0 -240px; }
.rounded-box .middle ul { list-style: none; margin: 10px 3px; }
.rounded-box .middle ul li { padding: 2px 0 3px 8px; line-height: 13px; background: url(/images/bullet-sprites.gif) 0 -120px no-repeat; list-style: none; }
.rounded-box .bottom { overflow: hidden; width: 100%; }
.rounded-box .bottom div { position: relative; float: left; width: 50%; height: 9px; line-height: 0px; font-size: 0; }
.rounded-box .bottom .left { background: url(/images/rounded-box-sprites.png) 0 -16px no-repeat; }
.rounded-box .bottom .right { background: url(/images/rounded-box-sprites.png) right -16px no-repeat; }

/** blue-border rounded-box **/
.rounded-box.blue-border .top .left { background-position: 0 -25px; }
.rounded-box.blue-border .top .right { background-position: right -25px; }
.rounded-box.blue-border .middle { background: #fff; border-left: solid 1px #c3dff1; border-right: solid 1px #c3dff1; }
.rounded-box.blue-border .bottom .left { background-position: 0 -41px; }
.rounded-box.blue-border .bottom .right { background-position: right -41px; }

/** fade-bg & blue-border rounded-box **/
.rounded-box.faded-bg .top .left { background-position: 0 -50px; }
.rounded-box.faded-bg .top .right { background-position: right -50px; }
.rounded-box.faded-bg .middle { background: url(/images/rounded-box-faded-bg.gif) top left repeat-x #edf5fa; border-left: solid 1px #c3dff1; border-right: solid 1px #c3dff1; }
.rounded-box.faded-bg .bottom .left { background-position: 0 -66px; }
.rounded-box.faded-bg .bottom .right { background-position: right -66px; }

/** no box around content rounded-box **/
.rounded-box.hidden .middle { background: none; }

/** corners by white mask **/
.rounded-box-mask { position:relative; }
.rounded-box-mask .tl { position: absolute; top: 0; left: 0; width: 4px; height: 4px; background: url(/images/rounded-box-mask.png) no-repeat left top;}
.rounded-box-mask .tr { position: absolute; top: 0; right: 0; width: 4px; height: 4px; background: url(/images/rounded-box-mask.png) no-repeat right top; }
.rounded-box-mask .bl { position: absolute; bottom: 0; left: 0; width: 4px; height: 4px; background: url(/images/rounded-box-mask.png) no-repeat left bottom; }
.rounded-box-mask .br { position: absolute; bottom: 0; right: 0; width: 4px; height: 4px; background: url(/images/rounded-box-mask.png) no-repeat right bottom; }
/** thickbox.css *********************************************/
/* ----------------------------------------------------------------------------------------------------------------*/
/* ---------->>> global settings needed for thickbox <<<-----------------------------------------------------------*/
/* ----------------------------------------------------------------------------------------------------------------*/
*{padding: 0; margin: 0;}

/* ----------------------------------------------------------------------------------------------------------------*/
/* ---------->>> thickbox specific link and font settings <<<------------------------------------------------------*/
/* ----------------------------------------------------------------------------------------------------------------*/
#TB_window {
	font: 12px Arial, Helvetica, sans-serif;
	color: #333333;
}

#TB_secondLine {
	font: 10px Arial, Helvetica, sans-serif;
	color:#666666;
}

#TB_window a:link {color: #666666;}
#TB_window a:visited {color: #666666;}
#TB_window a:hover {color: #000;}
#TB_window a:active {color: #666666;}
#TB_window a:focus{color: #666666;}

/* ----------------------------------------------------------------------------------------------------------------*/
/* ---------->>> thickbox settings <<<-----------------------------------------------------------------------------*/
/* ----------------------------------------------------------------------------------------------------------------*/
#TB_overlay {
	position: fixed;
	z-index:100;
	top: 0px;
	left: 0px;
	height:100%;
	width:100%;
}

.TB_overlayMacFFBGHack {background: url(macFFBgHack.png) repeat;}
.TB_overlayBG {
	background-color:#FFFFFF;
	filter:alpha(opacity=75);
	-moz-opacity: 0.75;
	opacity: 0.75;
}

* html #TB_overlay { /* ie6 hack */
     position: absolute;
     height: expression(document.body.scrollHeight > document.body.offsetHeight ? document.body.scrollHeight : document.body.offsetHeight + 'px');
}

#TB_window {
	position: fixed;
	background: #ffffff;
	z-index: 102;
	color:#000000;
	display:none;
	border: 4px solid #525252;
	text-align:left;
	top:50%;
	left:50%;
}

* html #TB_window { /* ie6 hack */
position: absolute;
margin-top: expression(0 - parseInt(this.offsetHeight / 2) + (TBWindowMargin = document.documentElement && document.documentElement.scrollTop || document.body.scrollTop) + 'px');
}

#TB_window img#TB_Image {
	display:block;
	margin: 15px 0 0 15px;
	border-right: 1px solid #ccc;
	border-bottom: 1px solid #ccc;
	border-top: 1px solid #666;
	border-left: 1px solid #666;
}

#TB_caption{
	height:25px;
	padding:7px 30px 10px 25px;
	float:left;
}

#TB_closeWindow{
	height:25px;
	padding:11px 25px 10px 0;
	float:right;
}

#TB_closeAjaxWindow{
	padding:7px 10px 5px 0;
	margin-bottom:1px;
	text-align:right;
	float:right;
}

#TB_ajaxWindowTitle{
	float:left;
	padding:7px 0 5px 10px;
	margin-bottom:1px;
}

#TB_title{
	background-color:#e8e8e8;
	height:27px;
}

#TB_ajaxContent{
	clear:both;
	padding:2px 15px 15px 15px;
	overflow:auto;
	text-align:left;
	line-height:1.4em;
}

#TB_ajaxContent.TB_modal{
	padding:15px;
}

#TB_ajaxContent p{
	padding:5px 0px 5px 0px;
}

#TB_load{
	position: fixed;
	display:none;
	height:13px;
	width:208px;
	z-index:103;
	top: 50%;
	left: 50%;
	margin: -6px 0 0 -104px; /* -height/2 0 0 -width/2 */
}

* html #TB_load { /* ie6 hack */
position: absolute;
margin-top: expression(0 - parseInt(this.offsetHeight / 2) + (TBWindowMargin = document.documentElement && document.documentElement.scrollTop || document.body.scrollTop) + 'px');
}

#TB_HideSelect{
	z-index:99;
	position:fixed;
	top: 0;
	left: 0;
	background-color:#fff;
	border:none;
	filter:alpha(opacity=0);
	-moz-opacity: 0;
	opacity: 0;
	height:100%;
	width:100%;
}

* html #TB_HideSelect { /* ie6 hack */
     position: absolute;
     height: expression(document.body.scrollHeight > document.body.offsetHeight ? document.body.scrollHeight : document.body.offsetHeight + 'px');
}

#TB_iframeContent{
	clear:both;
	border:none;
	margin-bottom:-1px;
	margin-top:1px;
	_margin-bottom:1px;
}

/** flyover.css *********************************************/

/* Parent Objects */
#pg-top .cart-nav { overflow: visible; }

/* Flyover Core */
#menu-product-link { width: 75px; }
#menu-signin-link { width: 63px; }
#pg .flyover { position: absolute; top: -1000px; left: 0; z-index: 9999; width: 259px; }
#pg .flyover .fly-head-tab { height: 51px; background: url(/images/flyover/flyover-menu-item.png) no-repeat left top; }
#pg .flyover .fly-head-tab-wide { height: 51px; background: url(/images/flyover/flyover-menu-item-wide.png) no-repeat left top; }
#pg .flyover .fly-head-tab-wide-up { height: 59px; background: url(/images/flyover/flyover-menu-item-wide-up.png) no-repeat left top; }
#pg .flyover .fly-head-tab-wrap { position: absolute; top: 0; left: 0; }
#pg .flyover .fly-head-tab-wrap-up { position: absolute; top: 0; left: 0; }
#pg .flyover .fly-head-tab a { padding: 20px 0 0 35px; height: 31px; width: 86px; display: block; font-weight: bold; color: #FFFFFF; background: none; }
#pg .flyover .fly-head-tab-wide a { padding: 20px 0 0 25px; height: 31px; width: 234px; display: block; font-weight: bold; color: #FFFFFF; background: none; }
#pg .flyover .fly-head-tab-wide-up a { padding: 20px 0 0 25px; height: 31px; width: 234px; display: block; font-weight: bold; color: #FFFFFF; background: none; }
#pg .flyover .fly-head-tab a:hover, #pg .flyover .fly-head-tab-wide a:hover, #pg .flyover .fly-head-tab-wide-up a:hover { text-decoration: none; }
#pg .flyover .fly-main-content { position: absolute; top: 32px; left: 0; }
#pg .flyover .fly-main-content-up { position: absolute; bottom: -26px; left: 0; }
#pg .flyover .fly-inner-content { position: absolute; top: 21px; left: 7px; width: 240px; }
#pg .flyover .fly-gradient { padding: 0 12px 0 7px; width: 240px; background: url(/images/flyover/flyover-gradient.png) no-repeat left bottom; }
#pg .flyover .fly-gradient-short { background: url(/images/flyover/flyover-gradient-short.png) no-repeat left bottom; }
#pg .flyover .fly-top-cap { width: 259px; height: 19px; background: url(/images/flyover/flyover-top-cap.png) no-repeat left top; }
#pg .flyover .fly-main-bg { width: 259px; background: url(/images/flyover/flyover-background.png) repeat-y left; }
#pg .flyover .fly-bottom-cap { width: 259px; height: 26px; background: url(/images/flyover/flyover-bottom-cap.png) no-repeat left top; }
#pg .flyover ul { float: none; }
#pg .flyover ul li { float: none; background: none; padding: 0; font-size: 12px; line-height: 20px; }
#pg .flyover ul li a { float: none; display: block; padding: 0 0 0 20px; font-weight: normal; background: url(/images/flyover/flyover-bullet.gif) no-repeat left top; }
#pg .flyover ul li a:hover { text-decoration: none; color: #FFFFFF; background: url(/images/flyover/flyover-highlight.png) no-repeat left top; }
#pg .flyover ul li.flymenufirst { padding: 10px 0 0 0; }
#pg .flyover ul li.alsotop { padding: 0; }
#pg .flyover ul li.flymenufirst a { padding: 0 0 0 10px; font-weight: bold; font-size: 15px; background: none; }
#pg .flyover ul li.flymenufirst a:hover { color: #2264AC; background: none; }
#pg .flyover .flydivide { width: 240px; height: 1px; margin: 10px 0; background: url(/images/flyover/flyover-divider.png) no-repeat left top; }
#pg .flyover .arrow { padding: 0 12px 0 10px; display: inline; float: none; background: url(/images/bullet-sprites.gif) no-repeat right top; }
#pg .flyoff { display: none; }
#pg .flyon { display: block; }
/** popbox.css *********************************************/

#blur-overlay { position: fixed; top: 0; left: 0; z-index: 90; width: 100%; height: 500px; display:none; }
* html #blur-overlay { /* ie6 hack */ position: absolute; height: expression(document.body.scrollHeight > document.body.offsetHeight ? document.body.scrollHeight : document.body.offsetHeight + 'px'); }
.overlayMacFFBGHack { background: url(/images/macFFBgHack.png) repeat; }

#popBox { position: absolute; top: 0; left: 0; width: 250px; z-index: 100; text-align: center; }
#popBox .container { position: relative; width: 245px; height: 60px; z-index:100; }
#popLoading { display:none; text-align:left; padding:10px; height:40px; width: 225px; }
#popLoading strong { padding:2px 0 4px 10px; color:#317fbf; display:block; font-size:11px; }
#popImg { display:none; margin:6px 0 0 6px; }
#popBox .imgCaption { display:none; text-align:left; padding:10px 20px; }
#popBox .imgCaption p { margin:0; }
#popIframeContent { display:none; margin:18px 0 0 6px; }
#popBox .fadeTop, #popBox .fadeBtm, #popClose { display:none; z-index:101; position:absolute; }
#popBox .taxCalc #popIframeContent { margin:0; }
#popBox .helpMeChoose #popIframeContent { margin:-3px 0 0 -2px; }
#popShadow { display:none; position:absolute; top:-8px; left:-8px; z-index:55; line-height:0; }
/** footer.css *********************************************/

#pg-links { padding: 30px 40px; overflow: hidden; width: 868px; line-height: 18px; }
#pg-links .col { position: relative; float: left; width: 217px; font-size: 11px; }
#pg-links .col ul li a { color: #515151; }
#pg-links .col ul li.first { font-weight: bold; font-size: 12px; }
#pg-links .col ul li.gap { height: 10px; }

#pg-footer { padding: 45px 40px; background: url(/images/footer-fade.gif) top left no-repeat; font-size: 11px; line-height: 18px; }
#pg-footer a.logo-intuit { display: block; width: 75px; height: 23px; background: url(/images/logo-sprites.gif) 0 -100px no-repeat; text-indent: -5000px;  }
#pg-footer a.truste { position: relative; display: block; margin-right: 50px; width: 116px; height: 31px; float: right; background: url(/images/logo-sprites.gif) 0 -200px no-repeat;  text-indent: -5000px; }
#pg-footer a.verisign { position: relative; display: block; margin: -12px 25px 0 0; width: 93px; height: 52px; float: right; background: url(/images/logo-sprites.gif) 0 -300px no-repeat;  text-indent: -5000px; }
#pg-footer ul { list-style: none; margin: 0; padding: 0; overflow: auto; width: 100%; }
#pg-footer ul li { position: relative; float: left; padding-right: 4px; }

#foot-notes-toggle { margin-left: 40px; font-size: 11px; }
.footer-graphic-normal { padding-left: 10px; background: url(/images/footer-sprites.gif) no-repeat 0 2px; }
.footer-graphic-expanded { background: url(/images/footer-sprites.gif) no-repeat 0 -17px; }
#foot-notes-content { margin: 0 40px; padding-left: 10px; display: none; }
/** header-split-tabs.css *********************************************/

#pg-top.split .nav { padding: 53px 0 0 191px;}
#pg-top.split .nav .thin {float:right;}
#pg-top.split .nav .thin a { padding:13px 13px 13px 8px;}
#pg-top.split .nav .basic { margin-left:0;}
#pg-top.split .nav .products a { width:52px;}
#pg-top.split .nav ul li.invest { margin-right:10px;}

#pg-top.split #menu-product-link { position:absolute; top:35px; left:72px; padding:10px;}
#pg-top.split #menu-product-link .fly-head-tab-wrap { top:-25px;left:-72px;}
#pg-top.split #menu-product-link .fly-main-content { top:7px;left:-72px;}

