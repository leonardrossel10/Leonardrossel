/* Client fallback: normalize myPhotosV2 entries to use /images/ and remove duplicates */
(function(){
  try{
    var s = localStorage.getItem('myPhotosV2');
    if(!s) return;
    var v = JSON.parse(s);
    if(!Array.isArray(v)) return;
    v = v.map(function(o){
      if(!o || !o.dataUrl) return o;
      o.dataUrl = o.dataUrl.replace(/\.thumbs(\/|\/\.thumbs\/)/g,'/images/');
      o.dataUrl = o.dataUrl.replace(/\.thumbs\//g,'/images/');
      return o;
    });
    var seen = {};
    var out = [];
    v.forEach(function(x){ if(x && x.dataUrl && !seen[x.dataUrl]){ seen[x.dataUrl]=true; out.push(x); } });
    localStorage.setItem('myPhotosV2', JSON.stringify(out));
  }catch(e){}
})();
