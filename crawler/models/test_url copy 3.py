# -*- coding: utf-8 -*-
import lxml
from lxml import etree, html
def create_root_node(text, parser_cls, base_url=None):
    """Create root node for text using given parser class.
    """
    body = text.strip().replace('\x00', '').encode('utf8') or b'<html/>'
    parser = parser_cls(recover=True, encoding='utf8')
    root = etree.fromstring(body, parser=parser, base_url=base_url)
    if root is None:
        root = etree.fromstring(b'<html/>', parser=parser, base_url=base_url)
    return root


body = '''	<html>

<head>

<title>富山市電子入札システム　トップページ</title>

<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"/>

</head>

<frameset rows="71,*" framespacing="0" frameborder="no" border="0">

<frame name="topFrame" scrolling="NO" noresize src="title.html" frameborder="NO" >

  <frameset rows="*,110" framespacing="0" frameborder="no" border="0">

    <frameset cols="459,*" framespacing="0" frameborder="no" border="0">

<frameset rows="83,*" frameborder="NO" border="0" framespacing="0">

<frame name="topFrame2" scrolling="NO" noresize src="system.html" >

<frame name="topFrame1" scrolling="NO" noresize src="menu.html" frameborder="NO" >

</frameset>

<frameset rows="35,*" frameborder="NO" border="0" framespacing="0">

<frame name="rightFrame" scrolling="NO" noresize src="wt.html" frameborder="NO">

<frame name="bottomFrame" scrolling="AUTO" noresize src="w.html" frameborder="NO">

</frameset>

</frameset>

<frame name="mainFrame" src="help.html" frameborder="NO" noresize scrolling="NO">

</frameset>

</frameset>

<noframes>

<body bgcolor="#FFFFFF" text="#000000"> </body>

</noframes>

</html>

'''

body = '''<html lang="ja"><head>
	
	<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
	





























	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Cache-Control" content="no-cache">
	<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT">





	<link rel="STYLESHEET" type="text/css" href="/PPIPublish/ppi/ejpcj/css/EjPCHCommon.css" title="default">
	<link rel="STYLESHEET" type="text/css" href="/PPIPublish/ppi/ejpcj/css/EjPCHCals.css" title="default">
	<link rel="STYLESHEET" type="text/css" href="/PPIPublish/ppi/ejpcj/css/EjPCHMain.css" title="default">





		<link rel="STYLESHEET" type="text/css" href="/PPIPublish/ppi/ejpcj/css/EjPCHOthersBrowser.css" title="default">



	<script language="JavaScript">
	<!--
		var contextPath   = '/ebidPPIPublish';
		var defaultAction = '/ebidPPIPublish/EjPPIj';

		var cssPath = '/PPIPublish/ppi/ejpcj/css/' ;
		var imgPath = '/PPIPublish/ppi/ejpcj/img/' ;

	//-->
	</script>
	<script language="JavaScript" src="/PPIPublish/ppi/ejpcj/script/EjPCHCommon.js"></script>
	<script language="JavaScript" src="/PPIPublish/ppi/ejpcj/script/EjPCHScreen.js"></script>
	<script language="JavaScript">
	<!--
	// 一般競争入札
	var OPEN_BID = "100201";
	// 公募型指名競争入札
	var SOUGHT_TYPE_SELECTIVE_BID = "200202";
	// 指名競争入札
	var SELECTIVE_BID = "200203";
	// 公募型競争入札
	var SOUGHT_TYPE_COMPETITIVE_BID = "200204";
	// 公募型プロポーザル
	var SOUGHT_TYPE_PROPOSAL = "300205";
	// 標準プロポーザル
	var STANDARD_PROPOSAL = "300206";
	// 工事希望型指名競争入札
	var CONSTRUCTION_HOPE_TYPE_SELECTIVE_BID = "200207";
	// 随意契約
	var FREE_CONTRACT = "300208";
	//-->
	</script>

	<script language="JavaScript" src="/PPIPublish/ppi/ejpcj/script/EjPCJTenderMethodContents.js"></script>







	<title>ふくい入札情報サービス -受注者-</title>



</head>



<frameset rows="68,*,30" frameborder="0" border="0" resizable="no">


		<frame src="/ebidPPIPublish/ppi/ejpcj/jsp/common/EjPCJ000030c.jsp" marginheight="0" marginwidth="0" name="Top_Frm" scrolling="no" frameborder="0" noresize="">
		<frame src="/ebidPPIPublish/ppi/ejpcj/jsp/common/EjPCJ000050c.jsp" marginheight="0" marginwidth="0" name="MainFrm" frameborder="0" noresize="">
		<frame src="/ebidPPIPublish/ppi/ejpcj/jsp/common/EjPCE010010t.jsp" marginheight="0" marginwidth="0" name="BtnFrame" scrolling="no" frameborder="0" noresize="">

	<noframes>
		<BODY bgcolor="#FFFFFF">
			<P>このページをご覧頂くにはフレーム対応のブラウザが必要です。</P>
		</BODY>
	</noframes>
</frameset>

</html>'''
parser = html.HTMLParser(recover=True, encoding='utf8')
r = etree.fromstring(body, parser=parser)
rs = r.xpath('//title')[0]
rs = r.xpath("//*[self::iframe or self::frame]")
print ([i.get('src') for i in rs ])
# print (str(rs.tag))