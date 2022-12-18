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
window.onload = function() {
	var snowflakeMaker = document.getElementById("snowflake-maker");
	var link = document.getElementById("download");
	var canvas = document.getElementById("snowflake-canvas");
	var ctx
	ctx = canvas.getContext("2d");
	var canvasX = document.getElementById("snowflake-canvas-x");
	var canvasY = document.getElementById("snowflake-canvas-y");
	var mirrorX = true;
	var mirrorY = true;
	var tool = "#ffffff";
	var scale = 10;
	var spawner = document.createElement("section");
	var submit = document.getElementById("submit");
	var submitP = document.getElementById("submit-p");
	setSubmit(false);

	var params = window.location.search.split("?")[1];
	if (params != null) {
		params = params.split("&");
		for (let i in params) {
			var paramKeyValue = params[i].split("=");
			if (paramKeyValue[0] == "image") {
				fileToCanvas(paramKeyValue[1]);
			} else if (paramKeyValue[0] == "forkof") {
				//document.getElementById("snowflake-forkof").value = paramKeyValue[1]; 
				// when cloning a get param of forkof=<id> is used instead of this, because well that just werks apperently
			}
		}
	}
		
	function setSubmit(allow) {
		if (allow) {
			submit.removeAttribute("disabled");
			submitP.setAttribute("style", "display: none;");
		} else {
			submit.setAttribute("disabled", "true");
			submitP.removeAttribute("style");
		}
	}
	function nolongerFork() {
		let stateObj = { id: "100" };
		window.history.pushState(stateObj,"paint", "/paint.html");
	}
	function fileToCanvas(imageSource) {
		snowflakeMaker.style.display = "flex";
		document.getElementById("tools").style.display = "flex";
		var image = new Image();
		image.src = imageSource;
		image.addEventListener("load", function() {
			if (image.width > canvasX.getAttribute("max") || image.height > canvasY.getAttribute("max")) {
				alert("image is too large! Its dimensions must be less than "+canvasX.getAttribute("max")+"x"+canvasY.getAttribute("max"));
			} else {
				canvas.width = image.width*scale;
				canvas.height = image.height*scale;
				ctx.imageSmoothingEnabled = false;
				ctx.drawImage(image, 0,0, canvas.width, canvas.height);
			}
		})
	}
	function makeCanvas() {
		canvas.width = canvasX.value * scale;
		canvas.height = canvasY.value * scale;
		
	}

	var pixel
	function paint(x, y) {
		var xScaled = Math.floor(x/scale)*scale;
		var yScaled = Math.floor(y/scale)*scale;
		if (tool == "erase") {
			ctx.clearRect(xScaled,yScaled,scale,scale);
			if (mirrorX)	 {
				ctx.clearRect(xScaled,canvas.height-yScaled-scale,scale,scale);
			}
			if (mirrorY)	 {
				ctx.clearRect(canvas.width-xScaled-scale,yScaled,scale,scale);
			}
			if (mirrorX && mirrorY)	 {
				ctx.clearRect(canvas.width-xScaled-scale,canvas.height-yScaled-scale,scale,scale);
			}
		} else if (tool == "picker"){
			var pixel = ctx.getImageData(x,y,1,1).data;
			if (pixel[3]!=0) {
			document.getElementById("paintbrush").value = "#"+pixel[0].toString(16)+""+pixel[1].toString(16)+""+pixel[2].toString(16);
				tool = "rgba("+pixel[0]+","+pixel[1]+","+pixel[2]+","+pixel[3]+")";
			}
		} else {
			ctx.fillStyle = tool;
			// draw where user clicks
			ctx.fillRect(xScaled,yScaled,scale,scale);
			// mirrors
			if (mirrorX)	 {
				ctx.fillRect(xScaled,canvas.height-yScaled-scale,scale,scale);
			}
			if (mirrorY)	 {
				ctx.fillRect(canvas.width-xScaled-scale,yScaled,scale,scale);
			}
			if (mirrorX && mirrorY)	 {
				ctx.fillRect(canvas.width-xScaled-scale,canvas.height-yScaled-scale,scale,scale);
			}
		}
		setSubmit(false);
	}

	function style() {
		var canvasN = document.createElement('canvas');
		var ctxN = canvasN.getContext("2d");
		canvasN.width = canvas.width/scale; 
		canvasN.height = canvas.height/scale;
		ctxN.drawImage(canvas, 0,0, canvas.width/scale, canvas.height/scale);
		var id = murmurhash2_32_gc(canvasN.toDataURL(), "potato");
		spawner.setAttribute("id","snowflakes"+id);
		document.getElementById("snowflake-id").value = id;


		var amplitude = 100
		var offsetX = -110
		var offsetY = 0
		
		var i=offsetY;
		var step = ((100+Math.abs(offsetY))/100);

		var style = "";
		styleTag = document.createElement("style");

		//display: flex;justify-content: flex-start;gap: 100px;
		style = style + "#snowflakes"+id+" { overflow:hidden; pointer-events:none; image-rendering:pixelated; } ";
		style = style + "#snowflakes"+id+" > span { position:fixed; top:-"+canvasN.height+"px; height:calc(100vh + "+canvasN.height+"px); } "
		style = style + "#snowflakes"+id+" span div { width:"+canvasN.width+"px; height:"+canvasN.height+"px; position:relative; background-image:url("+canvasN.toDataURL("image/png")+"); animation: sine 15s linear 0s infinite normal;} ";

		//animation: sine 15s linear 1s infinte normal;
		style = style + "@keyframes sine { ";
		var j=0
		var k  = 0
		while (j < 101) {
			var newline = j+"%{left:"+Math.floor(((Math.sin(k)*amplitude)+offsetX))+"px; top:"+(i)+"%;} ";
			style = style+newline;
			j=j+1;
			i=i+step;
			k=k+.1;
		}
		style = style + "}";

		styleTag.innerHTML = style;
		spawner.innerHTML = "<!--snowflakes(v1) generated with: https://snowfallgarden.lophius.xyz-->"
		spawner.appendChild(styleTag);


	}

	function murmurhash2_32_gc(str, seed) {
	var
		l = str.length,
		h = seed ^ l,
		i = 0,
		k;
	
	while (l >= 4) {
		k = 
		((str.charCodeAt(i) & 0xff)) |
		((str.charCodeAt(++i) & 0xff) << 8) |
		((str.charCodeAt(++i) & 0xff) << 16) |
		((str.charCodeAt(++i) & 0xff) << 24);
		
		k = (((k & 0xffff) * 0x5bd1e995) + ((((k >>> 16) * 0x5bd1e995) & 0xffff) << 16));
		k ^= k >>> 24;
		k = (((k & 0xffff) * 0x5bd1e995) + ((((k >>> 16) * 0x5bd1e995) & 0xffff) << 16));
	
		h = (((h & 0xffff) * 0x5bd1e995) + ((((h >>> 16) * 0x5bd1e995) & 0xffff) << 16)) ^ k;
	
		l -= 4;
		++i;
	}
  
  switch (l) {
  case 3: h ^= (str.charCodeAt(i + 2) & 0xff) << 16;
  case 2: h ^= (str.charCodeAt(i + 1) & 0xff) << 8;
  case 1: h ^= (str.charCodeAt(i) & 0xff);
          h = (((h & 0xffff) * 0x5bd1e995) + ((((h >>> 16) * 0x5bd1e995) & 0xffff) << 16));
  }

  h ^= h >>> 13;
  h = (((h & 0xffff) * 0x5bd1e995) + ((((h >>> 16) * 0x5bd1e995) & 0xffff) << 16));
  h ^= h >>> 15;

  return h >>> 0;
}
	canvas.onmousemove = function(e) {
		var rect = this.getBoundingClientRect(),
		x = e.clientX - rect.left-10;
		y = e.clientY - rect.top-10;
		if (mouseDown) {
			paint(x,y);
		}
	}
	var mouseDown = false;
	document.body.onmousedown = function() { 
		mouseDown = true;
	}
	document.body.onmouseup = function() {
		mouseDown = false;
	}

	document.getElementById("paintbrush").oninput = function(){
		tool = document.getElementById("paintbrush").value;
	}
	document.getElementById("new-canvas").addEventListener('click', function(){
		if (canvasX.value > canvasX.getAttribute("max") || canvasY.value > canvasY.getAttribute("max")) {
			alert("image is too large! Its dimensions must be less than "+canvasX.getAttribute("max")+"x"+canvasY.getAttribute("max"));
		} else {
			snowflakeMaker.style.display = "flex";
			document.getElementById("tools").style.display = "flex";
			makeCanvas();
			setSubmit(false);
			nolongerFork();
		}
	});
	document.getElementById("erase").addEventListener('click', function(){
		tool = 'erase';
		document.getElementById("paintbrush").value = "erase";
	});
	document.getElementById("picker").addEventListener('click', function(){
		tool = 'picker';
		document.getElementById("paintbrush").value = "picker";
	});

	link.addEventListener('click', function() {
    var canvasN = document.createElement('canvas');
    var ctxN = canvasN.getContext("2d");


	canvasN.width = canvasX.value; 
	canvasN.height = canvasY.value;
	ctxN.drawImage(canvas,0,0, canvasN.width,canvasN.height);
	link.href = canvasN.toDataURL("image/png");
	link.download = "snowfallgarden-"+murmurhash2_32_gc(canvasN.toDataURL(), "potato")+".png";
	});
	document.getElementById("mirror-x").addEventListener('change', function(){
		if (mirrorX) {
			mirrorX = false;
		} else {
			mirrorX = true;
		}
	});
	document.getElementById("mirror-y").addEventListener('change', function(){
		if (mirrorY) {
			mirrorY = false;
		} else {
			mirrorY = true;
		}
	});

	document.getElementById("image-input").addEventListener('change', function() {
		var fr = new FileReader();
		fr.onload = function() {
			fileToCanvas(fr.result);
		}
		fr.readAsDataURL(document.getElementById("image-input").files[0]);
		setSubmit(false);
		nolongerFork();
	});
	document.getElementById("demo").addEventListener('click', function() {

		const removeChildren = (parent) => {
			while (parent.lastChild) {
				parent.removeChild(parent.lastChild);
			}
		};
		removeChildren(spawner);
		
		style();


		newSnowflake(13);
		document.getElementById("snowflake-input").value = spawner.outerHTML;
		document.body.appendChild(spawner);
		setSubmit(true);

		
	});

	function newSnowflake(n) {
		var snowflake = document.createElement("div");
			snowflake.setAttribute("style", "animation-delay:"+ Math.round((Math.random() * 20)*10)/10+"s;"); 
			// > *20
			// random number between 0 and 20
			//  *10)/10
			//	round to 1 decimal place
			var div = document.createElement("span");
			div.setAttribute("style", "left:"+((n*10)-20)+"vw;");
			div.appendChild(snowflake);
			spawner.appendChild(div);
		//}

		var next = n - 1;
		if (next > 0) {
			newSnowflake(next);
		}
	}
}
