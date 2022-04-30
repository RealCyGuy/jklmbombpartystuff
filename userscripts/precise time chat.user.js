// ==UserScript==
// @name         Bomb Party Precise Time Chat
// @namespace    Violentmonkey Scripts
// @version      0.1.0
// @description  Show seconds in bomb party chat.
// @author       Cyrus Yip
// @match        https://jklm.fun/*
// @grant        none
// ==/UserScript==
if (window.location.pathname != "/") {
  function appendToChat(authorProfile, text) {
    if (
      authorProfile != null &&
      !authorProfile.isBroadcast &&
      mutedPeerIds.includes(authorProfile.peerId)
    )
      return;
    if (sidebar.hidden) sidebarToggleButton.classList.add("unread");

    chatMessageCount++;
    if (chatMessageCount > maxChatMessageCount)
      chatLog.removeChild($(chatLog, "div:not(.newMessages)"));

    const isScrolledToBottom =
      chatLog.scrollHeight - chatLog.clientHeight - chatLog.scrollTop < 10;
    const logEntry = $make("div", chatLog, {
      className: authorProfile == null ? "system" : "",
    });

    const time = new Date();
    const hoursMinutes =
      `0${time.getHours()}`.slice(-2) + ":" + `0${time.getMinutes()}`.slice(-2) + ":" + `0${time.getSeconds()}`.slice(-2);
    $make("span", logEntry, { className: "time", textContent: hoursMinutes });
    $makeText(" ", logEntry);

    if (authorProfile != null && authorProfile.isBroadcast) {
      const broadcast = $make("span", logEntry, { className: "broadcast" });
      $make("span", broadcast, {
        className: "author",
        textContent: authorProfile.nickname,
      });
      $makeText(": " + text, broadcast);
    } else {
      if (authorProfile != null) {
        const roles = authorProfile.roles != null ? authorProfile.roles : [];
        const badgesElt = $make("span", logEntry, { className: "badges" });
        for (const role of roles) {
          const badge = badgesByRole[role];
          $make("span", badgesElt, {
            textContent: badge.icon,
            title: badge.text,
          });
        }

        const service =
          authorProfile.auth != null ? authorProfile.auth.service : "guest";
        const link = $make("a", logEntry, {
          className: `author ${service}`,
          dataset: { peerId: authorProfile.peerId },
          href: "#",
        });
        $make("img", link, {
          className: "service",
          src: `/images/auth/${service}.png`,
          alt: "",
        });
        $makeText(authorProfile.nickname, link);
        $setTooltip(link, getAuthTextFromProfile(authorProfile));

        $makeText(": ", logEntry);
      }

      $make("span", logEntry, { className: "text", textContent: text });
    }

    if (
      document.visibilityState === "hidden" ||
      sidebar.hidden ||
      chatTab.hidden
    ) {
      if (unreadMarkerElt.hidden) {
        chatLog.insertBefore(unreadMarkerElt, logEntry);
        $show(unreadMarkerElt);
      }
    }

    if (isScrolledToBottom) chatLog.scrollTop = chatLog.scrollHeight;
  }

  var scriptNode = document.createElement("script");
  scriptNode.type = "text/javascript";
  scriptNode.textContent = appendToChat;

  document.querySelector("head").appendChild(scriptNode);
}
