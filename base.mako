<%!
    title = ""
    description = ""
    sideContent = False
%>
<!DOCTYPE html>

<html class="progdesign">
<head>
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <title>${self.attr.title}</title>
    <meta name="description" content="${self.attr.title}">
    <meta name="author" content="Nicolas Vanhoren">

    <%block name="favicons">
    <link rel="shortcut icon" href="/common/static/img/icon.ico">
    </%block>
    <link rel="stylesheet" type="text/css" href="/common/static/css/base_style.css" />
    <%block name="head">
    </%block>
</head>
<body>

    <%block name="beforeContent">
    </%block>

    <div class="mainHorizontalTable">
        <div class="contentRow">
            <div class="contentTable">
                % if self.attr.sideContent:
                <div class="leftAreaCell">
                    <%block name="sideContent">
                    </%block>
                </div>
                %endif
                <div class="rightAreaCell">
                    <%block name="headerMainContent">
                    </%block>
                    <%block name="mainContent">
                    </%block>
                </div>
            </div>
        </div>
        <div class="footerRow">
            <div class="footerCell">
                Copyright © 2013 <a href="https://github.com/nicolas-van">Nicolas Vanhoren</a><br />
                All Rights Reserved
            </div>
        </div>
    </div>

    <%block name="afterContent">
    </%block>

  <!--[if lt IE 8]>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>
    <script>
        // You may want to place these lines inside an onload handler
        CFInstall.check({
        mode: "overlay"
        });
    </script>
  <![endif]-->
</body>
</html>
