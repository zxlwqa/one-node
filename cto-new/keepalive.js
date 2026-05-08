// ==UserScript==
// @name         cto.new keepalive
// @namespace    http://tampermonkey.net/
// @version      2026-04-21
// @description  cto.new keepalive
// @author       vevc
// @match        https://cto.new/business/*/files
// @icon         https://www.google.com/s2/favicons?sz=64&domain=cto.new
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const TARGET_TEXT_SELECTOR = 'body > div:nth-child(8) > main:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)';
    const BUTTON_A_SELECTOR = 'body > div:nth-child(8) > main:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(2)';
    const BUTTON_B_SELECTOR = 'body > div:nth-child(8) > main:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(3)';

    function runTask() {

        const textElement = document.querySelector(TARGET_TEXT_SELECTOR);

        if (!textElement) {
            return;
        }

        const content = textElement.textContent.trim();
        let btnToClick = null;

        if (content === 'docker-compose.yml') {
            btnToClick = document.querySelector(BUTTON_B_SELECTOR);
        } else {
            btnToClick = document.querySelector(BUTTON_A_SELECTOR);
        }

        if (btnToClick) {
            btnToClick.click();
        }
    }

    setInterval(runTask, 30000);

    // 每 4 小时，强制刷新一次网页，防内存泄漏
    // 4小时 = 4 * 60 * 60 * 1000 = 14400000 毫秒
    setTimeout(() => {
        location.reload();
    }, 14400000);

})();
