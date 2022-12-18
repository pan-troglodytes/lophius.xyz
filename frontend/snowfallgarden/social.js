/**
 *
 * @licstart  The following is the entire license notice for the 
 *  JavaScript code in this page.
 *
 * Copyright (C) 2022 sacha
 *
 *
 * The JavaScript code in this page is free software: you can
 * redistribute it and/or modify it under the terms of the GNU
 * General Public License (GNU GPL) as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version.  The code is distributed WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.
 *
 * As additional permission under GNU GPL version 3 section 7, you
 * may distribute non-source (e.g., minimized or compacted) forms of
 * that code without the copy of the GNU GPL normally required by
 * section 4, provided you include this license notice and a URL
 * through which recipients can access the Corresponding Source.
 *  
 *  @licend  The above is the entire license notice
 * for the JavaScript code in this page.
 *
 */
function demoSnowflakes(id) {
	if (id == "entryfail") {
		alert("This code has yet to be audited. Despite the use of server side validation, I've decided to also manually review all submitted code. If I decide to allow this code can be ran this demo button will work. If you want to run this code anyway you may copy and paste it and run it elsewhere. Please dont take my judgement as advice. All code you execute and/or distribute on your website is at your own discretion");
	} else {
		container = document.getElementById("snowflake-container");
		snowflake = document.getElementById(id);
		removeChildren(container);
		container.innerHTML = htmlDecode(snowflake.innerHTML);
	}
}
function htmlDecode(input) {
	  var doc = new DOMParser().parseFromString(input, "text/html");
	  return doc.documentElement.textContent;
}
function removeChildren(parent) {
	while (parent.lastChild) {
		parent.removeChild(parent.lastChild);
	}
}
