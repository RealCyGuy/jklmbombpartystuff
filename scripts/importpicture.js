javascript:(function() {
  try {
    settings.picture = prompt("Paste profilepicture.py's copy stuff.");;
    saveSettings();
    alert("Probably saved successfully!");
  } catch (e) {
    alert(e);
  }
})();