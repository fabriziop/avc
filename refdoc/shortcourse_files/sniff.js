/* ###########################################################################

GLOBAL ASSETS RELEASE v3.9

SUN COMMON JS LIB v7.7

BUILD DATE: 20080625

COPYRIGHT SUN MICROSYSTEMS INC. 2008

CONTACT US AT http://www.sun.com/secure/contact/cer.jsp?id=1073e17d-8d6c-43f6-b7e8-cf210cc89ba9 WITH ANY QUESTIONS

########################################################################### */

// ###########################################################################
// BEGIN REG LIBRARY
// ###########################################################################

/*
reg library version 1.0
copyright 2008 Sun Microsystems
this lib does:
 - dom helper functions
 - event utilities
 - page load & traversal
 - javascript behavior simulation
 - css-like element selection and matching
*/

// ############################# HELPER FUNCTIONS ############################

// TEST FOR CLASS NAME
(function(){
	var patts={};// cache regexps for performance
	window.hasClassName=function(element, className){
		if(!patts[className]){patts[className]=new RegExp("(^|\\s)"+className+"($|\\s)");}
		return element.className && patts[className].test(element.className);
	};
})();

// ADD CLASSES TO OBJECTS
function addClassName(element, className){
	if (hasClassName(element, className)) { return false; }
	if (!element.className) { element.className = className; }
	else { element.className += ' '+className; }
	return true;
}

// REMOVE CLASSES FROM OBJECTS
function removeClassName(element, className){
	if (!hasClassName(element, className)) { return false; }
	var classNames = element.className.split(' ');
	var newClassNames = [];
	for (var a=0; a<classNames.length; a++){
		if (classNames[a] != className) { newClassNames.push(classNames[a]); }
	}
	element.className = newClassNames.join(' ');
	return true;
}

// TOGGLE CLASS NAME
function toggleClassName(element, className) {
	if (hasClassName(element, className)) { removeClassName(element, className); }
	else { addClassName(element, className); }
}

// SWITCH CLASS NAME A->B, B->A
function switchClassName(element, className1, className2) {
	if (className1 == className2) { throw "className1 and className2 both equal "+className1; }
	var has1 = hasClassName(element, className1);
	var has2 = hasClassName(element, className2);
	if (has1 && has2) { removeClassName(element, className2); }
	else if (!has1 && !has2) { addClassName(element, className1); }
	else if (has1) { removeClassName(element, className1); addClassName(element, className2); }
	else { removeClassName(element, className2); addClassName(element, className1); }
}

// TEST FOR CLASS NAME BY PATTERN
function matchClassName(element, pattern){
	var classNames = element.className.split(' ');
	for (var a=0; a<classNames.length; a++){
		var matches = classNames[a].match(pattern);
		if (matches) { return matches; }
	}
	return null;
}

// FIND PREVIOUS ELEMENT
function prevElem(el) {
	var prev = el.previousSibling;
	while(prev && prev.nodeType!=1){prev=prev.previousSibling;}
	return prev;
}

// FIND NEXT ELEMENT
function nextElem(el) {
	var next = el.nextSibling;
	while(next && next.nodeType!=1){next=next.nextSibling;}
	return next;
}

// ADD INNER WRAPPER
function innerWrap(el, wrapperEl) {
	var nodes = el.childNodes;
	while (nodes.length > 0) {
		var myNode = nodes[0];
		el.removeChild(myNode);
		wrapperEl.appendChild(myNode);
	}
	el.appendChild(wrapperEl);
}

// ADD OUTER WRAPPER
function outerWrap(el, wrapperEl) {
	el.parentNode.insertBefore(wrapperEl, el);
	el.parentNode.removeChild(el);
	wrapperEl.appendChild(el);
}

// GET PARENT
function getParent(el, sel) {
	var parsedSel = new Selector(sel);
	while (el.parentNode) {
		el = el.parentNode;
		if (el.nodeType==1 && parsedSel.matchesElement(el)) { return el; }
	}
	return null;
}

