// ==UserScript==
// @name         Bomb Party Detailed Rules Summary
// @namespace    Violentmonkey Scripts
// @version      0.1.0
// @description  Jklm.fun bomb party more detailed rules!
// @author       Cyrus Yip
// @match        https://*.jklm.fun/games/bombparty/
// @grant        none
// ==/UserScript==

const summary = document.querySelector(".quickRules .summary");
const details = document.createElement("span");
details.className = "bombpartymoredetails";

summary.appendChild(details);

function renderQuickRules() {
  const dictionaryId = rules.dictionaryId.value;
  $(".quickRules .dictionary").textContent = getText(
    rules.dictionaryId.items.find((x) => x.value === dictionaryId).label,
    `dictionaries.${rules.dictionaryId.value}.name`
  );

  const promptDifficultyLevel = rules.promptDifficulty.value;
  const promptDifficulty =
    promptDifficultyLevel === "custom"
      ? rules.customPromptDifficulty.value
      : milestone.dictionaryManifest.promptDifficulties[promptDifficultyLevel];

  $(".quickRules .wordsPerPrompt").textContent =
    promptDifficulty > 0
      ? `min. ${promptDifficulty}`
      : `max. ${-promptDifficulty}`;
  $(
    ".quickRules .bombpartymoredetails"
  ).textContent = ` ${rules.minTurnDuration.value}s,
                    ${rules.maxPromptAge.value} mpa,
                    ${rules.startingLives.value}|${rules.maxLives.value} lives`;
}
var scriptNode = document.createElement("script");
scriptNode.type = "text/javascript";
scriptNode.textContent = renderQuickRules;

document.querySelector("head").appendChild(scriptNode);
