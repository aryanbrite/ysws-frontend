(() => {
      const field = document.querySelector('.petal-field');
      const PETAL_PATH = 'M12 2.2C10.5 2.2 9 3 8 4.5C7 6 6.8 8 7.5 9.8C8.2 11.5 9.8 13.5 12 14.8C14.2 13.5 15.8 11.5 16.5 9.8C17.2 8 17 6 16 4.5C15 3 13.5 2.2 12 2.2ZM12 3.2C11.7 3.8 11.3 4.6 11.3 5.3C11.3 5.7 11.4 6.1 11.6 6.4C11.8 6.6 12.2 6.6 12.4 6.4C12.6 6.1 12.7 5.7 12.7 5.3C12.7 4.6 12.3 3.8 12 3.2Z';
      const rand = (min, max) => min + Math.random() * (max - min);
      const colors = ['#FFF5FA', '#FFE8F2', '#FFD4E5', '#FFB7C5'];

      function makePetal(index) {
        const el = document.createElement('div');
        el.className = 'petal';
        const size = rand(12, 42);
        const startX = rand(-12, 112);
        const drift = rand(-28, 28);
        const duration = rand(8, 18);
        const delay = rand(-duration, 0);
        const opacity = rand(.28, .88);
        const blur = rand(0, 1.5);
        const gradientId = `gradient-${index}`;

        el.style.cssText = `
          --size:${size.toFixed(2)}px;
          --x0:${startX.toFixed(2)}vw;
          --x1:${(startX + drift).toFixed(2)}vw;
          --duration:${duration.toFixed(2)}s;
          --delay:${delay.toFixed(2)}s;
          --opacity:${opacity.toFixed(3)};
          --blur:${blur.toFixed(2)}px;
          --rz0:${rand(-180, 180).toFixed(1)}deg;
          --rz1:${rand(540, 1260).toFixed(1)}deg;
          --ry0:${rand(-180, 180).toFixed(1)}deg;
          --ry1:${rand(720, 1800).toFixed(1)}deg;
        `;

        el.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="${colors[0]}" />
                <stop offset="25%" stop-color="${colors[1]}" />
                <stop offset="50%" stop-color="${colors[2]}" />
                <stop offset="75%" stop-color="${colors[3]}" />
                <stop offset="100%" stop-color="${colors[3]}" />
              </linearGradient>
            </defs>
            <path d="${PETAL_PATH}" fill="url(#${gradientId})" opacity=".95" />
          </svg>`;
        field.appendChild(el);
      }

      const count = Math.min(42, Math.max(24, Math.round(innerWidth / 24)));
      for (let i = 0; i < count; i++) makePetal(i);

      // Rebuild density on a major viewport change without interrupting ordinary resizing.
      let lastWidth = innerWidth;
      addEventListener('resize', () => {
        if (Math.abs(innerWidth - lastWidth) > 180) {
          lastWidth = innerWidth;
          field.replaceChildren();
          const nextCount = Math.min(42, Math.max(24, Math.round(innerWidth / 24)));
          for (let i = 0; i < nextCount; i++) makePetal(i);
        }
      });
    })();

    