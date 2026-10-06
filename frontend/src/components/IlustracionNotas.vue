<template>
  <!-- Una ventana de PowerPoint simplificada: la diapositiva arriba y, debajo, el panel de notas resaltado. -->
  <svg viewBox="0 0 320 210" class="w-full" role="img" aria-label="En PowerPoint, las notas del orador están debajo de la diapositiva">
    <rect x="1" y="1" width="318" height="208" rx="10" fill="var(--c-superficie)" stroke="var(--c-borde)" stroke-width="2" />
    <rect x="1" y="1" width="318" height="22" rx="10" fill="#C43E1C" />
    <rect x="1" y="14" width="318" height="9" fill="#C43E1C" />
    <circle cx="14" cy="12" r="3" fill="#fff" opacity=".7" /><circle cx="24" cy="12" r="3" fill="#fff" opacity=".7" />
    <text x="160" y="16" text-anchor="middle" font-size="9" fill="#fff" font-weight="600">PowerPoint</text>
    <!-- Miniaturas -->
    <rect x="10" y="32" width="46" height="26" rx="2" fill="var(--c-superficie-2)" stroke="var(--c-acento)" stroke-width="1.5" />
    <rect x="10" y="64" width="46" height="26" rx="2" fill="var(--c-superficie-2)" stroke="var(--c-borde)" />
    <rect x="10" y="96" width="46" height="26" rx="2" fill="var(--c-superficie-2)" stroke="var(--c-borde)" />
    <!-- Diapositiva -->
    <rect x="66" y="32" width="244" height="104" rx="3" fill="var(--c-superficie-2)" stroke="var(--c-borde)" />
    <rect x="86" y="54" width="120" height="10" rx="2" fill="var(--c-texto)" opacity=".75" />
    <rect x="86" y="72" width="170" height="6" rx="2" fill="var(--c-suave)" opacity=".5" />
    <rect x="86" y="84" width="150" height="6" rx="2" fill="var(--c-suave)" opacity=".5" />
    <!-- Notas del orador -->
    <rect x="66" y="144" width="244" height="54" rx="3" fill="var(--c-aviso-fondo)" stroke="var(--c-aviso)" stroke-width="2.5" />
    <text x="74" y="158" font-size="8.5" font-weight="700" fill="var(--c-aviso)">NOTAS DEL ORADOR · aquí va el guion</text>
    <rect x="74" y="166" width="220" height="5" rx="2" fill="var(--c-texto)" opacity=".45" />
    <rect x="74" y="176" width="200" height="5" rx="2" fill="var(--c-texto)" opacity=".45" />
    <rect x="74" y="186" width="140" height="5" rx="2" fill="var(--c-texto)" opacity=".45" />
  </svg>
</template>
