import React, { createContext, useContext, useState, useCallback } from "react";
import { T, LANGS } from "@/i18n/t";

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(() => {
    try { return localStorage.getItem("lang") || "it"; } catch { return "it"; }
  });
  const setLang = useCallback((l) => {
    setLangState(l);
    try { localStorage.setItem("lang", l); } catch {}
    document.documentElement.lang = l;
  }, []);
  const t = T[lang] || T.it;
  return (
    <LanguageContext.Provider value={{ lang, setLang, t, langs: LANGS }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLang() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLang must be used within LanguageProvider");
  return ctx;
}
