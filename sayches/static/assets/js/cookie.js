document.addEventListener("DOMContentLoaded", function(event) { 
  if (localStorage.getItem('scc') != "true")
{
  document.getElementById('cookieAcceptBar').style.display="block";

} 

document.getElementById('cookieAcceptBar').onclick = function(){
   localStorage.setItem('scc','true')
   document.getElementById('cookieAcceptBar').style.display="none";

}
});