// SHORTCUT FOR BUILDING ELEMENTS
function elem(name, atts, content) {
	// name: a tag name, with optional class or id: 'div', 'div.foo', 'div#bar', 'div.foo#bar', 'div#bar.foo'
	// atts: optional. object where keys=attribute names, values=attribute values: {'href':'page.html','target':'_blank'}
	// content: optional. either a string, or an element, or an arry of strings or elements
	if (name.indexOf('.') + name.indexOf('#') > -2) {
		var className = (name.indexOf('.') > -1) ? name.replace(/^.*\.([^\.#]*).*$/,"$1") : "";
		var id = (name.indexOf('#') > -1) ? name.replace(/^.*#([^\.#]*).*$/,"$1") : "";
		name = name.replace(/^([^\.#]*).*$/,'$1');
	}
	var e = document.createElement(name);
	if (className) { e.className = className; }
	if (id) { e.id = id; }
	if (atts) {
		var key;
		for (key in atts) {
			// setAttribute() has shaky support, try direct methods first
			if (key == 'class') { e.className = atts[key]; }
			else if (key == 'id') { e.id = atts[key]; }
			else if (key == 'href') { e.href = atts[key]; }
			else if (key == 'action') { e.action = atts[key]; }
			else if (key == 'method') { e.method = atts[key]; }
			else if (key == 'title') { e.title = atts[key]; }
			else if (key == 'alt') { e.alt = atts[key]; }
			else if (key == 'border') { e.border = atts[key]; }
			else if (key == 'caption') { e.caption = atts[key]; }
			else if (key == 'cellspacing') { e.cellspacing = atts[key]; }
			else if (key == 'for') { e.htmlFor = atts[key]; }
			else { e.setAttribute(key, atts[key]); }
		}
	}
	if (content) {
		if (!(content instanceof Array)) {
			content = [content];
		}
		for (var a=0; a<content.length; a++) {
			if (typeof content[a] == 'string') {
				e.appendChild(document.createTextNode(content[a]));
			}else{
				e.appendChild(content[a]);
			}
		}
	}
	if (name.toLowerCase() == 'img' && !e.alt) { e.alt = ''; }
	return e;
}

// GRAB JUST THE TEXTUAL DATA OF AN ELEMENT
function elemText(el) {
	// <a id="foo" href="page.html">click <b>here</b></a>
	// elemText(document.getElementById('foo')) == "click here"
	var r = el.innerHTML.replace(/<img[^>]+alt="([^">]+)[^>]+>/ig,'$1').replace(/<[^>]+>/ig,'');
	var d = elem('div');
	d.innerHTML = r;
	r = (d.childNodes[0]) ? d.childNodes[0].data : '';
	d = null;
	return r;
}

// GET SAFELY ENCODED STRINGS
function getSafelyEncodedString(s) {
	s = encodeURIComponent(s);
	s = s.replace(/&/,"&amp;").replace(/"/,"&quot;").replace(/</,"&lt;").replace(/>/,"&gt;");
	return s;
}

// SHORTHAND FOR VERBOSE DOM FUNCTIONS
function gebi(id){ return document.getElementById(id); }
function gebtn(tag, el){ if(!el){el=document;} return el.getElementsByTagName(tag); }

// ############################# EVENT UTILITIES #############################

// GET THE ELEMENT ON WHICH THE EVENT OCCURRED
function getTarget(e) {
	if (!e) { e = window.event; }
	if (e.target) { var targ = e.target; }
	else if (e.srcElement) { var targ = e.srcElement; }
	if (targ.nodeType == 3) { targ = targ.parentNode; } // safari hack
	return targ;
}

// CANCEL DEFAULT ACTION
function cancelDefault(e){
	if (typeof e.preventDefault != 'undefined') { e.preventDefault(); return; }
	e.returnValue=false;
}

// GENERIC EVENT ADDER, PLUS MEMORY LEAK PREVENTION
(function(){
	var evtLst = [];
	function rememberEvent(elmt,evt,hndl,cptr){
		evtLst.push([elmt,evt,hndl,cptr]);
	}
	function cleanup(){
		for(var a=0; a<evtLst.length; a++){
			var evt = evtLst[a];
			var elmt=evt[0];
			if(elmt.removeEventListener){
				elmt.removeEventListener(evt[1], evt[2], evt[3]);
			}
			if(elmt.detachEvent){
				elmt.detachEvent('on'+evt[1], evt[2]);
			}
		}
	}
	window.addEvent=function(elmt,evt,hndl,cptr) {
		cptr=(cptr)?true:false;
		if(elmt.addEventListener){
			elmt.addEventListener(evt,hndl,cptr);
			rememberEvent(elmt,evt,hndl,cptr);
		}else if(elmt.attachEvent){
			elmt.attachEvent("on"+evt,function(){hndl.call(elmt,window.event);});
			rememberEvent(elmt,evt,hndl);
		}
	}
	addEvent(window,'unload',cleanup);
})();

// ############################# LOAD AND TRAVERSAL ##############################

(function(){

	// we build these lists here where nobody can mess with them
	var preSetupQueue=[];
	var setupQueue={};
	var postSetupQueue=[];

	// just in case this isn't defined
	if(window.reg===undefined){window.reg={};}

	// traverse and act onload
	window.reg.setup=function(selector, setup, firstTimeOnly){
		firstTimeOnly=(firstTimeOnly)?true:false;
		var sq=setupQueue;
		var parsedSel = new Selector(selector);
		var tagNames=parsedSel.getTagNames();
		var regObj={
			selector:parsedSel,
			setup:setup,
			ran:false,
			firstTimeOnly:firstTimeOnly,
			isSimple:parsedSel.isSimple() // 'div.foo' is simple, 'div.foo > p' is not
		};
		for(var a=0;a<tagNames.length;a++){
			var tagName = tagNames[a];
			if(!sq[tagName]){sq[tagName]=[regObj];}
			else{sq[tagName][sq[tagName].length]=regObj;}
		}
	};
	// do this before setup
	window.reg.preSetup=function(fn){preSetupQueue.push(fn);};
	// do this after setup
	window.reg.postSetup=function(fn){postSetupQueue.push(fn);};
	// traversal helper
	var gebsHash = {}; // cache for perf.
	window.reg.getElementsBySelector = function(selString, startHere){
		if (!gebsHash[selString]) { gebsHash[selString] = new Selector(selString); }
		return gebsHash[selString].getMatchingElements(startHere);
	};

	// (re)run setup functions
	var runSetupFunctions = window.reg.rerun = function(el, cancelIfAlreadyRan){
		function runIt(el, regObj){
			regObj.setup.call(el);
			regObj.ran=true;
		}
		function shouldIgnore(el){
			// helps to not waste cycles checking simple elements like <p>
			return (!el.className && !el.id && el.nodeName != 'img');
		}
		var start = new Date().getTime();
		if (typeof el.setupFunctionsAlreadyRanHere != 'undefined' && el.setupFunctionsAlreadyRanHere && cancelIfAlreadyRan) { return; }
		var doc=(el)?el:document;
		var sq=setupQueue;
		var els=doc.getElementsByTagName('*');

		// crawl the dom
		for(var a=0;a<els.length;a++){
			var elmt=els[a];
			if (elmt.nodeType!=1){continue;}// ie7 does this for some reason
			var lcNodeName=elmt.nodeName.toLowerCase();
			var regObjArrayAll=sq['*'];
			var regObjArrayTag=sq[lcNodeName];
			var uninteresting = shouldIgnore(elmt);

			// any wildcards?
			if(regObjArrayAll){
				for(var b=0;b<regObjArrayAll.length;b++){
					var regObj=regObjArrayAll[b];
					if(uninteresting && regObj.isSimple){continue;}
					if(regObj.firstTimeOnly && regObj.ran){continue;}
					var matches = regObj.selector.matchesElement(elmt);
					if(matches){runIt(elmt, regObj);}
				}
			}

			// any items match this specific tag?
			if(regObjArrayTag){
				for(var b=0;b<regObjArrayTag.length;b++){
					var regObj=regObjArrayTag[b];
					if(uninteresting && regObj.isSimple){continue;}
					if(regObj.firstTimeOnly && regObj.ran){continue;}
					var matches = regObj.selector.matchesElement(elmt);
					if(matches){runIt(elmt, regObj);}
				}
			}
		}
		el.setupFunctionsAlreadyRanHere = true;
		var runtime = new Date().getTime() - start;
		if(!reg.setupRuntime){ reg.setupRuntime=runtime; }
		reg.lastSetupRuntime=runtime;
	}

	var loadFuncRan = false;
	function loadFunc(e) {
		if (!loadFuncRan) {
			for(var a=0;a<preSetupQueue.length;a++){
				preSetupQueue[a]();
			}
			runSetupFunctions(document, true);
			for(var a=0;a<postSetupQueue.length;a++){
				postSetupQueue[a]();
			}
			// postCrawl needs to go away ASAP
			if (typeof postCrawl != 'undefined') { var func; for (func in postCrawl) { postCrawl[func](); } }
			loadFuncRan = true;
		}
	}
	
	// contents of loadFunc only execute once, this sidesteps user agent sniffing 
	addEvent(window, 'load', loadFunc);
	addEvent(window, 'DOMContentLoaded', loadFunc);
})();

// ############################# BEHAVIOR SIMULATION ##############################

(function() {

	// these contain the event handling functions
	var clickHandlers = {};
	var mouseOverHandlers = {};
	var mouseOutHandlers = {};
	var focusHandlers = {};
	var blurHandlers = {};

	// just in case this isn't already defined
	if(window.reg===undefined){window.reg={};}
	
	// scrubber for convenience and consistency
	function getDepth(d){
		var result=d;
		if(result===null||result===undefined){result=-1;}
		result=parseInt(result);
		if(isNaN(result)){throw "bad arg for depth, "+d+" is not a number";}
		if(result<-1){throw "bad arg for depth, "+d+" is invalid, must be -1 or higher";}
		return result;
	}

	// add a handler function to a 
	function pushFunc(sel, handlerFunc, depth, handlers) {
		if(!handlerFunc){return;}
		depth=getDepth(depth);
		parsedSel=new Selector(sel);
		if(!handlers[sel]) {handlers[sel]=[];}
		handlers[sel].push({selector:parsedSel,handle:handlerFunc,depth:depth});
	}

	// click
	window.reg.click=function(sel, handlerFunction, depth){pushFunc(sel, handlerFunction, depth, clickHandlers);};

	// mouse over and out
	window.reg.hover=function(sel, overFunc, outFunc, depth){pushFunc(sel, overFunc, depth, mouseOverHandlers);pushFunc(sel, outFunc, depth, mouseOutHandlers);};
	window.reg.mouseover=function(sel, handlerFunction, depth){pushFunc(sel, handlerFunction, depth, mouseOverHandlers);};
	window.reg.mouseout=function(sel, handlerFunction, depth){pushFunc(sel, handlerFunction, depth, mouseOutHandlers);};

	// focus and blur
	window.reg.focusblur=function(sel, focusFunc, blurFunc, depth){pushFunc(sel, focusFunc, depth, focusHandlers);pushFunc(sel, blurFunc, depth, blurHandlers);};
	window.reg.focus=function(sel, focusFunc, depth){pushFunc(sel, focusFunc, depth, focusHandlers);};
	window.reg.blur=function(sel, blurFunc, depth){pushFunc(sel, blurFunc, depth, blurHandlers);};

	// the delegator
	function delegate(selectionHandlers, event) {
		var targ = getTarget(event);
		var sel; // make it local, otherwise mass confusion ensues
		if (selectionHandlers) {
			selectors:for (sel in selectionHandlers) {
				for(var a=0; a<selectionHandlers[sel].length; a++){
					var selHandler=selectionHandlers[sel][a];
					var depth = (selHandler.depth==-1) ? 100 : selHandler.depth;
					var el = targ;
					for (var b=-1; b<depth && el && el.nodeType == 1; b++, el=el.parentNode) {
						if (selHandler.selector.matchesElement(el)) {
							var retVal=selHandler.handle.call(el,event);
							// if they return false from the handler, cancel default
							if(retVal!==undefined && !retVal){
								cancelDefault(event);
							}
							break;
						}
					}
				}
			}
		}
	}

	// attach the events
	addEvent(document.documentElement,'click',function(e){
		delegate(clickHandlers, e);
	});
	addEvent(document.documentElement,'mouseover',function(e){
		delegate(mouseOverHandlers, e);
	});
	addEvent(document.documentElement,'mouseout',function(e){
		delegate(mouseOutHandlers, e);
	});
	if(typeof document.onactivate == 'object'){
		var focus = 'activate';
		var blur = 'deactivate';
	}else{
		var focus = 'focus';
		var blur = 'blur';
	}
	addEvent(document.documentElement,focus,function(e){
		delegate(focusHandlers, e);
	},true);
	addEvent(document.documentElement,blur,function(e){
		delegate(blurHandlers, e);
	},true);
	
	// handy for css
	addClassName(document.documentElement, 'regenabled');
})();

// ################################ SELECTORS ################################

(function(){

	// precompile these for performance
	var expressions = {
		leadSpace:  new RegExp("^\\s+"),
		tagName:    new RegExp("^([a-z_][a-z0-9_-]*)","i"),
		wildCard:   new RegExp("^\\*([^=]|$)"),
		className:  new RegExp("^(\\.([a-z0-9_-]+))","i"),
		pClassName: new RegExp("^(:([a-z0-9_-]+))","i"),
		id:         new RegExp("^(#([a-z0-9_-]+))","i"),
		att:        new RegExp("^(@([a-z_][a-z0-9_-]*))","i"),
		matchType:  new RegExp("(^\\^=)|(^\\$=)|(^\\!=)|(^\\*=)|(^=)"),
		spaceQuote: new RegExp("^\\s+['\"]")
	};

	// THIS CONSTRUCTOR CREATES PARSED REPRESENTATIONS OF CSS-LIKE SELECTORS
	window.Selector=function(selString) {
		var exp = expressions;
		this.items = []; // for each comma-separated selector, this array has an item
		var itms = []; // this will be added to this.items
		var count = 0;
		var origSel = selString;
		while (selString.length>0) {
			if (count > 100) { throw "failed parsing '"+origSel+"' stuck at '"+selString+"'"; }
			// get rid of any leading spaces
			if (exp.leadSpace.test(selString)) { selString=selString.replace(exp.leadSpace,''); }

			// find tag name
			var tagNameMatch = exp.tagName.exec(selString);
			if (tagNameMatch) {
				if (itms.length > 0 && itms[itms.length-1].name=='tag') { itms.push({name:'descendant'}); }
				itms.push({name:'tag',tagName:tagNameMatch[1].toLowerCase()});
				selString=selString.substring(tagNameMatch[1].length);
				tagNameMatch=null;
				continue;
			}
			// explicit wildcard selector
			if (exp.wildCard.test(selString)) {
				if (itms.length > 0 && itms[itms.length-1].name=='tag') { itms.push({name:'descendant'}); }
				itms.push({name:'tag',tagName:'*'});
				selString = selString.substring(1);
				continue;
			}
			var classMatch = exp.className.exec(selString);
			var pClassMatch = exp.pClassName.exec(selString);
			var idMatch = exp.id.exec(selString);
			var attMatch = exp.att.exec(selString);
			if (classMatch || pClassMatch || idMatch || attMatch) {
				// create a tag wildcard * if necessary
				if (itms.length==0 || itms[itms.length-1].name!='tag') { itms.push({name:'tag',tagName:'*'}); }
				var lastTag = itms[itms.length-1];
				// find class name, like .entry
				if (classMatch) {
					lastTag.className=classMatch[2];
					selString=selString.substring(classMatch[1].length);
					classMatch=null;
					continue;
				}
				// find pseudo class name, like :target
				if (pClassMatch) {
					var pClassName=pClassMatch[2];
					if('target'==pClassName){lastTag.targeted=true;}
					selString=selString.substring(pClassMatch[1].length);
					pClassMatch=null;
					continue;
				}
				// find id, like #content
				if (idMatch) {
					lastTag.id=idMatch[2];
					selString=selString.substring(idMatch[1].length);
					idMatch=null;
					continue;
				}
				// find attribute selector, like @src
				if (attMatch) {
					lastTag.attributeName=attMatch[2];
					selString=selString.substring(attMatch[1].length);
					attMatch=null;
					continue;
				}
			}
			// find attribute value specifier
			var matchTypeMatch=exp.matchType.exec(selString);
			if (matchTypeMatch) {
				// this will determine how the matching is done
				lastTag.matchType = matchTypeMatch[1] || matchTypeMatch[2] || matchTypeMatch[3] || matchTypeMatch[4] || matchTypeMatch[5];
				if(typeof lastTag.attributeName!='undefined'){
					selString=selString.substring(lastTag.matchType.length);
					if(selString.charAt(0)!='"'&&selString.charAt(0)!="'"){
						if(exp.spaceQuote.test(selString)){selString=selString.replace(exp.leadSpace,'');}
						else{throw origSel+" is invalid, single or double quotes required around attribute values";}
					}
					// it is enclosed in quotes, end is closing quote
					var q=selString.charAt(0);
					var lastQInd=selString.indexOf(q,1);
					if(lastQInd==-1){throw origSel+" is invalid, missing closing quote";}
					while(selString.charAt(lastQInd-1)=='\\'){
						lastQInd=selString.indexOf(q,lastQInd+1);
						if(lastQInd==-1){throw origSel+" is invalid, missing closing quote";}
					}
					lastTag.attributePattern=selString.substring(1,lastQInd);// lastTag should still be hanging around
					selString=selString.substring(lastTag.attributePattern.length+2);// +2 for the quotes
					continue;
				}
				matchTypeMatch=null;
			}
			// find child selector
			if (selString.charAt(0) == '>') {
				itms.push({name:'child'});
				selString=selString.substring(1);
				continue;
			}
			// find next sibling selector
			if (selString.charAt(0) == '+') {
				itms.push({name:'nextSib'});
				selString=selString.substring(1);
				continue;
			}
			// find after sibling selector
			if (selString.charAt(0) == '~') {
				itms.push({name:'followingSib'});
				selString=selString.substring(1);
				continue;
			}
			// find the comma separator
			if (selString.charAt(0) == ',') {
				this.items.push(itms);
				itms = [];
				selString = selString.substring(1);
				continue;
			}
			count++;
		}
		this.items.push(itms);
		this.selectorString=origSel;
		// do some structural validation
		for (var a=0;a<this.items.length;a++){
			var itms = this.items[a];
			if (itms.length==0) { throw "illegal structure: '"+origSel+"' contains an empty set"; }
			if (itms[0].name!='tag') { throw "illegal structure: '"+origSel+"' contains a dangling relation"; }
			if (itms[itms.length-1].name!='tag') { throw "illegal structure: '"+origSel+"' contains a dangling relation"; }
			for(var b=1;b<itms.length;b++){
				if(itms[b].name!='tag'&&itms[b-1].name!='tag'){ throw "illegal structure: '"+origSel+"' contains doubled up relations"; }
			}
		}
	}
})();

// FOR DEBUGGING, ETC
Selector.prototype.toString=function(){
	var result = this.selectorString+"\n======\n";
	for (var a=0;a<this.items.length;a++){
		for (var b=0;b<this.items[a].length;b++){
			var itm = this.items[a][b];
			result += itm.name;
			if(itm.name=='tag'){result+='='+itm.tagName;}
			if(itm.id){result+=' id='+itm.id;}
			if(itm.className){result+=' class='+itm.className;}
			if(itm.attributeName){result+=' att='+itm.attributeName;}
			if(itm.attributePattern){result+=' attPatt='+itm.attributePattern;}
			result+=' ';
		}
		result += "\n";
	}
	return result;
};

(function(){

	// SUBROUTINE FOR matchesElement()
	function matchIt(el, itm) {
		// try to falsify as soon as possible
		if (!el) { return false; }
		if (el.nodeName.toLowerCase()!=itm.tagName && itm.tagName!='*') { return false; }
		if (itm.className && !hasClassName(el,itm.className)) { return false; }
		if (itm.id && el.id != itm.id) { return false; }
		if (itm.targeted && (!location.hash || location.hash.substring(1) != el.id)) { return false; }
		if (itm.attributeName) {
			if (typeof el.hasAttribute != 'undefined') {
				if (!el.hasAttribute(itm.attributeName)) { return false; }
				var att = el.getAttribute(itm.attributeName);
			}else{
				if(el.nodeType!=1) {return false;}
				var att = el.getAttribute(itm.attributeName);
				if(itm.attributeName=='class'){att=el.className;}
				else if(itm.attributeName=='for'){att=el.htmlFor;}
				if(!att){return false;}
			}
			if (itm.attributePattern) {
				if (itm.matchType=='!='){
					if (att==itm.attributePattern){return false;}
				} else if (itm.matchType=='^='){
					if (att.indexOf(itm.attributePattern)!=0){return false;}
				} else if (itm.matchType=='*='){
					if (att.indexOf(itm.attributePattern)==-1){return false;}
				} else if (itm.matchType=='$='){
					if (att.indexOf(itm.attributePattern)!=att.length-itm.attributePattern.length){return false;}
				} else if (itm.matchType=='='){
					if (att!=itm.attributePattern){return false;}
				}else{
					if(!itm.matchType){throw "illegal structure, parsed selector cannot have null or empty attribute match type";}
					else{throw "illegal structure, parsed selector cannot have '"+itm.matchType+"' as an attribute match type";}
				}
			}
		}
		return true;
	}

	// PASS IT AN ELEMENT TO SEE IF IT MATCHES
	Selector.prototype.matchesElement = function(el) {
		if (!el) { throw this.selectorString+' cannot be evaluated against '+el; }
		if (el.nodeType != 1) { throw this.selectorString+' cannot be evaluated against element of type '+el.nodeType; }
		var result = new Array(this.items.length); // array of nulls. if one or more get set true, return true
		commas:for (var a=0;a<this.items.length;a++) { // for each comma-separated selector
			var tempEl = el;
			var itms = this.items[a];
			for (var b=itms.length-1; b>=0; b--) { // loop backwards through the items
				var itm = itms[b];
				if (itm.name == 'tag') {
					if (!matchIt(tempEl, itm)) {
						// these relational selectors require more extensive searching
						if (tempEl && b < itms.length-1 && itms[b+1].name=='descendant') { tempEl=tempEl.parentNode; b++; continue; }
						else if (tempEl && b < itms.length-1 && itms[b+1].name=='followingSib') { tempEl=tempEl.previousSibling; b++; continue; }
						else { continue commas; } // fail this one
					}
				}
				else if (itm.name == 'nextSib') { tempEl = prevElem(tempEl); }
				else if (itm.name == 'followingSib') { tempEl = prevElem(tempEl); }
				else if (itm.name == 'child') { tempEl = tempEl.parentNode; }
				else if (itm.name == 'descendant') { tempEl = tempEl.parentNode; }
			}
			result[a]=true;
		}
		for (var a=0;a<result.length;a++){if(result[a]){return true;}}
		return false;
	};

})();

// GETS THE TAG NAMES THAT THE SELECTOR REPRESENTS
Selector.prototype.getTagNames = function(el) {
	var hash = {}; // this avoids dupes
	for (var a=0;a<this.items.length;a++){
		hash[this.items[a][this.items[a].length-1].tagName]=null;
	}
	var result = [];
	var tag;
	for (tag in hash){result.push(tag);}
	return result;
}

// GETS ALL MATHCING ELEMENTS
Selector.prototype.getMatchingElements = function(startHere){
	if(!startHere){startHere = window.document;}
	var result = [];
	var tagNames = this.getTagNames();
	for (var a=0;a<tagNames.length;a++){
		var els = startHere.getElementsByTagName(tagNames[a]);
		for(var b=0;b<els.length;b++){
			if(els[b].nodeType!=1){continue;}
			if(this.matchesElement(els[b])){result.push(els[b]);}
		}
	}
	return (result.length>0)?result:null;
};

// FOR PERFORMANCE
Selector.prototype.isSimple = function() {
	return (this.items.length == 1 && this.items[0].length == 1);
}

// ###########################################################################
// END REG LIB, BEGIN XMLHTTPREQUEST FUNCTIONS
// ###########################################################################

// GENERIC HTTP REQUEST
function getfile(filepath,ftodo,fvar,ferr){
	var http_request = false;
	if (window.XMLHttpRequest) {
		http_request = new XMLHttpRequest();
		if (http_request.overrideMimeType && filepath.indexOf('.xml') > -1){
			http_request.overrideMimeType('text/xml');
		}
	}else if (window.ActiveXObject) { // IE
		try { http_request = new ActiveXObject("Msxml2.XMLHTTP");
		}catch(ex1){
			try{
				http_request = new ActiveXObject("Microsoft.XMLHTTP");
			}catch(ex2){}
		}
	}
	if (!http_request) {
		return false;
	}
	http_request.onreadystatechange = function() {
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
				if (filepath.indexOf('.xml') > -1){
					var rdata = http_request.responseXML.documentElement;
				}else{
					var rdata = http_request.responseText;
				}
				ftodo(rdata,fvar); // SUCCESS
			}else{
				if (ferr) { ferr(fvar,filepath,http_request.status,http_request.statusText); } // FAIL
			}
		}
	};
	http_request.open('GET', filepath, true);
	http_request.send(null);
}

// RETURN OBJECT FROM STRING
function getRequestObject(elementID,rdata,elementTag) {
	if (!elementTag){ elementTag = 'div'; } // elementTag optional, defaults to DIV
	var sudocont = document.createElement(elementTag);
	sudocont.innerHTML = rdata;
	var x = sudocont.getElementsByTagName(elementTag);
	var chunk;
	for (var i=0;i<x.length;i++) {
		if (x[i].id == elementID) {
			chunk = x[i];
			break;
		}
	}
	return chunk;
}

// BUILD AN ELEMENT FROM TEXT PULLED FROM XHR
function getElementByIdFromString(textBlob, id) {
	var container = document.createElement('div');
	container.innerHTML = textBlob;
	var tags = container.getElementsByTagName("*");
	for (var a=0; a<tags.length; a++){
		if (tags[a].id == id) { return tags[a]; }
	}
	return null;
}

// GENERIC XML HTTP REQUEST
function xhr(url, successFunc, failFunc, obj, postData){
	var http_request = false;
	if (window.XMLHttpRequest) {
		http_request = new XMLHttpRequest();
	}else if (window.ActiveXObject) { // IE
		try { http_request = new ActiveXObject("Msxml2.XMLHTTP"); }
		catch(e){
			try{ http_request = new ActiveXObject("Msxml3.XMLHTTP"); }
			catch(ex1){
				try{ http_request = new ActiveXObject("Microsoft.XMLHTTP"); }
				catch(ex2){}
			}
		}
	}
	if (!http_request) { return false; }
	if (!postData) { postData = null; }
	var method = (postData) ? "POST" : "GET";
	http_request.open(method, url, true);
	http_request.setRequestHeader('User-Agent','XMLHTTP/1.0');
	if (postData) { http_request.setRequestHeader('Content-type','application/x-www-form-urlencoded'); }
	http_request.onreadystatechange = function() {
		if (http_request.readyState == 4) {
			if (http_request.status == 200) {
				successFunc(http_request.responseText, obj);
			}else{
				failFunc(http_request.status, http_request.statusText, url, obj);
			}
		}
	};
	http_request.send(postData);
}

// GET DATA FROM A FORM FOR XHR
function getFormData(thisform) {
	var fargs = [];
	var inps = reg.getElementsBySelector("input, select, textarea",thisform);
	for (var a=0; a<inps.length; a++){
		var inp = inps[a];
		if (inp.type == "text" || inp.type == "hidden" || inp.type == "password"){
			fargs.push(encodeURIComponent(inp.name) + "=" + encodeURIComponent(inp.value));
		}
		if (inp.type == "checkbox" || inp.type == "radio" && inp.checked){
			fargs.push(encodeURIComponent(inp.name) + "=" + encodeURIComponent(inp.value));
		}
		if (inp.nodeName.toLowerCase()=='select'){
			fargs.push(encodeURIComponent(inp.name) + "=" + encodeURIComponent(inp.options[inp.selectedIndex].value));
		}
		if (inp.nodeName.toLowerCase()=='textarea'){
			fargs.push(encodeURIComponent(inp.name) + "=" + encodeURIComponent(inp.value));
		}
	}
	return fargs.join('&');
}

// ###########################################################################
// END XMLHTTPREQUEST FUNCTIONS, BEGIN SUN FUNCTIONS
// ###########################################################################

// BROWSER SNIFF
var is = new ottosniff();
function ottosniff(){
	var ua = navigator.userAgent.toLowerCase();
	var b = navigator.appName;
	if (b=="Netscape") this.b = "ns";
	else this.b = b;
	this.version = navigator.appVersion;
	this.v = parseInt(this.version);
	this.gecko = (ua.match(/\bgecko\/(20\d\d)(\d\d)(\d\d)/)) ? true : false;
	this.ns = (this.b=="ns" && this.v>=5);
	this.op = (ua.indexOf('opera')>-1);
	this.safari = (ua.indexOf('safari')>-1 && this.v < 5);
	this.safariAll = (ua.indexOf('safari')>-1);
	this.op7 = (this.op && this.v>=7 && this.v<8);
	this.op78 = (this.op && this.v>=7 || this.op && this.v>=8);
	this.ie5 = (this.version.indexOf('MSIE 5')>-1);
	this.ie6 = (this.version.indexOf('MSIE 6')>-1);
	this.ie7 = (this.version.indexOf('MSIE 7')>-1);
	this.ie56 = (this.ie5||this.ie6);
	this.ie567 = (this.ie5||this.ie6||this.ie7);
	this.iewin = (this.ie56 && ua.indexOf('windows')>-1 || this.ie7 && ua.indexOf('windows')>-1);
	this.iemac = (this.ie56 && ua.indexOf('mac')>-1);
	this.moz = (ua.indexOf('mozilla')>-1);
	this.ff = (ua.indexOf('firefox')>-1);
	this.moz13 = (ua.indexOf('mozilla')>-1 && ua.indexOf('1.3')>-1);
	this.oldmoz = (ua.indexOf('sunos')>-1 || this.moz13 && !this.ff || this.moz && ua.indexOf('1.4')>-1 && !this.ff || this.moz && ua.indexOf('1.5')>-1 && !this.ff || this.moz && ua.indexOf('1.6')>-1 && !this.ff);
	this.anymoz = this.gecko;
	this.ns6 = (ua.indexOf('netscape6')>-1);
}

// RTL SNIFF
var rtl = (document.documentElement.lang.indexOf('he') > -1 && document.documentElement.lang.indexOf('IL'))? true : false;

// ADD BROWSER CLASS TO HTML TAG
if(is.op){var bclass = "browserOpera";}
else if(is.safariAll){var bclass = "browserSafari";}
else if(is.ie56){var bclass = "browserExplorer56 browserExplorer";}
else if(is.ie7){var bclass = "browserExplorer7 browserExplorer";}
else if(is.iemac){var bclass = "browserExplorerMac";}
else if(is.oldmoz){var bclass = "browserOldMoz";}
else {var bclass = "";}
if(is.gecko){bclass += " gecko";}
bclass += " jsenabled";
addClassName(document.documentElement, bclass);

// IMG POSTLOAD
var imgpostload = [];
reg.postSetup(function(){
	if(typeof imgpostload=='undefined'){return;}
	for (var imp=0;imp<imgpostload.length;imp++){
		if(imgpostload[imp].title){
			imgpostload[imp].src = imgpostload[imp].title;
			imgpostload[imp].title = "";
		}
	}
});

if(typeof shutoff=='undefined'){var shutoff={global:false,share:false,pop:false,misc:false};}

if(!shutoff.global){
	reg.setup("div.a1r2 span.toolbarlinks > a,div.a1r2 span.siteid > a",sniffA1);
	reg.setup("ul#mtopics > li,div.a2topiclinks table tr td.navlinks > div",sniffA2);
	if(is.ie56){
		reg.setup("ul#mtopics",function(){
			reg.hover("ul#mtopics > li",function(){addClassName(this, 'a2mshow');},function(){removeClassName(this, 'a2mshow');});
		},true);
		reg.setup("td.navlinks",function(){
			reg.hover("div.a2topiclinks td.navlinks",function(){addClassName(this, 'a2mshow');},function(){removeClassName(this, 'a2mshow');}, 5);	
		},true);
		// rendering bug in ie6, "tickling" the dom like this fixes it
		reg.setup('div.g15v5 > table',function(){addClassName(this,'tickle');});
	}
	//  do goto set up for a2v8 if misc is set to false
	if(shutoff.misc){
		reg.preSetup(function(){
			var a2v8 = document.getElementById('a2v8');
			if (!a2v8) { return; }
			reg.setup("select.goto, select.showDiv",sniffGoto);
			reg.setup("ul.goto, ul.showDiv",sniffGotoUL);
		});
	}
}

if(!shutoff.share){reg.setup("div.pagetitle, div.smallpagetitle",sniffSharePage,true);}

if(!shutoff.pop){
	reg.setup("@class*='k2ajax-'",sniffK2ajax);
	reg.setup("@class*='k2over', @class*='k2focus', @class*='k2cl', @class*='k2show', @class*='k2hide'",sniffK2);
	reg.setup(".modal-launch, .modal-close",sniffModal);
	reg.setup('a.k5, area.k5', sniffK5Once, true);
}

if(!shutoff.misc){
	reg.setup("@class*='cTool-'",sniffClassTool);
	reg.setup("img@src*='_off.'",sniffRollover);
	reg.setup("div.g23",sniffG23);
	reg.setup("div.g27w2",sniffG27);
	reg.setup("div.imgbox",sniffImgbox);
	reg.setup("select.goto, select.showDiv",sniffGoto);
	reg.setup("ul.goto, ul.showDiv",sniffGotoUL);
	reg.setup(".xfadefirst",sniffXfade);
	reg.setup("ul.listfade",sniffListfade);
	reg.setup("a.loadUrl@href",sniffLoadUrl);
	reg.setup('a.imgswap, area.imgswap, img.imgswap, span.imgswap', sniffImgswap);
	reg.setup('a@class*="mswap", area@class*="mswap", span@class*="mswap", img@class*="mswap"', sniffMultiswap);
	reg.setup('img.postload', function(){imgpostload.push(this);});
	reg.setup('a.toggleObj, area.toggleObj', sniffToggler);
	reg.setup('a.toggle-all-table-checkboxes', sniffToggleAllCheckboxesInTable);
	reg.setup('div.pc1collapsible', sniffExpandCollapsePc1);
	reg.setup('form@class*="wgform-"', sniffFormHijax);
	reg.setup('div.g15v5 > table.details tr.main-row > th',function(){this.appendChild(elem('div.after',{},[elem('div.show',{},ltxt.showDetails),elem('div.hide',{},ltxt.hideDetails)]));});
	if (location.hash) { reg.setup('div.g15v5 table tbody:target',function(){removeClassName(this, 'collapsed');addClassName(this, 'uncollapsed');}); }
	if(is.ie56){reg.setup('div.g15v5 > table',function(){ addClassName(this, 'tickle'); });}
	if (typeof widgets != 'undefined'){reg.setup('.wg1', sniffWg1);}// can this go away?
}

reg.preSetup(function(){
	var cpy=gebi('copyDate');
	if(!cpy){return;}
	cpy.innerHTML = "1994-"+new Date().getFullYear()+' ';
});

// setup download page action
reg.preSetup(function(){
	var pc10 = document.getElementById('pc10');
	if (!pc10) { return; }
	var imgs = reg.getElementsBySelector("p.pc10img img.pc10img");
	if (!imgs || imgs.length==0) { return; }

	// now i know i'm on the right page
	for (var a=0; a<imgs.length; a++){
		var img = imgs[a];

		// need src for hovered and non-hovered versions
		var src = img.src;
		var src_over = src.replace(/(\.[a-z]+$)/,"_hvr$1");//x.png > x_hvr.png
	
		// append hovered image
		var img_over = img.cloneNode(true);
		img_over.src = src_over;
		img_over.className = 'pc10img_over';
		img.parentNode.appendChild(img_over);
	}

	// init the hover action
	if (!window.pc10active) {
		window.pc10active = true;
		reg.hover("div.pc10item",function(e){
			addClassName(this,'pc10itemover');
		},function(e){
			removeClassName(this,'pc10itemover');
		});
	}
});

// SETUP PRODUCT FINDER
reg.preSetup(function(){
	var fn1 = document.getElementById('productFinder');
	if(!fn1){return;}
	reg.setup('form#productFinderForm',function(){
		var ck = this.getElementsByTagName('input');
		for (var i=0;i<ck.length;i++){
			if(ck[i].type == "checkbox" && ck[i].checked == true){
				addClassName(ck[i].parentNode.parentNode, "checked");
			}else if(ck[i].type == "checkbox" && ck[i].checked == false){
				removeClassName(ck[i].parentNode.parentNode, "checked");
			}
		}
	});
	reg.setup('ul#fn1Filters',function(){
		// set up toggle links
		var ems = this.getElementsByTagName('em');
		for (var i=0;i<ems.length;i++){
			if(ems[i].parentNode.nodeName.toLowerCase() == "li"){
				var a = elem('a',{'href':'#toggleView'});
				a.onclick = function(){
					toggleClassName(this.parentNode.parentNode, "collapsed");
					return false;
				};
				innerWrap(ems[i],a)
			}
		}
		// collapse all but first 4 LIs, unless var showLIs exist
		var li = this.getElementsByTagName('li');
		var n = 0;
		for (var i=0;i<li.length;i++){
			if(li[i].parentNode == this && n > 3 && li[i].getElementsByTagName('li')[0] && li[i].getElementsByTagName('li')[0].className.indexOf('selection') > -1){
				addClassName(li[i], "collapsed");
			}else if(li[i].parentNode == this && li[i].getElementsByTagName('em')[0]){
				n++;
			}
		}
	});
});


// BUBBLING EVENTS
reg.focusblur("body",blurOut);
reg.focusblur("input.autoclear,input#searchfield",autoclearFocus,autoclearBlur);
reg.click('a@class*="hijax-", @class*="hijax-" a', hijaxLink);
reg.click('a.popup, area.popup, a.media-launch',bubblePop);
reg.click('div.g15v5 tr.main-row > th@scope="row"',function(ev){switchClassName(this.parentNode.parentNode, 'collapsed', 'uncollapsed');});
reg.hover("img.spriteswap",spriteOver,spriteOut, 0);
reg.click('div.a2topiclinks > ul > li > a',function(){clickA2(this,this.innerHTML.normalize(),this.innerHTML.normalize())});
reg.click('div.a2m a',function(){var p = this.parentNode.parentNode.parentNode.parentNode.getElementsByTagName('a')[0].innerHTML.normalize();clickA2(this,p,this.innerHTML.normalize())});

// SETUP -> A1
var a1 = [];
a1['x'] = 1;
function sniffA1(){
	var link = this;
	oldA1Content(); // LEGACY
	var a1w  = ['<div class="a1menux1"></div>\n<div class="a1menuw2"><div class="a1menuw1">\n','</div><div class="a1menux2"></div></div>'];
	if(!a1['ent']){
		for (key in a1) {
			var d = elem('div');
			d.innerHTML = key;
			a1[d.innerHTML] = a1[key];
		}
		a1['ent'] = true;
	}
	var linkText = link.innerHTML.normalize();
	var a1id = "a1menu"+a1['x'];
	a1['x']++;
	if (hasClassName(link, 'language-select')){
		var d = elem('div.a1menu');
		addClassName(link, 'k2over-languageselector y3 x-10');
		d.id = 'languageselector';
		d.style.width = "170px"
		d.innerHTML = a1w[0]+'<h5></h5><div></div>'+a1w[1];
 		link.parentNode.insertBefore(d,link.nextSibling);
		sniffK2.call(link);
 		sniffSiteSelector(link.parentNode);
	}else if(a1[linkText]){
		var d = elem('div.a1menu');
		addClassName(link, 'karrow');
		addClassName(link, 'k2over-'+a1id+' y3 x-6');
		if (hasClassName(link, "a1cart")){
			link.innerHTML = '<span class="carticon small">'+link.innerHTML+'</span>';
			link.style.paddingLeft = "0px";
		}
		if(a1[linkText].indexOf('a1-2col') > -1){
			var wc = 'a1Large';
		}else if(a1[linkText].indexOf('<p>') > -1){
			var wc = 'a1Medium';
		}else{
			var wc = 'a1Small';
		}
		d.id = a1id;
		addClassName(d,wc);
		d.innerHTML = a1w[0]+a1[linkText]+a1w[1];
		link.parentNode.insertBefore(d,link.nextSibling);
		sniffK2.call(link);
	}
}

// SETUP -> A2
var a2 = [];
function sniffA2(){
	var fobj = this;
	var sall=(typeof ltxt=='undefined')?seeall:ltxt.seeall;
	if(navmenu['1.0']) oldA2Content(); // LEGACY
 	if(document.getElementById('ip1')) oldA2TableFix(); // LEGACY
	if(!a2['ent']){
		for (key in a2) {
			var d = elem('div');
			d.innerHTML = key;
			a2[d.innerHTML.strip()] = a2[key];
		}
		a2['ent'] = true;
	}
	var n = fobj.getElementsByTagName('a')[0].innerHTML.normalize();
	if(a2[n]){
		var h = fobj.getElementsByTagName('a')[0].href;
		addEvent(fobj.getElementsByTagName('a')[0], 'focus', function(){
			if(this.parentNode.nodeName.toLowerCase() == 'li'){
				addClassName(this.parentNode, 'a2mshow');
				blurIt.push([this.parentNode,'a2mshow']);
			}else{
				addClassName(this.parentNode.parentNode, 'a2mshow');
				blurIt.push([this.parentNode.parentNode,'a2mshow']);
			}
		});
		var d = elem('div.a2m',{});
		d.style.marginLeft = (rtl)?'-'+(198 - fobj.offsetWidth)+'px':'-20px';
		var u = elem('ul',{});
		var a = elem('a',{'href':h});
		a.innerHTML = sall+' &#187;';
		var l =  elem('li',{});
		if (h.indexOf('#') < 0 && h.split('#')[1] != '') {
			l.appendChild(a);
		}
		u.innerHTML = a2[n];
		u.appendChild(l);
		d.appendChild(u);
		fobj.appendChild(d);
		addClassName(fobj.getElementsByTagName('li')[0], 'firstchild');
	}else if(fobj.nodeName.toLowerCase() == 'li'){
		addClassName(fobj, 'a2nomenu');
	}else{
		addClassName(fobj.parentNode, 'a2nomenu');
	}
}

// SETUP -> K5
function sniffK5Once() {
	var el = this;
	var cssK5 = elem('link',{'type':'text/css','href':cssdir+'/k5.css','rel':'stylesheet'});
	document.getElementsByTagName('head')[0].appendChild(cssK5);
	reg.click('a.k5, a.media-popin',k5Click);
	reg.click('.k5close',k5Close);
}
function pauseAll() {
	window.paused = true;
	addClassName(document.body,'paused');
}
function resumeAll() {
	window.paused = false;
	removeClassName(document.body,'paused');
}
function k5Click(e) {
	var clicked = this;
	
	// get the id to grab
	var idMatches = matchClassName(clicked,/^id-(\S+)$/);
	if (idMatches) {
		var id = idMatches[1];
	} else if (clicked.href.indexOf('#')!=-1) {
		var id = clicked.href.substring(clicked.href.indexOf('#')+1);
	}else{ throw 'no id value was specified for k5 object. className "id-someId" or URL anchor reference "...page.html#someId"'; }
	
	// which mode to trigger
	var k5DivClass = 'k5 k5empty';
	var isVid,isInf,isLog,isMed;
	if(hasClassName(clicked,'k5vid')){k5DivClass+=' k5vid';isVid=true;}
	else if(hasClassName(clicked,'k5login')){k5DivClass+=' k5login';isLog=true;}
	else if(hasClassName(clicked,'k5media')){k5DivClass+=' hijax-'+id;isMed=true;}
	else if(hasClassName(clicked,'k5info')){k5DivClass+=' k5info';isInf=true;}
	
	// get the title string
	var t = (clicked.title) ? clicked.title : elemText(clicked);
	
	// build some elements
	var title = elem('h2.k5title',{},t);
	var clSrc,clW,clH;
	if(isLog){clSrc=imdir+'/k5login_x.gif';clW=clH='21';}
	else if(isInf){clSrc=imdir+'/k5info_x.gif';clW=clH='21';}
	else{clSrc=imdir+'/ic_close_win_big_x.gif';clW='30';clH='19';}
	var close = elem('span.k5close',{},elem('img',{'title':'close','alt':'close','src':clSrc,'border':'0','width':clW,'height':clH}))
	var objectDiv = elem('div.k5w2',{},' ');
	objectDiv.refId = id;
	var k5VidImg = isVid ? elem('div.k5vidshadow',{},elem('img#k5vidshadow',{src:imdir+'/k5_vid_shadow.png',alt:''})) : ' ';
	var k5Div = elem('div',{'class':k5DivClass},[elem('div.k5w1',{},[title,elem('p.k5close',{},close),objectDiv,k5VidImg,elem('span.k5x1',{}),elem('span.k5x2',{}),elem('span.k5x3',{}),elem('span.k5x4',{})]),k5VidImg]);

	// position it from the  top
	var topMatch = matchClassName(clicked,/^top(\d+)$/);
	if(topMatch){
		k5Div.firstChild.style.marginTop=topMatch[1]+'px';
		if(isVid){k5VidImg.style.marginTop=topMatch[1]+'px';}
	}
	
	// append the element to the dom
	document.body.appendChild(k5Div);
	
	// size the element
	k5Div.sized = false;
	var matches = matchClassName(clicked,/^(\d+)(x(\d+))?$/);
	if (matches) {
		k5Div.sized = true;
		k5Div.firstChild.style.width = matches[1] + 'px';
		if (matches[3]) { objectDiv.style.height = matches[3] + 'px'; }
	}

	// in case ajax fails
	k5Div.setError = function(error,url) {
		removeClassName(this,'k5empty');
		addClassName(this,'k5error');
		this.firstChild.style.width = null;
		var objectDiv = this.firstChild.getElementsByTagName('div')[0];
		objectDiv.style.height = null;
		objectDiv.appendChild(elem('div',{'class':'g29 g29v2'},elem('div.g29w1',{},elem('div.g29w2',{},[elem('h5',{},"Unable to display content."),elem('p',{},"Error: "+error),elem('p',{},"URL: "+url),elem('p',{},"Please notify the website owner of this problem.")]))));
	};


	// ie6 needs special treatment
	var de=document.documentElement;
	if (is.ie6) {
		window.k5ie6bg = elem('div.k5ie6bg',{},'.');
		window.k5ie6bg.style.width = de.clientWidth + 'px';
		window.k5ie6bg.style.height = de.scrollHeight + 'px';
		document.body.appendChild(window.k5ie6bg);
		window.k5ie6bg.style.filter = 'alpha(opacity=60)';
		k5Div.style.width = de.clientWidth + 'px';
	}
	
	// so when it's closed the page can scroll back to where it was
	if (is.ie6||is.ie7) {
		k5Div.oldTop = de.scrollTop;
	} else {
		k5Div.oldTop = self.pageYOffset;
	}
	
	// glass over the viewport
	//k5Div.style.height = de.scrollHeight + 'px';
	//if (is.safari) { k5Div.style.height = self.innerHeight + 'px'; }
	window.scrollTo(0,0);
	
	var href = clicked.href;
	if (href.indexOf('#')!=-1) { href = href.substring(0,href.indexOf('#')); }
	var thisHref=location.href;
	if (thisHref.indexOf('#')!=-1) { thisHref = thisHref.substring(0,thisHref.indexOf('#')); }
	
	function success(str, objectDiv){
		var k5Div = objectDiv.parentNode.parentNode;
		var el = getRequestObject(objectDiv.refId,str);
		if (!el) { k5Div.setError("id "+objectDiv.refId+" not found",href); return; } // OOPS, #FRAG NOT FOUND
		var hdngs=reg.getElementsBySelector('.k5customtitle',el);
		if(hdngs&&hdngs.length>0){
			title.firstChild.data=elemText(hdngs[0]);
			hdngs[0].parentNode.removeChild(hdngs[0]);
		}
		removeClassName(el, 'hidethis');
		removeClassName(k5Div,'k5empty');
		objectDiv.appendChild(el);
		reg.rerun(objectDiv);
		var matches = matchClassName(el,/^(\d+)(x(\d+))?$/);
		if (matches && !k5Div.sized) {
			k5Div.firstChild.style.width = matches[1] + 'px';
			if (matches[3]) { objectDiv.style.height = matches[3] + 'px'; }
		}
		var vs = document.getElementById('k5vidshadow');
		if (vs) {
			vs.style.width = (k5Div.firstChild.offsetWidth+30)+'px';
			vs.style.height = (k5Div.firstChild.offsetHeight+30)+'px';
		}
		var inpts=reg.getElementsBySelector('input@type!="hidden",select,textarea',el);
		if(inpts&&inpts.length>0){
			inpts[0].focus();
		}
	}
	function fail(status, statusText, href, objectDiv){
		var k5Div = objectDiv.parentNode.parentNode;
		var err = (statusText) ? status + ' ' + statusText : status;
		k5Div.setError(err,href);
	}
	
	if(href==thisHref){
		var elmt=gebi(id);
		if (!elmt) { k5Div.setError("id "+objectDiv.refId+" not found",href); return; } // OOPS, #FRAG NOT FOUND
		var s='<div><div id="'+elmt.id+'" class="'+elmt.className+'">'+elmt.innerHTML+'</div></div>';
		success(s, objectDiv);
	}else{
		xhr(href, success, fail, objectDiv);
	}

	pauseAll();
	return false;
}
function k5Close(e){
	try{var k5Div = reg.getElementsBySelector('div.k5')[0];}catch(ex){return;}
	document.body.removeChild(k5Div);
	window.scrollTo(0,k5Div.oldTop);
	resumeAll();
	if (is.ie6) { document.body.removeChild(window.k5ie6bg); }
	return false;
}

// SETUP -> K2
ked = [];
function sniffK2(shownow){
	var fobj = this;
	var pdoc = document;
	fobj.prp = [0,0,0,"","",""];
	fobj.className = fobj.className.replace(/(k2over) +/,"$1-");
	fobj.className = fobj.className.replace(/(k2click) +/,"$1-");
	fobj.className = fobj.className.replace(/(k2focus) +/,"$1-");
	fobj.className = fobj.className.replace(/(k2close) +/,"$1-");

	var cls = fobj.className.split(' ');

	if(fobj.className.indexOf("k2ajaxload") > -1 && fobj.href && document.body.getElementsByTagName('div')[0] ){
		for (var v=0;v<cls.length;v++){
			if (cls[v].indexOf("k2over") > -1 || cls[v].indexOf("k2click") > -1 || cls[v].indexOf("k2focus") > -1){
				var k2id = cls[v].split('-');
				if (!k2id[2]){
					k2id[2] = k2id[1];
				}
			}
		}
		var link = document.createElement('a');
		link.className = 'loadUrl';
		link.href = fobj.href+'#'+k2id[2];
		if(!document.getElementById(k2id[2])){
			var div = document.createElement('div');
			div.className = 'g32auto';
			div.id = k2id[2];
			div.appendChild(link);
			document.getElementsByTagName('body')[0].getElementsByTagName('div')[0].appendChild(div);
		}
	}


	for (var v=0;v<cls.length;v++){
		if (cls[v].indexOf("k2over") > -1 || cls[v].indexOf("k2click") > -1 || cls[v].indexOf("k2focus") > -1){
			var p_objs = fobj.aob = cls[v].split('-');
			if (!p_objs[2]){
				fobj.aob[2] = p_objs[2] = p_objs[1];
				fobj.aob[1] = fobj;
			}
			kpop = document.getElementById(p_objs[2]);
			kpop.kp_objs = p_objs[2];
			kpop.kp_trig = p_objs[1];
		}else if (cls[v].indexOf("k2close") > -1){
			fobj.aob = cls[v].split('-');
		}else if (cls[v].indexOf("x") == 0){
			fobj.prp[0] = (cls[v].substring(1) * 1) + fobj.prp[0];
		}else if (cls[v].indexOf("y") == 0){
			fobj.prp[1] = (cls[v].substring(1) * 1) + fobj.prp[1];
		}else if (cls[v].indexOf("z") == 0){
			fobj.prp[2] = (cls[v].substring(1) * 1);
		}else if (cls[v].indexOf("pAbsolute") == 0){
			fobj.prp[3] = (cls[v].substring(1));
		}else if (cls[v].indexOf("vBottom") == 0 || cls[v].indexOf("vTop") == 0 || cls[v].indexOf("vMiddle") == 0 || cls[v].indexOf("vAlignTopBottom") == 0){
			fobj.prp[4] = cls[v];
		}else if (cls[v].indexOf("hRight") == 0 || cls[v].indexOf("hMiddleRight") == 0 || cls[v].indexOf("hLeft") == 0 || cls[v].indexOf("hMiddleLeft") == 0 || cls[v].indexOf("hMiddle") == 0 || cls[v].indexOf("hAlignRight") == 0){
			fobj.prp[5] = cls[v];
		}
	}
	if (fobj.aob[0].indexOf("k2over") > -1){
		addEvent(fobj,"mouseover",function(){
			showK2(this.aob[2],this.aob[1],this.prp[0],this.prp[1],this.prp[2],this.prp[3],this.prp[4],this.prp[5]);
		});
		if (!hasClassName(fobj, "mOverOff")){
			addEvent(kpop,"mouseover",function(){
				showK2(this.kp_objs);
			});
		}
		addEvent(kpop,"mouseout",function(){
			hideK2(this.kp_objs);
		});
		addEvent(fobj,"mouseout",function(){
			hideK2(this.aob[2]);
		});
		addEvent(fobj,"focus",function(){
			showK2(this.aob[2],this.aob[1],this.prp[0],this.prp[1],this.prp[2],this.prp[3],this.prp[4],this.prp[5]);
			blurIt.push([document.getElementById(this.aob[2]),'hidden']);
		});

		if(shownow){
			showK2(fobj.aob[2],fobj.aob[1],fobj.prp[0],fobj.prp[1],fobj.prp[2],fobj.prp[3],fobj.prp[4],fobj.prp[5]);
			return false;
		}
	}else if (fobj.aob[0] == "k2click"){
		addEvent(fobj,"click",function(e){
			showK2(this.aob[2],this.aob[1],this.prp[0],this.prp[1],this.prp[2],this.prp[3],this.prp[4],this.prp[5]);
			addK2(this.aob[2],this.aob[1],this.prp[0],this.prp[1],this.prp[2],this.prp[3],this.prp[4],this.prp[5]);
			cancelDefault(e);
			return false;
		});
		if(shownow){
			showK2(fobj.aob[2],fobj.aob[1],fobj.prp[0],fobj.prp[1],fobj.prp[2],fobj.prp[3],fobj.prp[4],fobj.prp[5]);
			addK2(fobj.aob[2],fobj.aob[1],fobj.prp[0],fobj.prp[1],fobj.prp[2],fobj.prp[3],fobj.prp[4],fobj.prp[5]);
			return false;
		}
	}else if (fobj.aob[0] == "k2focus"){
		addEvent(fobj,"focus",function(){
			showK2(this.aob[2],this.aob[1],this.prp[0],this.prp[1],this.prp[2],this.prp[3],this.prp[4],this.prp[5]);
			addK2(this.aob[2],this.aob[1],this.prp[0],this.prp[1],this.prp[2],this.prp[3],this.prp[4],this.prp[5]);
		});
		addEvent(fobj,"blur",function(){
			hideK2(this.aob[2],1);
		});
	}else if (fobj.aob[0] == "k2close"){
		addEvent(fobj,"click",function(e){
			hideK2(this.aob[1],1);
			cancelDefault(e);
		});
	}
	fobj.className = fobj.className.replace(/(k2over)-|(k2focus)-|(k2cl...)-/,"$1 ");
}
function showK2(popupID,callerID,Xoffset,Yoffset,Zindex,posy,btmup,ort,etype){
	var popupObj = document.getElementById(popupID);
	if (!popupObj){
		var popupObj = popupID;
	}
	if (callerID){
		var ptop = plft = 0;
		var callerObj = document.getElementById(callerID);
		if (!callerObj){
			var callerObj = callerID;
		}

		if (ort == "hLeft"){
			plft = plft - popupObj.offsetWidth;
		}else if (ort == "hMiddleLeft"){
			plft = plft - popupObj.offsetWidth;
			plft = plft + parseInt(callerObj.offsetWidth / 2);
		}else if (ort == "hMiddle"){
			plft = parseInt(callerObj.offsetWidth / 2);
			plft = plft - parseInt(popupObj.offsetWidth / 2);
		}else if (ort == "hMiddleRight"){
			plft = parseInt(callerObj.offsetWidth / 2);
		}else if (ort == "hRight"){
			plft = callerObj.offsetWidth;
		}else if (ort == "hAlignRight"){
			plft = plft + callerObj.offsetWidth - popupObj.offsetWidth;
		}

		if (btmup == "vTop"){
			ptop = ptop - popupObj.offsetHeight;
		}else if (btmup == "vMiddle"){
			ptop = ptop + parseInt(callerObj.offsetHeight / 2);
			ptop = ptop - parseInt(popupObj.offsetHeight / 2);
		}else if (btmup == "vBottom"){
			ptop = ptop + callerObj.offsetHeight;
		}else if (btmup == "vAlignBottom"){
			ptop = ptop + callerObj.offsetHeight - popupObj.offsetHeight;
		}else if (btmup == "vAlignTopBottom"){
			var scrolltop = 0;
			if( document.body && ( document.body.scrollLeft || document.body.scrollTop ) ) {
				scrolltop = document.body.scrollTop;
			}else if( document.documentElement && ( document.documentElement.scrollLeft || document.documentElement.scrollTop)){
				scrolltop = document.documentElement.scrollTop;
			}
			var winheight = 0;
			if( typeof( window.innerWidth ) == 'number' ) {
				winheight = window.innerHeight;
			} else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
				winheight = document.documentElement.clientHeight;
			}
			var alignbottom = callerObj.offsetHeight - popupObj.offsetHeight;
		}
		if (is.safari && posy == "Absolute"){
			if (posy != "Absolute"){
				callerObj.style.position = "relative";
			}
			getXY(callerObj.offsetParent);
		}else{
			getXY(callerObj);
		}

		ptop = ptop + callerObj.Y;
		plft = plft + callerObj.X;
		if (btmup == "vAlignTopBottom" && ptop > scrolltop + (winheight/2)){
			ptop = ptop + alignbottom;
			Yoffset = Yoffset * -1;
		}
		plft = plft + Xoffset;
		ptop = ptop + Yoffset;
		popupObj.style.top=ptop+'px';
		popupObj.style.left=plft+'px';
	}
	if (Zindex){
		popupObj.style.zIndex = Zindex;
	}
	popupObj.style.visibility = "visible";
}
function hideK2(popupID,popcls,fader){
	var popupObj = document.getElementById(popupID);
	if (!popupObj){
		var popupObj = popupID;
	}
	popupObj.style.visibility = "hidden";
	if (popcls){
		ked[popupID] = "";
	}
}
function addK2(p0,p1,p2,p3,p4,p5,p6,p7){
	ked[p0] = [p0,p1,p2,p3,p4,p5,p6,p7];
}
addEvent(window, 'resize', function(){
	var kdp;
	for (kdp in ked){
		if (ked[kdp][0]){
			showK2(ked[kdp][0],ked[kdp][1],ked[kdp][2],ked[kdp][3],ked[kdp][4],ked[kdp][5],ked[kdp][6],ked[kdp][7]);
		}
	}
});

// SETUP -> K2 W/ AJAX
function sniffK2ajax(){
	var fobj = this;
	var containerID = fobj.className.split('k2ajax-')[1].split(' ')[0];
	var fileUrl = document.getElementById(containerID).getElementsByTagName('a')[0].href;
	var mvnt = (fobj.className.indexOf('k2over-') > -1) ? 'mouseover' : 'click';
	addEvent(fobj,mvnt,function(){
		if(document.getElementById(containerID).innerHTML.indexOf('getUrl') > -1){
			var fvars = [containerID,fobj];
			getfile(fileUrl,function(rdata,fvar){
				if(rdata.indexOf('contentchunk') > -1){
					rdata = getRequestObject('contentchunk',rdata).innerHTML;
				}
				document.getElementById(fvar[0]).innerHTML = rdata;
				reg.rerun(document.getElementById(fvar[0]));
				sniffK2.call(fvar[1],true);
			},fvars);
		}
	});
}

// SETUP -> G23
function sniffG23(){
	var fobj = this;
	var uls = reg.getElementsBySelector('ul.g23tree',fobj);
	for (var a=0;a<uls.length;a++){
		var tree = uls[a];
		var lis = tree.getElementsByTagName('li');
		for (var b=0;b<lis.length;b++){
			var li = lis[b];
			var isDefaultExpanded = hasClassName(li, 'default-expanded');
			var isBranch = false;
			if (li.getElementsByTagName('ul').length>0){
				// it's a branch if there's a nested <ul>
				if (isDefaultExpanded) { addClassName(li, 'branch'); }
				else { addClassName(li, 'collapsed branch'); }
				isBranch = true;
				var subUl = li.getElementsByTagName('ul')[0];
				subUl.parentNode.removeChild(subUl);
				li.innerWrap = elem('div.g23x');
				innerWrap(li, li.innerWrap);
				li.appendChild(subUl);
			}
			var isLast = !nextElem(li);
			if (isLast) { addClassName(li, 'last'); }
			if (is.ie6) { li.isLast = isLast; li.isBranch = isBranch; }
			if (is.ie6 && li.isLast && li.isBranch && isDefaultExpanded) { addClassName(li, 'ie-expanded-last'); }
			else if (is.ie6 && li.isLast && li.isBranch && !isDefaultExpanded) { addClassName(li, 'ie-collapsed-last'); }
			if (isBranch){
				// build the expand/collapse button
				var link = elem('a.g23toggler',{},elem('img',{'src':'/im/a.gif','height':'10','width':'20','alt':'expand / collapse '}));
				link.onclick = function(){
					var parent = getParent(this,'li');
					if (!hasClassName(parent, 'collapsed')){
						addClassName(parent, 'collapsed');
						if (is.ie6 && parent.isLast && parent.isBranch){
							addClassName(parent, 'ie-collapsed-last');
							removeClassName(parent, 'ie-expanded-last');
						}
					}else {
						removeClassName(parent, 'collapsed');
						if (is.ie6 && parent.isLast && parent.isBranch){
							removeClassName(parent, 'ie-collapsed-last');
							addClassName(parent, 'ie-expanded-last');
						}
					}
				};
				li.getElementsByTagName('div')[0].insertBefore(link, li.getElementsByTagName('div')[0].firstChild);
				if (hasClassName(tree, 'g23check-tree')){
					// build the indicator of how many children are checked
					var countSpan = document.createElement('span');
					countSpan.className = 'g23checked-count';
					for (var c=0;c<li.childNodes.length;c++){
						if (li.childNodes[c].nodeName.toLowerCase()=='ul') { li.sublist = li.childNodes[c]; }
						if (hasClassName(li.childNodes[c], 'g23item-extra-info')) { li.extraInfo = li.childNodes[c]; }
					}
					li.innerWrap.appendChild(countSpan);
					li.countSpan = countSpan;
					countSpan.appendChild(document.createTextNode(' ')); // space, rather than empty string, for safari
					if (window.opera) { countSpan.innerHTML = '&nbsp;'; } // tickle opera
					li.updateCount = function(){
						var count = 0;
						var inputs = reg.getElementsBySelector('input@type="checkbox"', this.sublist);
						for (var b=0; b<inputs.length; b++){ if (inputs[b].checked) { count++; } }
						inputs = null;
						if (this.countSpan){
							if (count  < 1) { this.countSpan.firstChild.data = ' '; if (window.opera) { this.countSpan.innerHTML = '&nbsp;'; } } // safari space, tickle opera
							if (count == 1) { this.countSpan.firstChild.data = '(1 checked item not shown)'; }
							if (count  > 1) { this.countSpan.firstChild.data = '('+count+' checked items not shown)'; }
						}
					}
				}
			}
			li = null;
		}
		if (location.hash) {
			var target = gebi(location.hash.substring(1));
			if (target && new Selector('ul.g23tree li').matchesElement(target)) {
				do {
					removeClassName(target,'collapsed');
					target = getParent(target,'ul.g23tree li');
				} while (target);
			}
		}
		if (hasClassName(tree, 'g23check-tree')){
			var inputs = reg.getElementsBySelector('input@type="checkbox"', tree);
			for (var b=0; b<inputs.length; b++){
				var parent = getParent(inputs[b], 'li');
				parent.checkBox = inputs[b];
				inputs[b].onclick = function(){
					var parent = getParent(this, 'li');
					var subinputs = parent.getElementsByTagName('input');
					for (var c=0;c<subinputs.length;c++){
						subinputs[c].checked = this.checked;
					}
					var subitems = parent.getElementsByTagName('li');
					for (var c=0;c<subitems.length;c++){
						if (typeof subitems[c].updateCount == 'function') { subitems[c].updateCount(); }
					}
					var ancestor = getParent(parent,'li');
					if (!this.checked){
						parent = this;
						while (parent.parentNode){
							parent = parent.parentNode;
							if (parent.checkBox) { parent.checkBox.checked = false; }
						}
					}else if (ancestor && ancestor.checkBox){
						subinputs = ancestor.getElementsByTagName('input');
						var allChecked = true;
						for (var c=0;c<subinputs.length;c++){
							if (subinputs[c].type != 'checkbox') { continue; }
							if (subinputs[c] != parent.parentNode.parentNode.checkBox && !subinputs[c].checked) { allChecked = false; }
						}
						parent.parentNode.parentNode.checkBox.checked = allChecked;
					}
					parent = this;
					while (parent.parentNode){
						parent = parent.parentNode;
						if (typeof parent.updateCount == 'function') { parent.updateCount(); }
					}
					parent = null;
				}
			}
			if (location.hash){
				var target = location.hash.substring(1);
				for (var b=0;b<lis.length;b++){
					var li = lis[b];
					if (li.id == target){
						var inputs = li.getElementsByTagName('input');
						for (var c=0; c<inputs.length; c++){
							if (inputs[c].type != 'checkbox') { continue; }
							inputs[c].checked = true;
						}
						var el = li;
						while (el.parentNode && !hasClassName(el, 'g23tree')){
							if (el.nodeName.toLowerCase() == 'li' && hasClassName(el, 'branch')){
								removeClassName(el, 'collapsed');
								if (is.ie6 && el.isLast && el.isBranch){
									removeClassName(el, 'ie-collapsed-last');
									addClassName(el, 'ie-expanded-last');
								}
							}
							el = el.parentNode;
						}
						var subitems = li.getElementsByTagName('li');
						for (var c=0;c<subitems.length;c++){
							if (hasClassName(subitems[c], 'branch')){
								removeClassName(subitems[c], 'collapsed');
								if (is.ie6 && subitems[c].isLast && subitems[c].isBranch){
									removeClassName(subitems[c], 'ie-collapsed-last');
									addClassName(subitems[c], 'ie-expanded-last');
								}
							}
						}
						inputs = null;
						el = null;
					}
				}
			}
			for (var b=0;b<lis.length;b++){
				var li = lis[b];
				if (typeof li.updateCount == 'function') { li.updateCount(); }
				li = null;
			}
		}
		tree = null;
	}
}

// SETUP -> K4
function sniffModal(){
	var fobj = this;
	if (hasClassName(fobj, "modal-launch")){
		var matches = fobj.className.match(/launch\-id\-([a-z0-9_-]+)/);
		if (!matches) { return; }
		else { fobj.modalId = matches[1]; }
		fobj.onclick = function(e){
			showK4(this.modalId);
			return false;
		};
	}else{
		fobj.onclick = function(e){
			var k4 = this.parentNode;
			while (!hasClassName(k4, 'k4') && k4.parentNode) { k4 = k4.parentNode; }
			if (hasClassName(k4, 'k4') && k4.id) { hideK4(k4.id); }
			return false;
		};
	}
}
function showK4(id){
	var div = document.getElementById(id);
	if (!div) { return; }
	removeClassName(div, "k4hidden");
	var inputs = div.getElementsByTagName("input");
	for (var a=0;a<inputs.length;a++){
		if (inputs[a].type == 'text'){
			inputs[a].focus();
			break;
		}
	}
	if (is.ie6){
		var selects = document.getElementsByTagName("select");
		for (var a=0;a<selects.length;a++){
			addClassName(selects[a], 'k4in-effect');
		}
	}
}
function hideK4(id){
	var div = document.getElementById(id);
	addClassName(div, "k4hidden");
	if (is.ie6){
		var selects = document.getElementsByTagName("select");
		for (var a=0;a<selects.length;a++){
			removeClassName(selects[a], 'k4in-effect');
		}
	}
}

// SETUP -> ROLLOVERS
var preloaderOn = [];
var preloaderOff = [];
var preloaderActive = [];
var activeImg = [];
function sniffRollover(){
	var fobj = this;
	fobj.rsrc = fobj.src;
	preloaderOff[fobj.rsrc] = new Image();
	preloaderOff[fobj.rsrc].src = fobj.rsrc;
	if (hasClassName(fobj, "rollover")){
	  preloaderOn[fobj.rsrc] = new Image();
	  preloaderOn[fobj.rsrc].src = fobj.src.replace(/_off\./,"_on.");
	  fobj.onmouseout = function(){
		  if (activeImg[this.imgGroup] != this){
			  this.src = preloaderOff[this.rsrc].src
		  }
	  };
		fobj.onmouseover = function(){
			if (activeImg[this.imgGroup] != this){
				this.src = preloaderOn[this.rsrc].src
			}
		};
	}
	if (fobj.className.indexOf("active-") > -1){
	  fobj.imgGroup = fobj.className;
	  fobj.imgGroup = fobj.imgGroup.replace(/.*active-(.*).*/,"$1");
	  preloaderActive[fobj.rsrc] = new Image();
	  preloaderActive[fobj.rsrc].src = fobj.src.replace(/_off\./,"_active.");
	  if (fobj.className.indexOf("setactive-") > -1){
		  activeImg[fobj.imgGroup] = fobj;
		  fobj.src = preloaderActive[fobj.rsrc].src;
	  }
	  fobj.onclick = function(){
			if (this.src != preloaderActive[this.rsrc].src){
				this.src = preloaderActive[this.rsrc].src;
				if (activeImg[this.imgGroup]){
					activeImg[this.imgGroup].src = preloaderOff[activeImg[this.imgGroup].rsrc].src;
				}
				activeImg[this.imgGroup] = this;
			}
		};
	}
}

// SETUP -> COUNTRY & LANGUAGE SELECTOR
function sniffSiteSelector(span) {
	var lnks = span.getElementsByTagName('a');
	for (var a=0; a<lnks.length; a++) {
		var lnk = lnks[a];
		if (hasClassName(lnk, 'country-select')) {
			addClassName(lnk,'modal-launch launch-id-country-selector');
			sniffModal.call(lnk);
			var k4 = elem('div',{'class':'k4 k4v1 k4hidden','id':'country-selector'});
			k4.innerHTML = '<div class="k4w1"><div class="k4w2"><div class="k4w3"><div class="k4w4"><div class="k4title"><h2>'
				+'</h2><p class="modal-extra"><a href="" class="modal-close">[X]</a></p></div><div class="k4body">'
				+'</div></div></div></div></div>';
			k4.setTitle=function(txt){this.getElementsByTagName('h2')[0].innerHTML=txt;};
			k4.setBody=function(txt){this.getElementsByTagName('div')[5].innerHTML=txt;};
			document.body.appendChild(k4);
			addEvent(lnk, 'click', function(){
				var thisHref = this.href;
				try {
					getfile(this.href, function(rdata,fvar){
						try {
							var headingText = elemText(getRequestObject('country-data-title',rdata,'h2'));
							var bodyText = getRequestObject('country-data',rdata).innerHTML;
						} catch (ex) { window.location = thisHref; }
						k4.setTitle(headingText);
						k4.setBody(bodyText);
					});
				} catch (e) { window.location = thisHref; }
			});
		} else if (hasClassName(lnk, 'language-select')) {
			var k2 = document.getElementById('languageselector');
			k2.setTitle=function(txt){this.getElementsByTagName('h5')[0].innerHTML=txt;};
			k2.setBody=function(txt){this.getElementsByTagName('div')[3].innerHTML=txt;};
			addEvent(lnk, 'mouseover', function(){
				var thisHref = this.href;
				try {
					getfile(this.href, function(rdata,fvar){
						try {
							var headingText = elemText(getRequestObject('language-data-title',rdata,'h2'));
							var bodyText = getRequestObject('language-data',rdata).innerHTML;
						} catch (ex) {
							k2.setTitle('no data');
							return;
						}
						k2.setTitle(headingText);
						k2.setBody(bodyText);
					});
				} catch (e) { window.location = thisHref; }
			});
		}
	}
}

// SETUP -> GOTO MENU
function sniffGoto(){
	var fobj = this;
	if(hasClassName(fobj, 'showDiv')){
		addEvent(fobj,"change",function(){
				var divID = this.options[this.selectedIndex].value.split('#')[1];
				if (this.currentItem){
						addClassName(this.currentItem,'hidethis');
				}
				if(document.getElementById(divID)){
					this.currentItem = document.getElementById(divID);
					removeClassName(this.currentItem,'hidethis');
				}else{
					this.currentItem = null;
				}
		});
	}else if(this.className.indexOf('hijax-') > -1){
		addEvent(fobj,"change",function(){
			var link = this.options[this.selectedIndex];
			try{
				var id = matchClassName(this,/^hijax-(\S*)/)[1];
				var targetDIV = gebi(id);
			} catch (ex) {
				return;
			}
			if(link.value != "" && link.getAttribute("value")){
				xhr(link.value, function(rdata,obj){
					// succeed
					var el = getElementByIdFromString(rdata, id);
					if (!el) { window.location=link.href; }
					rdata = el.innerHTML;
					hijaxCache[link.value+' '] = rdata;
					targetDIV.innerHTML = rdata;
					reg.rerun(targetDIV);
					if(document.getElementById('linkToPage')){
						document.getElementById('linkToPage').href = link.value;
					}
				},function(){
					// fail
					window.location=link.value;
				});
			}
		});
	}else{
		addEvent(fobj,"change",function(){
			if(this.options[this.selectedIndex].value != "" && this.options[this.selectedIndex].getAttribute("value")){
				document.location = this.options[this.selectedIndex].value;
			}
		});
	}
}

// SETUP -> GOTO UL MENU
function sniffGotoUL(){
	var fobj = this;
	var li = getChildNodesByTagName(fobj,'li');
	var options = "";
	var heading = prevElem(fobj);
	if(heading && hasClassName(heading, 'listTitle')){
		options = options+'<option value="" class="gotoHeading">'+heading.innerHTML+'</option>\n';
	}
	var ulclass = "goto";
	var hi = (this.className.indexOf('hijax-') > -1) ? ' '+matchClassName(this,/^(hijax-\S*)/)[1] : '';
	var form = elem('form',{'action':''});
	fobj.parentNode.insertBefore(form, fobj);
	if(hasClassName(fobj, 'showDiv')){
		ulclass = "showDiv";
		var exdiv = document.createElement('div');
		fobj.parentNode.insertBefore(exdiv, fobj);
	}
	for (var n=0;n<li.length;n++){
		var sel = (li[n].className.indexOf('selected') > -1)? ' selected="selected"' : ''; 
		if (li[n].getElementsByTagName('a')[0]){
			options = options+'<option'+sel+' value="'+li[n].getElementsByTagName('a')[0].href+'">'+li[n].getElementsByTagName('a')[0].innerHTML+'</option>';
		}else if (li[n].innerHTML){
			options = options+'<option'+sel+' value="">'+li[n].innerHTML+'</option>';
		}
		if (hasClassName(fobj, 'showDiv') && li[n].getElementsByTagName('div')[0]){
			exdiv.appendChild(li[n].getElementsByTagName('div')[0]);
		}
	}
	form.innerHTML = '<select class="'+ulclass+hi+'">'+options+'</select>';
	fobj.parentNode.removeChild(fobj);
}

// SETUP -> IMG BOX & IMG ZOOM
var zimg = 1;
function sniffImgbox(){
	var imgdiv = this;
	var img = imgdiv.getElementsByTagName('img')[0];
	imgdiv.style.background  = 'url('+img.src+') no-repeat';
	imgdiv.style.width = img.width+'px';
	imgdiv.style.height = img.height+'px';
	img.style.visibility = 'hidden';

	if (is.ie56 && hasParent(imgdiv,'div','g20w1')){
		var wrapdiv = hasParent(imgdiv,'div','g20w1');
		wrapdiv.style.width = ((img.width * 1) + 12) + 'px';
		addClassName(wrapdiv, 'showcorners');
	}

	if (hasClassName(imgdiv,'imgcorners')){
		imgdiv.innerHTML = '<div class="imgw1"><div class="imgw2"><div class="imgw3"><div class="imgw4" style="width:'+img.width+'px;height:'+img.height+'px">'+imgdiv.innerHTML+'</div></div></div></div>';
	}
	if (hasClassName(imgdiv,'imgzoom')){
		var lgimg = imgdiv.getElementsByTagName('a')[0].href;
		var lgDiv = document.createElement('div');
		lgDiv.className = 'zoomimg k2';
		lgDiv.id = 'zoomimg'+zimg;
		var lgblur = document.createElement('a');
		lgblur.style.backgroundImage = 'none';
		lgblur.onclick = function(){return false;}
		var lgImg = document.createElement('img');
		lgImg.src = lgimg;
		lgblur.appendChild(lgImg);
		lgDiv.appendChild(lgblur);
		imgdiv.appendChild(lgDiv);
		if (hasClassName(imgdiv,'imgright')){
			imgdiv.className = imgdiv.className+' hAlignRight x10';
		}else{
			imgdiv.className = imgdiv.className+' x-10';
		}
		imgdiv.className = imgdiv.className+' vAlignTopBottom y-10 k2over-zoomimg'+zimg;
		sniffK2.call(imgdiv);
		imgdiv.getElementsByTagName('a')[0].onclick = function(){return false;}
		imgdiv.getElementsByTagName('a')[0].style.width = img.width+'px';
		imgdiv.getElementsByTagName('a')[0].style.height = img.height+'px';
		zimg++;
	}
}

// SETUP -> SHARE THIS PAGE
function sniffSharePage() {
	var titleDiv = this;
	if(typeof sharetxt!='undefined'){
		var share_url = getSafelyEncodedString(location.href);
		var share_title = getSafelyEncodedString(document.title);
		var shareThisPage = '\
		<div class="sharepagew1 share-mailto">\
		<table summary="layout" cellpadding="0" cellspacing="0"><tr>\
		<td id="share-mailto"><a href="mailto:?subject='+sharetxt[0]+'{pagetitle}&body='+sharetxt[1]+'%0A%0A'+share_url+'" class="sharelink mailto" title="'+sharetxt[2]+'"></a></td>\
		<td id="share-technorati"><a href="http://www.technorati.com/search/'+share_url+'" class="sharelink technorati" title="'+sharetxt[3]+'"></a></td>\
		<td id="share-delicious"><a href="http://del.icio.us/post?v=4;url='+share_url+';title='+share_title+'" class="sharelink delicious" title="'+sharetxt[4]+'"></a></td>\
		<td id="share-digg"><a href="http://digg.com/submit?phase=2&amp;url='+share_url+'&amp;title='+share_title+'" class="sharelink digg" title="'+sharetxt[5]+'"></a></td>\
		<td id="share-slashdot"><a href="http://slashdot.org/bookmark.pl?title='+share_title+'&amp;url='+share_url+'" class="sharelink slashdot" title="'+sharetxt[6]+'"></a></td>\
		';
		var links = document.getElementsByTagName('link');
		var feed_url = null;
		var feed_title = null;
		var numFeeds = 0;
		for (var a=0; a<links.length; a++) {
			if (''+links[a].rel.toLowerCase() == 'alternate') {
				numFeeds++;
				if (!feed_url) {
					feed_url = links[a].href;
					feed_title = links[a].title;
				}
			}
		}
		if (numFeeds > 1) {
			shareThisPage += '<td id="share-multiple-feeds"><a href="#" title="'+sharetxt[7]+'"></a></td>';
		} else if (numFeeds == 1) {
			shareThisPage += '<td id="share-feed"><a href="'+feed_url+'" class="sharelink feed" title="'+feed_title+'"></a></td>';
		} else {
			shareThisPage += '<td id="share-blank"> </td>';
		}
		shareThisPage += '</tr></table></div>';

		if(hasClassName(document.body,'a0v3')){return;}// not on media shells
		titleDiv.id='sharepage';
		if (is.ie5) { return; }
		if (typeof shareThisPage == 'undefined') { return; }
		share_title = (titleDiv.getElementsByTagName('h1')[0]) ? elemText(titleDiv.getElementsByTagName('h1')[0]) : share_title;
		share_title = share_title.normalize();
		shareThisPage = shareThisPage.replace(/{pagetitle}/,share_title);
		var metas = document.getElementsByTagName('meta');
		for (var a=0;a<metas.length;a++) {
			if (""+metas[a].name.toLowerCase()=='share-this-page' && ""+metas[a].content.toLowerCase()=='no') { return; }
		}
		var shareDiv = document.createElement('div');
		shareDiv.className = 'sharepage';
		titleDiv.appendChild(shareDiv);
		shareDiv.innerHTML = shareThisPage;
		var mult = document.getElementById("share-multiple-feeds");
		if (mult) {
			var lnk = mult.getElementsByTagName('a')[0];
			lnk.titleDiv = titleDiv;
			lnk.mult = mult;
			addEvent(lnk,'click',function(e){
				if (!this.feedListDiv) {
					var links = document.getElementsByTagName('link');
					var feedLinks = [];
					var feedListStr = '<ul class="feedicon icons">';
					for (var a=0; a<links.length; a++) {
						if (''+links[a].rel.toLowerCase() == 'alternate') {
							feedLinks[feedLinks.length] = links[a];
						}
					}
					for (var a=0; a<feedLinks.length; a++) {
						feedListStr += '<li';
						if (a==0) { feedListStr += ' class="first-child"'; }
						else if (a==feedLinks.length - 1) { feedListStr += ' class="last-child"'; }
						feedListStr += '><div><a class="sharelink feed" href="'+feedLinks[a].href+'">'+feedLinks[a].title+'</a></div></li>';
					}
					feedListStr += '</ul><span class="x1"></span><span class="x2"></span>';
					var feedListDiv = elem('div',{'id':'share-feed-list'});
					feedListDiv.innerHTML = feedListStr;
					this.titleDiv.appendChild(feedListDiv);
					this.feedListDiv = feedListDiv;
					addClassName(this.mult,'showing');
					tagOmnitureCustomLinksForSharePage(this.feedListDiv);
				} else {
					if (hasClassName(this.feedListDiv,'hidethis')) {
						removeClassName(this.feedListDiv,'hidethis');
						addClassName(this.mult,'showing');
					} else {
						addClassName(this.feedListDiv,'hidethis');
						removeClassName(this.mult,'showing');
					}
				}
				cancelDefault(e);
			});
		}
		tagOmnitureCustomLinksForSharePage(shareDiv);
	}
}
function tagOmnitureCustomLinksForSharePage(el){
	if (typeof window.s_co!='undefined') {
		var custLink = function(e) {
			var prepend = this.className.replace(/sharelink /,"")+": ";
			s_linkType='o';
			s_linkName=prepend+this.href;
			s_lnk=s_co(this);
			s_gs(s_account);
		}
		var links = el.getElementsByTagName('a');
		for (var a=0; a<links.length; a++) {
			if (!hasClassName(links[a], 'sharelink')) { continue; }
			addEvent(links[a], 'click', custLink);
		}
	}
}

// SETUP -> IMG SWAP
var imgpreload = [];
function sniffImgswap() {
	var link = this;
	if (link.src){
		imgpreload[link.id] = new Image();
		imgpreload[link.id].src = link.src;
	}else{
		link.imgref = link.className.replace(/[^ ]* ?([^ ]+_\d).*/,"$1").split('_');
		link.src = document.getElementById(link.imgref[0]).src.replace(/_\d+\./,"_"+link.imgref[1]+".");
		imgpreload[link.src] = new Image();
		imgpreload[link.src].src = link.src;
		if (!hasClassName(link,'swapOnclick')){
			link.onmouseover = function(){
				document.getElementById(this.imgref[0]).src = imgpreload[this.src].src;
			}
			link.onmouseout = function(){
				document.getElementById(this.imgref[0]).src = imgpreload[this.imgref[0]].src;
			}
			if (!hasClassName(link,'followLink')){
				link.onclick = function(){return false;}
			}
		}else{
			link.onclick = function(){
				imgpreload[this.imgref[0]].src = document.getElementById(this.imgref[0]).src = imgpreload[this.src].src;
				return false;
			}
		}
	}
}

// SETUP -> IMG MULTI SWAP
function sniffMultiswap(){
	var fobj = this;
	if(fobj.src){
		imgpreload[fobj.id] = new Image();
		imgpreload[fobj.id].src = fobj.src;
		if(fobj.className.indexOf('mswap-') > -1){
			var aimg = fobj.className.split('mswap-')[1].split('-')[0].split(' ')[0];
			fobj.src = fobj.src.replace(/[^\/]+(\.....?)$/,aimg+'$1');
		}
	}else{
		fobj.targetid = fobj.className.split('mswap-')[1].split('-')[0].split(' ')[0];
		var prefixid = fobj.targetid.replace(/(.*)\d+?/,'$1');
		fobj.pre = prefixid;
		if(fobj.className.indexOf('mswap-'+fobj.targetid+'-') > -1){
			var imgfile = fobj.className.split('mswap-'+fobj.targetid+'-')[1].split(' ')[0];
		}else{
			var imgfile = fobj.href.replace(/.*\/([^\/]+)?/,'$1').split('.')[0];
		}
		fobj.src = document.getElementById(fobj.targetid).src.replace(/[^\/]+(\.....?)$/,imgfile+'$1');
		imgpreload[fobj] = new Image();
		imgpreload[fobj].src = fobj.src;

		addEvent(fobj,"click",function(e){
			var n = 1;
			while(document.getElementById(this.pre+n)){
				document.getElementById(this.pre+n).src = imgpreload[this.pre+n].src;
				n++;
			}
			document.getElementById(this.targetid).src = this.src;
			if (hasClassName(this,'followLink') || this.target != ''){
			}else{
				cancelDefault(e);
			}
		});
	}
}

// SETUP -> G27
var g27c = 0;
function sniffG27() {
	var fobj = this;
	var pm = (!hasClassName(fobj.getElementsByTagName('div')[0],'hidethis'))?'m':'p';
	var mp = (pm == 'p')?'m':'p';
	var xspace = (rtl)?'&nbsp;&nbsp;':'';
	fobj.getElementsByTagName('h3')[0].innerHTML = '<a href="#" class="toggleObj objects-g27obj'+g27c+'-g27ttp'+g27c+'-g27ttm'+g27c+'"><span id="g27ttp'+g27c+'" class="g27'+pm+'">&nbsp;'+xspace+'</span><span id="g27ttm'+g27c+'" class="hidethis g27'+mp+'">&nbsp;'+xspace+'</span> '+fobj.getElementsByTagName('h3')[0].innerHTML+'</a>';
	fobj.getElementsByTagName('div')[0].id = 'g27obj'+g27c;
	g27c++;
}

// SETUP -> TOGGLE ALL CHECKBOXES IN A TABLE
function sniffToggleAllCheckboxesInTable(){
	var lnk = this;
	var pTab = lnk.parentNode;
	while(pTab.nodeName.toLowerCase()!='table'){pTab=pTab.parentNode;}
	lnk.checkStatus=true;
	lnk.titleSelect='Select All';
	lnk.titleUnselect='Unselect All';
	lnk.title=lnk.titleSelect;
	lnk.img=lnk.getElementsByTagName('img')[0];
	lnk.img.alt=lnk.titleSelect;
	var inputs=pTab.getElementsByTagName('input');
	lnk.checkboxes=[];
	for(var b=0;b<inputs.length;b++){
		if('checkbox'==inputs[b].type){lnk.checkboxes.push(inputs[b]);}
	}
	lnk.onclick=function(){
		for(var c=0;c<this.checkboxes.length;c++){
			this.checkboxes[c].checked=this.checkStatus;
		}
		this.title=(this.checkStatus)?this.titleUnselect:this.titleSelect;
		this.img.alt=(this.checkStatus)?this.titleUnselect:this.titleSelect;
		this.checkStatus=!this.checkStatus;
		return false;
	}
}

// SETUP -> EXPANDIBLE / COLLAPSIBLE PC1
function sniffExpandCollapsePc1(){
	var div = this;
	addClassName(div,'pc1collapsed');
	removeClassName(div,'pc1collapsible');
	var h=div.getElementsByTagName('h2')[0];
	var lnk=elem('a',{'href':'#'},' '+elemText(h));
	var im=elem('img',{'src':'/im/pc1-expand.gif','alt':'','class':'pc1expand-collapse-icon','border':'0'});
	im.srcCollapse='/im/pc1-collapse.gif';
	im.srcExpand=im.src;
	lnk.titleCollapse='Collapse this section';
	lnk.titleExpand='Expand this section';
	lnk.title=lnk.titleExpand;
	lnk.insertBefore(im,lnk.firstChild);
	lnk.im=im;
	lnk.div=div;
	h.innerHTML='';
	h.appendChild(lnk);
	lnk.onclick=function(){
		if(hasClassName(this.div,'pc1expanded')){
			addClassName(this.div,'pc1collapsed');
			removeClassName(this.div,'pc1expanded');
			this.title=this.titleExpand;
			this.im.src=this.im.srcExpand;
		}else{
			addClassName(this.div,'pc1expanded');
			removeClassName(this.div,'pc1collapsed');
			this.title=this.titleCollapse;
			this.im.src=this.im.srcCollapse;
		}
		return false;
	};
	var innerContainer=getElementsByClassName(div, 'cornerBR')[0];
	var p=elem('p',{'class':'pc1expand-note'},' Click the plus icon to expand this section.');
	innerContainer.appendChild(p);
}

// SETUP -> CLASS TOGGLE
function sniffClassTool(){
	var fobj = this;
	var cls = fobj.className.split(' ');
	for (var v=0;v<cls.length;v++){
		if (cls[v].indexOf('cTool-') == 0){
			var objs = cls[v].split('cTool-')[1].split('-');
			if(objs[objs.length - 1].indexOf('RMV') > -1 || objs[objs.length - 1].indexOf('TGL') > -1 || objs[objs.length - 1].indexOf('ADD') > -1){
				var action = "click";
			}else{
				var action = objs[objs.length - 1];
				objs.pop();
			}
			fobj.objs = objs;
			fobj.tid = objs.shift();
			var thistest = fobj.tid;
			if(fobj.tid == "this"){
				fobj.tid = fobj;
			}
			if (action == 'hover' && !is.ie56 && thistest == "this"){
				// then do this hover in the css!
			}else if(action == 'hover'){
				addEvent(fobj,"mouseout",function(e){
					classomatic(this.tid,this.objs);
				});
				var action = "mouseover";
				addEvent(fobj,action,function(e){
					classomatic(this.tid,this.objs);
					if (action == 'click'){
						cancelDefault(e);
					}
				});
			}else{
				addEvent(fobj,action,function(e){
					classomatic(this.tid,this.objs);
					if (action == 'click'){
						cancelDefault(e);
					}
				});
			}
		}
	}
}
function classomatic(id,todo){
	if(!document.getElementById(id)){
		var tobj = id;
	}else{
		var tobj = document.getElementById(id);
	}
	for (var v=0;v<todo.length;v++){
		if(todo[v].indexOf('RMV') == 0){
			removeClassName(tobj, todo[v].substring(3,todo[v].length));
		}else if(todo[v].indexOf('ADD') == 0){
			addClassName(tobj, todo[v].substring(3,todo[v].length));
		}else if(todo[v].indexOf('TGL') == 0){
			if (hasClassName(tobj, todo[v].substring(3,todo[v].length))){
				removeClassName(tobj, todo[v].substring(3,todo[v].length));
			}else if (!hasClassName(tobj, todo[v].substring(3,todo[v].length))){
				addClassName(tobj, todo[v].substring(3,todo[v].length));
			}
		}
	}
}

// SETUP -> GENERIC TOGGLER
function sniffToggler(){
	var fobj = this;
	if(hasClassName(fobj, 'showThis')){
			fobj.toggler = fobj.href.split('#')[1];
			addEvent(fobj,"click",function(e){
				var objRoot = this.toggler.replace(/\d+?/,"");
				var n = 1;
				while(document.getElementById(objRoot+n)){
					if(this.toggler == objRoot+n){
						removeClassName(document.getElementById(this.toggler), 'hidethis');
					}else{
						addClassName(document.getElementById(objRoot+n), 'hidethis');
					}
					n++;
				}
				cancelDefault(e);
			});
	}else{
		var cls = fobj.className.split(' ');
		for (var v=0;v<cls.length;v++){
			if (cls[v].indexOf('objects-') == 0){
				fobj.toggler = cls[v].replace(/objects-/,"");
			}
		}
		addEvent(fobj,"click",function(e){
			var tid = this.toggler.split('-');
			var i;
			for (i in tid){
				if (tid[i].indexOf('ALL') > -1){
					var tAll = [];
					var x = 1;
					while (document.getElementById(tid[i].split('ALL')[0]+x)){
						tAll.push(tid[i].split('ALL')[0]+x);
						x++;
					}
					var ii;
					for (ii in tAll){
						toggler(this,tAll[ii]);
					}
				}else{
					toggler(this,tid[i]);
				}
			}
			cancelDefault(e);
		});
	}
}
function toggler(fobj,id){
	if (hasClassName(document.getElementById(id), 'hidethis') && !hasClassName(fobj, 'hideall') || hasClassName(fobj, 'showall')){
		removeClassName(document.getElementById(id), 'hidethis');
	}else if (!hasClassName(document.getElementById(id), 'hidethis') || hasClassName(fobj, 'hideall')){
		addClassName(document.getElementById(id), 'hidethis');
	}
}

// SETUP -> UL.LISTFADE
var ulid = 0;
function sniffListfade(){
	var fobj = this;
	ulid++;
	var li = fobj.getElementsByTagName('li');
	var x = 0;
	while (li[x]){
		li[x].id = ulid+'ulfade'+(x+1);
		if (x==0){
			addClassName(li[x], 'xfadefirst');
			var p = 'pause5';
			if (fobj.className.indexOf('pause') > -1){
				p = getClassContains(fobj,'pause');
			}
			addClassName(li[x], p);
		}else{
			addClassName(li[x], 'xfade');
		}
		x++;
	}
}

// SETUP -> AJAX INCLUDE
function sniffLoadUrl(){
	var fobj = this;
	if(fobj.href.indexOf('#') > -1){
		var thehref = fobj.href.split('#')[0];
		var id = fobj.href.split('#')[1];
		getfile(thehref,function(rdata,objs){
			if(objs[0]){
				rdata = getRequestObject(objs[0],rdata);
				var wclass = rdata.className;
				rdata = rdata.innerHTML;
			}
			if(objs[1].parentNode.className.indexOf('g32auto') > -1 && objs[0]){
				objs[1].parentNode.className = wclass;
				objs[1].parentNode.innerHTML = rdata;
			}else{
				var insertDIV = elem('div');
				objs[1].parentNode.insertBefore(insertDIV, objs[1]);
				insertDIV.innerHTML = rdata;
				reg.rerun(insertDIV);
				objs[1].parentNode.removeChild(objs[1]);
			}
		},[id,fobj]);
	}
}

// SETUP -> FORM AJAXER
function sniffFormHijax(){
	var fobj = this;
	addEvent(fobj,"submit",function(e){
				var targetDIV = getClassContains(this, "wgform-").split('wgform-')[1];
				if(hasParent(this,targetDIV)){
					var findSubmits = this.getElementsByTagName('input');
					var foundSubmits = [];
					for (i=0; i<findSubmits.length; i++){
						if(findSubmits[i].type == 'submit'){
							foundSubmits.push(findSubmits[i]);
						}
					}
					if (foundSubmits[1]){
						for (i=0; i<foundSubmits.length; i++){
							foundSubmits[i].style.display="none";
						}
						var p=elem('p',{'class':'wgSubmitting'}, ltxt.processingRequest+'...');
						this.appendChild(p);
					}else if(foundSubmits[0]){
							foundSubmits[0].value=ltxt.processingRequest;
							foundSubmits[0].disabled=true;
					}
				}
				getfile(this.action+'?'+getFormData(this), function(rdata,fvar){
				if(rdata.indexOf(targetDIV) > -1){
					rdata = getRequestObject(targetDIV,rdata).innerHTML;
				}
				document.getElementById(targetDIV).innerHTML = rdata;
				reg.rerun(document.getElementById(targetDIV));
			});
		cancelDefault(e);
	});
}

// SETUP -> XFADE
var xfade = [];
var xfadeObj = [];
var xfadeLoop = [];
var xfadeStop = [];
function sniffXfade(){
	var fobj = this;
	if ((fobj.id.substring((fobj.id.length - 1),fobj.id.length) * 1) == 1){
		var transparent = false;
		var bgforie;
		var pause = 10000;
		var id =  fobj.id.substring(0,(fobj.id.length - 1));
		var cls = fobj.className.split(' ');
		for (var v=0;v<cls.length;v++){
			if (cls[v].indexOf("pause") == 0){
				pause = cls[v].replace(/pause(.*)$/,"$1");
				pause = pause * 1000;
			}else if (cls[v].indexOf("transparent") == 0){
				transparent = true;
			}else if (cls[v].indexOf(".jpg") == 0 || cls[v].indexOf(".gif") == 0){
				bgforie = cls[v];
			}
		}
		var xf = 1;
		while (document.getElementById(id+xf)){
			xfadeObj[id+xf] = [document.getElementById(id+xf),0];
			xfadeObj[id+xf][0].onmouseover = function(){if(xfadeStop[id][0] != -1){xfadeStop[id][0] = 0;}}
			xfadeObj[id+xf][0].onmouseout  = function(){if(xfadeStop[id][0] != -1){xfadeStop[id][0] = 1;}}
			// transparent obj
			if (transparent){
				if (is.oldmoz){
					setopacity(xfadeObj[id+xf][0],1);
					xfadeObj[id+xf][0].style.visibility = "hidden";
				}
				if (bgforie && is.iewin){
					xfadeObj[id+xf][0].style.backgroundImage = 'url('+bgforie+')';
				}
				if (is.oldmoz && xf == 1){
					xfadeObj[id+xf][0].style.visibility = "visible";
				}
			}
			xf++;
		}
		xf--;
		xfade[id] = [xf,1,pause];
		if (document.getElementById(id+'Total')){
			document.getElementById(id+'Total').innerHTML = xf;
		}
		if (document.getElementById(id+'Back')){
			document.getElementById(id+'Back').onclick = function(){
				xfadeStop[id] = [-1,-1];
				clearTimeout(xfadeLoop[id]);
				xfader(id);
				return false;
			};
		}
		if (document.getElementById(id+'Next')){
			document.getElementById(id+'Next').onclick = function(){
				xfadeStop[id] = [-1,1];
				clearTimeout(xfadeLoop[id]);
				xfader(id);
				return false;
			};
		}
		xfadeStop[id] = [1,1];
		xfadeLoop[id] = setTimeout('xfader(\''+id+'\')',pause);
	}
}
function xfader(id){
	// define this/next frame
	var nx = xfade[id][1] + xfadeStop[id][1];
	if(nx > xfade[id][0]){
		nx = 1;
	}
	if(nx < 1){
		nx = xfade[id][0];
	}
	var stillfading = false;
	if (xfadeStop[id][0] == 0 && xfadeObj[id+nx][1] != 0){
		var stillfading = true;
	}
	var ox = xfade[id][1];
	if (xfadeObj[id+ox][1] == 0){
		xfadeObj[id+ox][1] = 1;
	}
	if (xfadeStop[id][0] != 0 || stillfading){
		// set up objects
		if (xfadeObj[id+nx][1] == 0){
			if (!is.oldmoz){
				setopacity(xfadeObj[id+nx][0],.1);
			}
			xfadeObj[id+nx][0].style.visibility = "visible";
			xfadeObj[id+ox][0].style.zIndex = 2;
			xfadeObj[id+nx][0].style.zIndex = 10;
		}
		// if skip to next
		if (xfadeStop[id][0] == -1){
			xfadeObj[id+nx][1] = 1;
		}else{
			if (is.safari || is.oldmoz || is.ns6 || is.iemac){
				xfadeObj[id+nx][1] = 1;
			}else{
				xfadeObj[id+nx][1] = xfadeObj[id+nx][1] + .2;
			}
		}

		// set opac
		if (is.anymoz && xfadeObj[id+nx][1] == 1){
			if (!is.oldmoz){
				setopacity(xfadeObj[id+nx][0],.99);
			}
		}else{
			setopacity(xfadeObj[id+nx][0],xfadeObj[id+nx][1]);
		}
		// if fading else, complete and pause
		if (xfadeObj[id+nx][1] < 1){
			setTimeout('xfader(\''+id+'\')',120);
		}else{
			xfade[id][1] = nx;
			xfadeObj[id+ox][0].style.visibility = "hidden";
			xfadeObj[id+ox][1] = 0;
			if (document.getElementById(id+'This')){
				document.getElementById(id+'This').innerHTML = nx;
			}
			if (xfadeStop[id][0] != 0){
				xfadeStop[id] = [1,1];
				xfadeLoop[id] = setTimeout('xfader(\''+id+'\')',xfade[id][2]);
			}
		}
	}
	// if paused
	if(xfadeStop[id][0] == 0){
		clearTimeout(xfadeLoop[id]);
		xfadeLoop[id] = setTimeout('xfader(\''+id+'\')',200);
	}
}

// BUBBLE -> LINK AJAXER
var hijaxCache = {};
function hijaxLink(ev){
	var link = this;
	try{
		var hijaxEl = link;
		while (hijaxEl && !matchClassName(hijaxEl,/^hijax-/)) { hijaxEl = hijaxEl.parentNode; }
		var id = matchClassName(hijaxEl,/^hijax-(\S*)/)[1];
		var targetDIV = gebi(id);
	} catch (ex) {
		return;
	}

	var hstring = link.href+' ';
	if (!hijaxCache[hstring]){
		xhr(link.href, function(rdata,obj){
			// succeed
			var el = getElementByIdFromString(rdata, id);
			if (!el) { window.location=link.href; }
			rdata = el.innerHTML;
			hijaxCache[hstring] = rdata;
			targetDIV.innerHTML = rdata;
			reg.rerun(targetDIV);
			if(document.getElementById('linkToPage')){
				document.getElementById('linkToPage').href = link.href;
			}
		},function(){
			// fail
			window.location=link.href;
		});
		cancelDefault(ev);
	}else{
		targetDIV.innerHTML = hijaxCache[hstring];
		reg.rerun(targetDIV);
		if(document.getElementById('linkToPage')){
			document.getElementById('linkToPage').href = link.href;
		}
		cancelDefault(ev);
	}
};

// BUBBLE -> SPRITE SWAP
function spriteOver(){
	this.style.left = (this.width)/2 * -1 +'px';
}
function spriteOut(){
	this.style.left = 0+'px';
}

// BUBBLE -> HANDLE CLOSING OF FOCUS TRIGGERED OBJECTS
var blurIt=[];
function blurOut(ev){
	var obj = this;
	t = getTarget(ev);
	var b = blurIt;
	blurIt=[];
	for(var i=0; i<b.length; i++){
		if(!hasParent(t,b[i][0])){
			if(b[i][1] == 'hidden'){
				b[i][0].style.visibility='hidden';
			}else if(b[i][1]){
				removeClassName(b[i][0],b[i][1]);
			}else{
				b[i][0].style.display='none';
			}
		}else{
		 	blurIt.push(b[i]);
		}
	}
}

// BUBBLE -> POP UP
function bubblePop(e){
	var link = this;
	if (hasClassName(link, 'media-launch') && !matchClassName(link, '[0-9]+x[0-9]+')){
		addClassName(link,'662x652');
	}
	var popW = '820';
	var popH = '600';
	var param = ['no',0,0,0,0,0,0,'',''];
	var popUrl = link.href;
	if (link.target) { var popTarget = link.target; }
	else { var popTarget = "newpopup"; }
	var cls = link.className.split(' ');
	for (var v=0;v<cls.length;v++){
		if (cls[v].search('[0-9]+x[0-9]+') > -1){
			var f = cls[v].split('x');
			popW = f[0];
			popH = f[1];
		}else if(cls[v].indexOf("name-") == 0){
			var f = cls[v].split('name-');
			popTarget = f[1];
		}else if(cls[v] == "scrolling"){
			var param = ['yes',1,0,0,0,0,0];
		}else if(cls[v] == "full"){
			var param = ['yes',1,1,1,1,1,1];
		}else if(cls[v].indexOf("yes_") == 0 || cls[v].indexOf("no_") == 0){
			var f = cls[v].split('_');
			f[1] = "f"+f[1];
			var param = f[1].split('');
			param[0] = f[0];
		}
		if(link.className.indexOf("centerpop") > 1){
			param[7] = screen.availHeight/2 - popH/2;
			param[8] = screen.availWidth/2 - popW/2;
		}
	}
	openPopup(popUrl,popTarget,popW,popH,param[0],param[1],param[2],param[3],param[4],param[5],param[6],param[7],param[8]);
	cancelDefault(e);
}
function openPopup(url,name,width,height,resizable,scrollbars,menubar,toolbar,location,directories,status,top,left) {
	var tl = (top && left) ? ',top=' + top +',left=' + left : '';
	var popup = window.open(url, name, 'width=' + width + ',height=' + height + ',resizable=' + resizable + ',scrollbars=' + scrollbars	+ ',menubar=' + menubar + ',toolbar=' + toolbar + ',location=' + location + ',directories=' + directories + ',status=' + status+tl);
	popup.focus();
}

// BUBBLE -> AUTOCLEAR
function autoclearFocus(){
	if(this.value == this.defaultValue) this.value='';
}
function autoclearBlur(){
	if(this.value=='') this.value = this.defaultValue;
}

// BUBBLE -> A2
function clickA2(a,menu,link) {
	if(!document.getElementById('a0v2') && window.s_account){
		s_linkType='o';
		s_linkName='Masthead Menu: '+menu;
		s_linkTrackVars = 'prop15,prop16';
		s_prop15=s_pageName;
		s_prop16=link;
		s_lnk=s_co(a);
		s_gs(s_account)
	}
}

// ################################# HELPERS #################################

// " foo  " -> "foo"
if(!String.prototype.strip){
	String.prototype.strip=function(){return this.replace(/^\s+|\s+$/g, "");};
}

// " foo   bar  " -> "foo bar"
if(!String.prototype.normalize){
	String.prototype.normalize=function(sp){
		sp=(!sp && sp!=='')?' ':sp;
		return this.strip().replace(/\s+/g,sp);
	};
}

// HAS PARENT
function hasParent(obj,tag,classname){
	var parent = obj;
	if(classname){
		while (parent = parent.parentNode) {
			if (parent.nodeName.toLowerCase() == tag && hasClassName(parent,classname) || tag == "*" && hasClassName(parent,classname)){
				return parent;
			}
		}
	}else if (typeof tag == 'string') {
		while (parent = parent.parentNode) {
			if (parent.id == tag){
				return parent;
			}
		}
	}else{
		while (parent = parent.parentNode) {
			if (parent == tag){
				return parent;
			}
		}
	}
}

// GET XY OF OBJ
function getXY(obj){
	var o = obj;
	obj.X = obj.Y = 0;
	while(o){
		obj.X = obj.X + o.offsetLeft;
		obj.Y = obj.Y + o.offsetTop;
		o = o.offsetParent;
	}
}

// GET ELEMENTS BY CLASS NAME
function getElementsByClassName(node, className){
	var results = [];
	var els = node.getElementsByTagName("*");
	var len=els.length;
	for(var a=0; a<len; a++){
		if(hasClassName(els[a], className)){
			results.push(els[a]);
		}
	}
	return results;
}

// GET FULL CLASS NAME FROM PARTIAL STRING
function getClassContains(obj,subst){
	var rcl = false;
	var cls = obj.className.split(' ');
	for (var v=0;v<cls.length;v++){
		if (cls[v].indexOf(subst) > -1){
			rcl = cls[v];
		}
	}
	return rcl;
}

// GET CHILD NODES VIA TAG NAME
function getChildNodesByTagName(el, tagName){
	var cn = el.childNodes;
	var nd = [];
	for (var n=0;n<cn.length;n++){
		if(tagName == cn[n].nodeName.toLowerCase()){
			nd.push(cn[n]);
		}
	}
	return nd;
}

// SET OPACITY
function setopacity(id_or_obj,opac){
	if (document.getElementById(id_or_obj)){
		var oobj = document.getElementById(id_or_obj);
	}else if(id_or_obj){
		var oobj = id_or_obj;
	}
	if (oobj){
		if (document.all && !is.op){
			oobj.filters.alpha.opacity = opac * 100;
		}else{
			oobj.style.MozOpacity = opac;
			oobj.style.opacity = opac;
		}
	}
}

// ########################### LEGACY / DEPRECATED ###########################

// A1 LEGACY
var a1hrefs = [];
var a1menus = [];
function oldA1Content(){
	var k;
	for (k in a1hrefs){
		a1[a1hrefs[k][0]] = a1menus[k][1];
	}
	a1hrefs = a1menus = [];
}

// A2 LEGACY
var navmenu = [];
var oldmenu = [];
function popfly(){}
function closefly(){}
function prepmenus(){}
function printmenus(){}
function oldA2Content(){
	var x = 1;
	while(x < 10){
		if(navmenu[x+'.0'] && !a2[navmenu[x+'.0'].split('|')[0]]){
			var xx = 1;
			var li = '';
			while(navmenu[x+'.'+xx]){
				li += '<li><a href="'+navmenu[x+'.'+xx].split('|')[1]+'">'+navmenu[x+'.'+xx].split('|')[0]+'</a></li>\n';
				xx++;
			}
			a2[navmenu[x+'.0'].split('|')[0]] = li;
		}
		if(oldmenu[x+'.0'] && !a2[oldmenu[x+'.0'].split('|')[0]]){
			var xx = 1;
			var li = '';
			while(oldmenu[x+'.'+xx]){
				li += '<li><a href="'+oldmenu[x+'.'+xx].split('|')[1]+'">'+oldmenu[x+'.'+xx].split('|')[0]+'</a></li>\n';
				xx++;
			}
			a2[oldmenu[x+'.0'].split('|')[0]] = li;
		}
		x++;
	}
	navmenu = oldmenu = [];
}
function oldA2TableFix(){
	var x = 1;
	while (document.getElementById('ip'+x)){
		var td = document.getElementById('ip'+x).parentNode;
		td.parentNode.removeChild(td);
		x++;
	}
}


// in case this is still called from somewhere
function domCrawl(domObject,tagList){reg.rerun(domObject);}

// this needs to go away
function catchBodyClicks() {
	if (document.body) {
		addEvent(document.body,'click',function(e){
			if (!e) var e = window.event;
			if (e.target) { var targ = e.target; }
			else if (e.srcElement) { var targ = e.srcElement; }
			if (targ.nodeType == 3) { targ = targ.parentNode; } // we don't need no stinkin' text nodes
			var sel;
			if (typeof bodyClickHandlers != 'undefined') {
				selectors:for (sel in bodyClickHandlers) {
					var el = targ;
					var tries = 0;
					while (el.nodeType == 1) {
						try { if (elementMatchesSelector(el, sel)) { bodyClickHandlers[sel](el, e); break; } }
						catch (e) { continue selectors; }
						if (!el.parentNode || tries > 20) { break; }
						el = el.parentNode;
						tries++;
					}
				}
			}
		});
	}else{
		window.setTimeout('catchBodyClicks()',100);
	}
}
catchBodyClicks();
window.bodyClickHandlers = {};

// this needs to go away
function elementMatchesSelector(el, sel) {
	return new Selector(sel).matchesElement(el);
}

// TODO: DELETE THIS
function sniffLinkHijax(fobj){
	if (fobj.nodeName.toLowerCase() == 'a'){
		var links = new Array(fobj);
	}else if(fobj.getElementsByTagName('a')[0]){
		var links = fobj.getElementsByTagName('a');
	}
	for (i=0; i<links.length; i++){
		links[i].targetDIV = fobj.className.split('hijax-')[1];
		addEvent(links[i],"click",function(e){
			var targetDIV = this.targetDIV;
			var hstring = this.href+' ';
			if (!hijaxCache[hstring]){
				getfile(this.href, function(rdata,fvar){
					if(rdata.indexOf('id="'+targetDIV+'"') > -1){
						rdata = getRequestObject(targetDIV,rdata).innerHTML;
						hijaxCache[hstring] = rdata;
						document.getElementById(targetDIV).innerHTML = rdata;
						reg.rerun(document.getElementById(targetDIV));
					}
				});
				cancelDefault(e);
			}else{
				document.getElementById(targetDIV).innerHTML = hijaxCache[hstring];
				reg.rerun(document.getElementById(targetDIV));
				cancelDefault(e);
			}
		});
	}
};

// this needs to go away
function addOnresizeEvent(func){addEvent(window, 'resize', func);}
