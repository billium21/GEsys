# -*- coding: utf-8 -*-
template = """
<!--DOCTYPE HTML-->
<HTML>
    <head>
        <title>Size Report</title>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
		
		<script type="text/javascript" src="http://mbraak.github.io/jqTree/tree.jquery.js"></script>
		
		<style>
			ul.jqtree-tree {{
			    margin-left: 12px;
			}}

			ul.jqtree-tree,
			ul.jqtree-tree ul.jqtree_common {{
			    list-style: none outside;
			    margin-bottom: 0;
			    padding: 0;
			}}

			ul.jqtree-tree ul.jqtree_common {{
			    display: block;
			    margin-left: 12px;
			    margin-right: 0;
			}}
			ul.jqtree-tree li.jqtree-closed > ul.jqtree_common {{
			    display: none;
			}}

			ul.jqtree-tree li.jqtree_common {{
			    clear: both;
			    list-style-type: none;
			}}
			ul.jqtree-tree .jqtree-toggler {{
			    display: block;
			    position: absolute;
			    left: -1.5em;
			    top: 30%;
			    *top: 0;  /* fix for ie7 */
			    font-size: 12px;
			    line-height: 12px;
			    font-family: arial;  /* fix for ie9 */
			    border-bottom: none;
			    color: #333;
			}}

			h4 {{
			    font-size: 14px;
			    line-height: 14px;
			    font-family: arial;  /* fix for ie9 */
			    color: #1C4257;
			}}

			h5 {{
			    font-size: 10px;
			    line-height: 10px;
			    font-family: arial;  /* fix for ie9 */
			    color: #1C4257;
			}}

			ul.jqtree-tree .jqtree-toggler:hover {{
			    color: #000;
			}}

			ul.jqtree-tree .jqtree-element {{
			    cursor: pointer;
			}}

			ul.jqtree-tree .jqtree-title {{
			    color: #1C4257;
			    vertical-align: middle;
			}}

			ul.jqtree-tree li.jqtree-folder {{
			    margin-bottom: 4px;
			}}

			ul.jqtree-tree li.jqtree-folder.jqtree-closed {{
			    margin-bottom: 1px;
			}}

			ul.jqtree-tree li.jqtree-folder .jqtree-title {{
			    margin-left: 0;
			}}

			ul.jqtree-tree .jqtree-toggler.jqtree-closed {{
			    background-position: 0 0;
			}}

			span.jqtree-dragging {{
			    color: #fff;
			    background: #000;
			    opacity: 0.6;
			    cursor: pointer;
			    padding: 2px 8px;
			}}

			ul.jqtree-tree li.jqtree-ghost {{
			    position: relative;
			    z-index: 10;
			    margin-right: 10px;
			}}

			ul.jqtree-tree li.jqtree-ghost span {{
			    display: block;
			}}

			ul.jqtree-tree li.jqtree-ghost span.jqtree-circle {{
			    background-image: url(jqtree-circle.png);
			    background-repeat: no-repeat;
			    height: 8px;
			    width: 8px;
			    position: absolute;
			    top: -4px;
			    left: 2px;
			}}

			ul.jqtree-tree li.jqtree-ghost span.jqtree-line {{
			    background-color: #0000ff;
			    height: 2px;
			    padding: 0;
			    position: absolute;
			    top: -1px;
			    left: 10px;
			    width: 100%;
			}}

			ul.jqtree-tree li.jqtree-ghost.jqtree-inside {{
			    margin-left: 48px;
			}}

			ul.jqtree-tree span.jqtree-border {{
			    position: absolute;
			    display: block;
			    left: -2px;
			    top: 0;
			    border: solid 2px #0000ff;
			    -webkit-border-radius: 6px;
			    -moz-border-radius: 6px;
			    border-radius: 6px;
			    margin: 0;
			}}

			ul.jqtree-tree .jqtree-element {{
			    width: 100%; /* todo: why is this in here? */
			    *width: auto; /* ie7 fix; issue 41 */
			    position: relative;
			}}

			ul.jqtree-tree li.jqtree-selected > .jqtree-element,
			ul.jqtree-tree li.jqtree-selected > .jqtree-element:hover {{
			    background-color: #97BDD6;
			    background: -webkit-gradient(linear, left top, left bottom, from(#BEE0F5), to(#89AFCA));
			    background: -moz-linear-gradient(top, #BEE0F5, #89AFCA);
			    background: -ms-linear-gradient(top, #BEE0F5, #89AFCA);
			    background: -o-linear-gradient(top, #BEE0F5, #89AFCA);
			    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.7);
			}}

			ul.jqtree-tree .jqtree-moving > .jqtree-element .jqtree-title {{
			    outline: dashed 1px #0000ff;
			}}
		</style>

		<script type="text/javascript">
			var data = {json};

			$(function() {{
			    $('#tree1').tree({{
				data: data
			    }});
			}});
		</script>

	</head>

	<body>
	        <h4>{summary} </h4><hr>
		<div id="tree1"></div>
		<h5>{timestamp} </h5>
	</body>
<HTML>
"""
