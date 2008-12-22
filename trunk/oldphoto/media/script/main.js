window.Opera =  (window.opera!=null)  || false;
window.IE = (document.all && (!window.Opera))  || false;
window.IE55 = (window.IE && window.createPopup!=null && document.createComment==null) || false;
window.Mozilla = (window.outerWidth && !window.Opera && (window.navigator.product!=null)) || false;
window.gecko = (document.getBoxObjectFor !=null);
window.IE50 = (window.IE && (document.createTextNode!=null) && (window.createPopup==null)  ) || false;
window.IE60= (window.IE && document.createComment!=null ) || false;
window.IE40 = (document.all && !window.IE50 && !window.IE55 && !window.IE60 &&  (window.opera==null) ) || false;
if (!window.gecko) {
 Nifty("div.roundC");
 Nifty("div.roundSC","small");
 Nifty("ul#headeraa A","transparent top");
}
function checkAll(o) 
{
	var value = o.checked;
    var boxes=document.getElementsByTagName("input");
    for(var i=0; i<boxes.length; i++) {
        if (boxes[i].type=='checkbox') {
            boxes[i].checked=value;
        }
    }
}