javascript:(function() {
  let picture = prompt("Paste profilepicture.py's copy stuff.", "");
  if (picture == null) {
    return;
  }
  try {
    settings.picture = picture;
    saveSettings();
    alert("Probably saved successfully!");
  } catch (e) {
    alert(e);
  }
})();