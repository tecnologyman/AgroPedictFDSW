/* =========================================
   ANIMACIONES AGROPREDICT - animations.js
   Controla y activa las animaciones
   ========================================= */

class AgroPredict Animations {
  constructor() {
    this.animateOnScroll = this.animateOnScroll.bind(this);
    this.countUpNumbers = this.countUpNumbers.bind(this);
    this.init();
  }

  /**
   * Inicializar observadores de animaciones
   */
  init() {
    // Esperar a que el DOM esté listo
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupObservers());
    } else {
      this.setupObservers();
    }
  }

  /**
   * Configurar Intersection Observer para animar elementos al entrar en viewport
   */
  setupObservers() {
    // Observer para elementos que deben animarse al entrar en vista
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          this.animateElement(entry.target);
          // Solo animar una vez
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observar todos los elementos que deben animarse
    const elementsToAnimate = document.querySelectorAll(
      '[data-animate], .metric-card, .result-card, .form-group, .chart-container, .prediction-row'
    );

    elementsToAnimate.forEach((element) => {
      observer.observe(element);
    });

    // Animar elementos de dashboard inmediatamente al cargar
    this.animateDashboard();

    // Observar números para contador
    this.observeCounters();
  }

  /**
   * Animar elemento cuando entra en vista
   */
  animateElement(element) {
    // Si el elemento tiene atributo data-animate, usar ese
    if (element.hasAttribute('data-animate')) {
      const animation = element.getAttribute('data-animate');
      element.classList.add(animation);
    } else {
      // Sino, usar clases CSS predefinidas
      if (element.classList.contains('metric-card')) {
        element.classList.add('animate-fade-in-up');
      } else if (element.classList.contains('result-card')) {
        element.classList.add('animate-scale-in');
      } else if (element.classList.contains('form-group')) {
        element.classList.add('animate-fade-in-left');
      } else if (element.classList.contains('chart-container')) {
        element.classList.add('animate-fade-in-up');
      } else if (element.classList.contains('prediction-row')) {
        element.classList.add('animate-fade-in-left');
      }
    }
  }

  /**
   * Animar dashboard al cargar la página
   */
  animateDashboard() {
    // Animar tarjetas de métricas
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach((card, index) => {
      setTimeout(() => {
        card.classList.add('animate-fade-in-up');
      }, index * 100);
    });

    // Animar gráficos
    const charts = document.querySelectorAll('.chart-container');
    charts.forEach((chart, index) => {
      setTimeout(() => {
        chart.classList.add('animate-fade-in-up');
      }, 400 + index * 100);
    });

    // Animar números contadores
    setTimeout(() => {
      this.animateNumbers();
    }, 300);
  }

  /**
   * Animar números con contador (cuenta progresiva)
   */
  animateNumbers() {
    const numberElements = document.querySelectorAll('[data-counter]');

    numberElements.forEach((element) => {
      const target = parseFloat(element.getAttribute('data-counter'));
      const duration = 1500; // 1.5 segundos
      const startTime = Date.now();
      const startValue = 0;

      const animate = () => {
        const currentTime = Date.now();
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing función (ease-out)
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const currentValue = startValue + (target - startValue) * easeProgress;

        // Determinar formato según el valor
        if (target > 100) {
          element.textContent = currentValue.toFixed(0);
        } else if (target > 10) {
          element.textContent = currentValue.toFixed(1);
        } else {
          element.textContent = currentValue.toFixed(2);
        }

        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };

      animate();
    });
  }

  /**
   * Observar contadores que aparecen al hacer scroll
   */
  observeCounters() {
    const observerOptions = {
      threshold: 0.5,
      rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
          this.countUpNumber(entry.target);
          entry.target.classList.add('counted');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observar elementos con atributo data-counter
    const counterElements = document.querySelectorAll('[data-counter]');
    counterElements.forEach((element) => {
      observer.observe(element);
    });
  }

  /**
   * Contador individual para un elemento
   */
  countUpNumber(element) {
    const target = parseFloat(element.getAttribute('data-counter'));
    const duration = 1200;
    const startTime = Date.now();

    const animate = () => {
      const currentTime = Date.now();
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing: ease-out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const currentValue = easeProgress * target;

      // Formato según tipo de número
      if (target > 100) {
        element.textContent = currentValue.toFixed(0);
      } else if (target > 10) {
        element.textContent = currentValue.toFixed(1);
      } else {
        element.textContent = currentValue.toFixed(2);
      }

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        element.textContent = element.getAttribute('data-counter');
      }
    };

    animate();
  }

  /**
   * Animar barra de progreso
   */
  animateProgressBars() {
    const progressBars = document.querySelectorAll('[data-progress]');

    progressBars.forEach((bar) => {
      const targetProgress = parseFloat(bar.getAttribute('data-progress'));
      const progressFill = bar.querySelector('.progress-bar-fill');

      if (progressFill) {
        setTimeout(() => {
          progressFill.style.width = targetProgress + '%';
          progressFill.classList.add('animate-progress');
        }, 100);
      }
    });
  }

  /**
   * Activar efecto de carga (spinner)
   */
  showLoadingState(element) {
    element.classList.add('animate-spin', 'loading-spinner');
    element.style.cursor = 'not-allowed';
    element.disabled = true;
  }

  /**
   * Desactivar efecto de carga
   */
  hideLoadingState(element) {
    element.classList.remove('animate-spin', 'loading-spinner');
    element.style.cursor = 'pointer';
    element.disabled = false;
  }

  /**
   * Animar validación de formulario
   */
  animateFormSuccess(formElement) {
    formElement.classList.add('form-success');
    setTimeout(() => {
      formElement.classList.remove('form-success');
    }, 500);
  }

  /**
   * Animar error de formulario
   */
  animateFormError(inputElement) {
    inputElement.classList.add('form-error');
    setTimeout(() => {
      inputElement.classList.remove('form-error');
    }, 1000);
  }

  /**
   * Animar resultado exitoso
   */
  animateResultCard(resultCard) {
    resultCard.classList.add('animate-scale-in');
    
    // Animar números dentro de la tarjeta
    const numberElements = resultCard.querySelectorAll('[data-counter]');
    numberElements.forEach((element) => {
      setTimeout(() => {
        this.countUpNumber(element);
      }, 300);
    });
  }

  /**
   * Pulse animación en elemento
   */
  pulse(element, times = 2) {
    element.classList.add('animate-pulse');
    
    setTimeout(() => {
      element.classList.remove('animate-pulse');
    }, times * 1000);
  }

  /**
   * Glow animación en elemento
   */
  glow(element, duration = 2000) {
    element.classList.add('animate-glow');
    
    setTimeout(() => {
      element.classList.remove('animate-glow');
    }, duration);
  }

  /**
   * Bounce animación en elemento
   */
  bounce(element, times = 3) {
    element.classList.add('animate-bounce');
    
    setTimeout(() => {
      element.classList.remove('animate-bounce');
    }, times * 1000);
  }

  /**
   * Animar formulario de entrada de datos
   */
  animateFormFields() {
    const formGroups = document.querySelectorAll('.form-group');

    formGroups.forEach((group, index) => {
      group.style.animationDelay = `${index * 0.1}s`;
      group.classList.add('animate-fade-in-left');
    });
  }

  /**
   * Limpiar todas las animaciones de un elemento
   */
  clearAnimations(element) {
    element.classList.remove(
      'animate-fade-in',
      'animate-fade-in-up',
      'animate-fade-in-left',
      'animate-fade-in-right',
      'animate-scale-in',
      'animate-slide-in-up',
      'animate-slide-in-down',
      'animate-pulse',
      'animate-glow',
      'animate-bounce',
      'animate-spin',
      'form-success',
      'form-error'
    );
  }
}

