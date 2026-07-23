import React from "react";
import { motion } from "framer-motion";
import { Award, BookOpen, Quote, MapPin, Sparkles } from "lucide-react";
import Reveal from "@/components/Reveal";
import { mostre, premi, pubblicazioni, critiche } from "@/data/extra";

export default function Mostre() {
  return (
    <div data-testid="mostre-page">
      {/* HERO TITLE */}
      <section className="relative pt-40 pb-14 text-center">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, ease: [0.2, 0.7, 0.2, 1] }}>
          <h1 className="font-display text-[2.6rem] sm:text-[4.2rem] lg:text-[5.2rem] leading-none text-[#f3eee7] tracking-[0.05em]">
            MOSTRE <span className="text-gold-bright">&</span> CRITICA
          </h1>
          <div className="divider-ornament my-6"><Sparkles size={16} className="text-gold" /></div>
          <p className="font-display text-gold-bright text-base sm:text-xl tracking-[0.42em] uppercase">di Cortona Francesca</p>
        </motion.div>
      </section>

      {/* CRITICA QUOTES */}
      <section className="max-w-5xl mx-auto px-6 lg:px-10 pb-20" data-testid="critica-section">
        <div className="grid md:grid-cols-3 gap-6">
          {critiche.map((c, i) => (
            <Reveal key={i} delay={i * 0.1}>
              <figure className="h-full p-7 border relative" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
                <Quote size={28} className="text-gold opacity-50" />
                <blockquote className="font-serif-el italic text-xl text-[#d8d2ca] leading-snug mt-4">
                  «{c.testo}»
                </blockquote>
                <figcaption className="font-ui text-[0.68rem] tracking-[0.25em] uppercase text-gold-bright mt-5">
                  — {c.autore}
                </figcaption>
              </figure>
            </Reveal>
          ))}
        </div>
      </section>

      {/* PREMI */}
      <section className="max-w-5xl mx-auto px-6 lg:px-10 pb-20" data-testid="premi-section">
        <Reveal className="flex items-center gap-4 mb-9">
          <Award className="text-gold" size={26} />
          <h2 className="font-display text-3xl text-[#f3eee7]">Premi & Riconoscimenti</h2>
          <span className="flex-1 hairline" />
        </Reveal>
        <div className="grid sm:grid-cols-3 gap-5">
          {premi.map((p, i) => (
            <Reveal key={p.titolo} delay={i * 0.1}>
              <div className="h-full p-7 border text-center" style={{ borderColor: "var(--gold)", background: "linear-gradient(160deg, #1e1a29, #14111c)" }}>
                <span className="font-ui text-[0.68rem] tracking-[0.3em] uppercase text-gold">{p.data}</span>
                <h3 className="font-display text-xl text-gold-bright mt-3 leading-snug tracking-wide2">{p.titolo}</h3>
                <p className="font-serif-el text-lg text-[#a29b93] mt-2">{p.luogo}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* MOSTRE TIMELINE */}
      <section className="max-w-4xl mx-auto px-6 lg:px-10 pb-20" data-testid="mostre-section">
        <Reveal className="flex items-center gap-4 mb-9">
          <MapPin className="text-gold" size={24} />
          <h2 className="font-display text-3xl text-[#f3eee7]">Percorso Espositivo</h2>
          <span className="flex-1 hairline" />
        </Reveal>
        <div className="relative pl-8 border-l" style={{ borderColor: "var(--line)" }}>
          {mostre.map((m, i) => (
            <Reveal key={i} delay={i * 0.06}>
              <div className="relative pb-9 group">
                <span className="absolute -left-[38px] top-1.5 w-3 h-3 rounded-full border-2 transition-colors group-hover:bg-[var(--gold)]"
                      style={{ borderColor: "var(--gold)", background: "var(--bg)" }} />
                <span className="font-ui text-[0.68rem] tracking-[0.3em] uppercase text-gold">{m.data}</span>
                <h3 className="font-display text-xl md:text-2xl text-[#f3eee7] mt-1 tracking-wide2">{m.titolo}</h3>
                <p className="font-serif-el text-lg text-[#c7c0b7] mt-1">{m.luogo}</p>
                <p className="font-ui text-sm text-[#8a837b] mt-0.5">A cura di {m.cura}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* PUBBLICAZIONI */}
      <section className="max-w-4xl mx-auto px-6 lg:px-10 pb-10" data-testid="pubblicazioni-section">
        <Reveal className="flex items-center gap-4 mb-9">
          <BookOpen className="text-gold" size={24} />
          <h2 className="font-display text-3xl text-[#f3eee7]">Pubblicazioni & Stampa</h2>
          <span className="flex-1 hairline" />
        </Reveal>
        <div className="grid sm:grid-cols-2 gap-5">
          {pubblicazioni.map((p, i) => (
            <Reveal key={p.titolo} delay={(i % 2) * 0.08}>
              <div className="h-full p-6 border flex gap-4" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
                <span className="font-display text-gold text-sm shrink-0 pt-1">{p.anno}</span>
                <div>
                  <h3 className="font-display text-lg text-gold-bright tracking-wide2">{p.titolo}</h3>
                  <p className="font-serif-el text-lg text-[#a29b93] mt-1 leading-snug">{p.nota}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>
    </div>
  );
}
