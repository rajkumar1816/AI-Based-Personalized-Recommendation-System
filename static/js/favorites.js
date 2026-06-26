/* Favorites page actions */
async function removeFavorite(id){
  await fetch('/favorites', {method:'DELETE',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});
  location.reload();
}
