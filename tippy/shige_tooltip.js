document.addEventListener('DOMContentLoaded', function() {
    const selectors = ['.shige_day_farm'];

    selectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(element => {
            const cardCount = parseInt(element.getAttribute('data-card-count'), 10);
            let backgroundColor;

            if (cardCount === 0) {
                backgroundColor = 'rgba(128, 128, 128, 0.9)';
            } else if (cardCount > 30) {
                const blueValue = Math.min(200, Math.max(0, Math.floor((cardCount / 100) * 200)));
                backgroundColor = `rgba(${0 + blueValue}, 100, 255, 0.9)`;
            } else {
                const blueValue = Math.min(100, Math.max(0, Math.floor((cardCount / 30) * 100)));
                backgroundColor = `rgba(0, ${200 - blueValue}, 255, 0.9)`;
            }

            tippy(element, {
                content: element.getAttribute('data-tippy-content'),
                allowHTML: true,
                animation: 'scale',
                theme: 'custom',
                onShow(instance) {
                    const tippyBox = instance.popper.querySelector('.tippy-box');
                    tippyBox.style.backgroundColor = backgroundColor;
                    const tippyArrow = instance.popper.querySelector('.tippy-arrow');
                    tippyArrow.style.color = backgroundColor;
                }
            });
        });
    });
});