// Inicializar cuando el DOM esté listo
let agroAnimations;

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    agroAnimations = new AgroPredict Animations();
  });
} else {
  agroAnimations = new AgroPredict Animations();
}

// Exportar para uso en otros scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AgroPredict Animations;
}
function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `toast-notification toast-${type}`;
    notification.innerHTML = `
        <div class="toast-content">
            <span>${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Evento del botón guardar
document.addEventListener('DOMContentLoaded', function() {
    const btnGuardar = document.getElementById('btn-guardar');
    
    if (btnGuardar) {
        btnGuardar.addEventListener('click', function() {
            const año = document.querySelector('input[name="año"]')?.value;
            const rendimiento = document.querySelector('input[name="rendimiento_real"]')?.value;
            
            if (!año || !rendimiento) {
                showNotification('❌ Por favor completa todos los campos.', 'error');
                return;
            }
            
            // FormData
            const formData = new FormData();
            formData.append('año', año);
            formData.append('rendimiento_real', rendimiento);
            formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
            
            // Enviar
            fetch('/predicciones/api-ingresar-datos-historicos/', {
                method: 'POST',
                body: JSON.stringify({
                    prediccion_id: window.prediccionId, // Debes pasar esto desde el HTML
                    datos_historicos: [{
                        ano: parseInt(año),
                        rendimiento_real: parseFloat(rendimiento)
                    }]
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                showNotification(data.message, data.type);
                
                // Si éxito, limpiar inputs
                if (data.success) {
                    document.querySelector('input[name="año"]').value = '';
                    document.querySelector('input[name="rendimiento_real"]').value = '';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('❌ Error de conexión', 'error');
            });
        });
    }
});

// Función helper para obtener CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}