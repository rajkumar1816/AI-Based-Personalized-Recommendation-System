/* History page actions */
async function clearHistory(){
  await fetch('/history', {method:'DELETE'});
  location.reload();
}

async function exportHistory(){
  window.location='/history/export';
}
