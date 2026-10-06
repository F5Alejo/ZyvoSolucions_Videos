import { reactive } from "vue";

/** Un solo reproductor para todas las muestras de voz: si suena una, se calla la anterior. */
export const muestra = reactive({ url: null as string | null, sonando: false, avance: 0 });

let audio: HTMLAudioElement | null = null;

export function alternarMuestra(url: string) {
  if (muestra.url === url && audio) {
    if (audio.paused) void audio.play();
    else audio.pause();
    return;
  }
  audio?.pause();
  // Si hay otro video o audio sonando en la página, también se calla.
  document.querySelectorAll("video, audio").forEach((m) => (m as HTMLMediaElement).pause());
  audio = new Audio(url);
  muestra.url = url;
  muestra.avance = 0;
  audio.ontimeupdate = () => { if (audio?.duration) muestra.avance = audio.currentTime / audio.duration; };
  audio.onplay = () => (muestra.sonando = true);
  audio.onpause = () => (muestra.sonando = false);
  audio.onended = () => { muestra.sonando = false; muestra.avance = 0; };
  void audio.play().catch(() => (muestra.sonando = false));
}

export function detenerMuestra() {
  audio?.pause();
  muestra.url = null;
  muestra.avance = 0;
}
