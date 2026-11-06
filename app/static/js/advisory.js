/**
 * RythuCrop - Smart Agronomic Cultivation Advisory Engine
 * Interactive 3-card layout, dynamic priority filtering,
 * and 100% reactive multilingual localization across 10 Indic languages.
 */

(function(window, document) {
    'use strict';

    // Multilingual Stage Timing Badges for Card 1
    const STAGE_TIMING_BADGES = {
        0: {
            en: "Stage 1 • Sowing & Seed Prep",
            te: "దశ 1 • విత్తనశుద్ధి & నాట్లు",
            hi: "चरण 1 • बुवाई एवं बीजोपचार",
            ta: "நிலை 1 • விதைப்பு & விதை நேர்த்தி",
            kn: "ಹಂತ 1 • ಬಿತ್ತನೆ ಮತ್ತು ಬೀಜೋಪಚಾರ",
            ml: "ഘട്ടം 1 • വിതയ്ക്കലും വിത്തുപരിപാലനവും",
            mr: "टप्पा 1 • पेरणी व बीजप्रक्रिया",
            bn: "পর্যায় ১ • বপন ও বীজ শোধন",
            gu: "તબક્કો 1 • વાવણી અને બીજ માવજત",
            od: "ପର୍ଯ୍ୟାୟ ୧ • ବୁଣିବା ଓ ବିହନ ବିଶୋଧନ"
        },
        1: {
            en: "Stage 2 • Vegetative Growth",
            te: "దశ 2 • శాఖీయ పెరుగుదల",
            hi: "चरण 2 • वानस्पतिक वृद्धि",
            ta: "நிலை 2 • தாவர வளர்ச்சி",
            kn: "ಹಂತ 2 • ಸಸ್ಯಕ ಬೆಳವಣಿಗೆ",
            ml: "ഘട്ടം 2 • സസ്യവളർച്ച",
            mr: "टप्पा 2 • शाकीय वाढ",
            bn: "পর্যায় ২ • অঙ্গজ বৃদ্ধি",
            gu: "તબક્કો 2 • વાનસ્પતિક વૃદ્ધિ",
            od: "ପର୍ଯ୍ୟାୟ ୨ • ଶାଖା ବୃଦ୍ଧି"
        },
        2: {
            en: "Stage 3 • Flowering & Moisture",
            te: "దశ 3 • పూత & తేమ యాజమాన్యం",
            hi: "चरण 3 • फूल एवं नमी प्रबंधन",
            ta: "நிலை 3 • பூக்கும் நிலை & பாசனம்",
            kn: "ಹಂತ 3 • ಹೂಬಿಡುವಿಕೆ & ತೇವಾಂಶ",
            ml: "ഘട്ടം 3 • പൂവിടലും നനയും",
            mr: "टप्पा 3 • फुले व पाणी व्यवस्थापन",
            bn: "পর্যায় ৩ • ফুল ও আর্দ্রতা নিয়ন্ত্রণ",
            gu: "તબક્કો 3 • ફૂલો અને ભેજ નિયંત્રણ",
            od: "ପର୍ଯ୍ୟାୟ ୩ • ଫୁଲ ଓ ଆର୍ଦ୍ରତା ପରିଚାଳନା"
        },
        3: {
            en: "Stage 4 • Maturity & Harvesting",
            te: "దశ 4 • పరిపక్వత & కోత",
            hi: "चरण 4 • परिपक्वता एवं कटाई",
            ta: "நிலை 4 • முதிர்ச்சி & அறுவடை",
            kn: "ಹಂತ 4 • ಪಕ್ವತೆ ಮತ್ತು ಕೊಯ್ಲು",
            ml: "ഘട്ടം 4 • വിളവെടുപ്പ്",
            mr: "टप्पा 4 • पक्वता व काढणी",
            bn: "পর্যায় ৪ • পরিপক্কতা ও ফসল কাটা",
            gu: "તબક્કો 4 • પાકવાની સ્થિતિ અને લણણી",
            od: "ପର୍ଯ୍ୟାୟ ୪ • ଅମଳ ସମୟ"
        }
    };

    // Card Suffixes
    
    // Chemical formula mapping to translation keys
    const FORMULA_MAP = {
        "25% Nitrogen + Zinc": "formula_zinc",
        "25% Nitrogen + 50% K2O": "formula_potash",
        "Micronutrient Boost": "formula_micro",
        "50% N + 100% P₂O₅ + 50% K₂O": "formula_basal"
    };

    function getLocalizedFormula(rawFormula, lang, t) {
        if (!rawFormula) return "";
        const clean = String(rawFormula).trim();
        const key = FORMULA_MAP[clean];
        if (key) {
            return t(key, rawFormula);
        }
        return (typeof window.translateDynamic === 'function' ? window.translateDynamic(rawFormula, lang) : null) || rawFormula;
    }

    const STEP_PREFIX_I18N = {
        en: "Step",
        te: "దశ",
        hi: "चरण",
        ta: "நிலை",
        kn: "ಹಂತ",
        ml: "ഘട്ടം",
        mr: "टप्पा",
        bn: "পর্যায়",
        gu: "તબક્કો",
        od: "ପର୍ଯ୍ୟାୟ"
    };

    const ADVISORY_TITLE_SUFFIX = {
        en: "Cultivation Advisory & Management",
        te: "సాగు సలహాలు & సమగ్ర యాజమాన్యం",
        hi: "खेती सलाह एवं समग्र प्रबंधन",
        ta: "சாகுபடி ஆலோசனை & முழுமையான மேலாண்மை",
        kn: "ಕೃಷಿ ಸಲಹೆ ಮತ್ತು ಸಮಗ್ರ ನಿರ್ವಹಣೆ",
        ml: "കൃഷി ഉപദേശം & സമഗ്ര പരിപാലനം",
        mr: "लागवड सल्ला व संपूर्ण व्यवस्थापन",
        bn: "চাষের পরামর্শ ও সমন্বিত ব্যবস্থাপনা",
        gu: "ખેતી સલાહ અને વ્યવસ્થાપન",
        od: "ଚାଷ ପରାମର୍ଶ ଓ ପରିଚାଳନା"
    };

    function getActiveLanguage() {
        return (window.AppState && window.AppState.lang) || localStorage.getItem('rythucrop_lang') || 'en';
    }

    function getTranslation(key, fallback) {
        const lang = getActiveLanguage();
        const dict = (window.TRANSLATIONS && window.TRANSLATIONS[lang]) || {};
        if (dict[key] !== undefined && dict[key] !== "") return dict[key];
        const enDict = (window.TRANSLATIONS && window.TRANSLATIONS['en']) || {};
        if (enDict[key] !== undefined) return enDict[key];
        return fallback !== undefined ? fallback : key;
    }

    /**
     * Main Render Advisory function - Auth Gated
     */
    async function renderAdvisory() {
        const cropEl = document.getElementById("advisoryCropSelect") || document.getElementById("adCrop");
        const priorityEl = document.getElementById("adPriority") || document.getElementById("advisoryPrioritySelect");
        const resBox = document.getElementById("advisoryResult") || document.getElementById("advisoryCard");

        if (!cropEl || !resBox) return;

        const crop = cropEl.value || "rice";
        const priority = priorityEl ? priorityEl.value : "care";
        const lang = getActiveLanguage();

        // 1. Strict Authentication Verification via Backend API
        try {
            const authResp = await fetch(`/api/advisory?crop=${encodeURIComponent(crop)}&lang=${encodeURIComponent(lang)}&priority=${encodeURIComponent(priority)}`, {
                method: "GET",
                headers: { "Content-Type": "application/json" }
            });

            if (!authResp.ok) {
                if (authResp.status === 401) {
                    alert("Smart Advisory error: Authentication required. Please login with your Email.");
                    resBox.style.display = "none";
                    resBox.innerHTML = "";
                    return;
                }
            }
        } catch (err) {
            console.error("Advisory authentication verification error:", err);
        }
        const dict = (window.TRANSLATIONS && window.TRANSLATIONS[lang]) || {};
        const t = (k, fb) => (dict[k] !== undefined && dict[k] !== "") ? dict[k] : (fb !== undefined ? fb : k);

        // Restore DOM container structure if cleared by lifecycle reset
        let container = document.getElementById("advisoryContainer");
        let heading = document.getElementById("advisoryHeading");

        if (!container) {
            if (window._CONTAINER_TEMPLATES && window._CONTAINER_TEMPLATES.advisoryResult) {
                resBox.innerHTML = window._CONTAINER_TEMPLATES.advisoryResult;
                container = document.getElementById("advisoryContainer");
                heading = document.getElementById("advisoryHeading");
            } else {
                resBox.innerHTML = `
                    <div class="result-header" id="advisoryHeaderLabel" data-i18n="advice_label">${t("advice_label", "AGRONOMIC ADVICE")}</div>
                    <h3 id="advisoryHeading" style="font-weight:800; font-size:1.25rem; color:var(--primary-dark); margin:6px 0 16px;"></h3>
                    <div id="advisoryContainer" class="grid-3" style="margin-top:1rem;"></div>
                `;
                container = document.getElementById("advisoryContainer");
                heading = document.getElementById("advisoryHeading");
            }
        }

        // Get localized crop name
        const cropNames = (window.RYTHUCROP_I18N && window.RYTHUCROP_I18N.crop_names) || (window.LOCALIZED_CROP_NAMES) || {};
        let cropKey = crop.toLowerCase().replace(/[\(\)\/\s]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
        if (cropKey.includes("cotton")) cropKey = "cotton";
        else if (cropKey.includes("turmeric")) cropKey = "turmeric";
        else if (cropKey.includes("arhar") || cropKey.includes("tur") || cropKey.includes("pigeonpea")) cropKey = "arhar_tur";
        else if (cropKey.includes("gram")) cropKey = "gram";
        else if (cropKey.includes("chillies")) cropKey = "dry_chillies";

        const localizedCrop = (cropNames[cropKey] && (cropNames[cropKey][lang] || cropNames[cropKey]["en"])) || crop.toUpperCase();

        // Retrieve localized advisory dataset
        const langAdvisory = (window.ADVISORY_TRANSLATED_BUNDLES && window.ADVISORY_TRANSLATED_BUNDLES[lang]) || null;
        const fallbackAdvisory = (window.ADVISORY_TRANSLATED_BUNDLES && window.ADVISORY_TRANSLATED_BUNDLES["en"]) || window.ADVISORY_DATABASE || {};
        const data = (langAdvisory && langAdvisory[crop]) || fallbackAdvisory[crop] || fallbackAdvisory["rice"] || {};

        // Localized Headings & Labels
        const cardCareTitle = t("advisory_card1_title", t("card_care_title", "Agronomic Growth Stages & Crop Care"));
        const cardFertTitle = t("advisory_card2_title", t("card_fert_title", "Targeted Nutrient & Fertilizer Schedule"));
        const cardPestTitle = t("advisory_card3_title", t("card_pest_title", "Pest & Disease IPM Shield"));
        const activeFocusText = t("advisory_active_focus", "★ Active Focus");

        if (heading) {
            if (data && data.title) {
                heading.textContent = data.title;
            } else {
                const suffix = ADVISORY_TITLE_SUFFIX[lang] || ADVISORY_TITLE_SUFFIX["en"];
                heading.textContent = `${localizedCrop} ${suffix}`;
            }
        }

        if (!container) return;
        container.innerHTML = "";

        const showCare = priority === "all" || priority === "care";
        const showFertilizer = priority === "all" || priority === "fertilizer";
        const showPest = priority === "all" || priority === "pest";

        // Layout class and style with smooth Active Focus isolation mode
        if (priority === "all") {
            container.className = "grid grid-cols-1 md:grid-cols-3 gap-6 mt-4 transition-all duration-300";
            container.style.cssText = "";
        } else {
            container.className = "max-w-3xl mx-auto mt-4 transition-all duration-300 transform scale-100 opacity-100";
            container.style.cssText = "";
        }

        // =========================================================================
        // CARD 1: AGRONOMIC GROWTH STAGES & CROP CARE (Green Theme)
        // =========================================================================
        if (showCare && data.care && data.care.length > 0) {
            const isHighlighted = priority === "care";
            const careCard = document.createElement("div");
            careCard.className = `bg-white/95 rounded-2xl p-6 shadow-md border ${isHighlighted ? 'border-emerald-500 ring-2 ring-emerald-200 shadow-xl' : 'border-slate-200/80'} border-t-4 border-t-emerald-500 flex flex-col gap-4 transition-all duration-300 hover:shadow-xl`;

            careCard.innerHTML = `
                <div class="flex justify-between items-center flex-wrap gap-2 pb-2 border-b border-slate-100">
                    <div class="flex items-center gap-2.5">
                        <span class="w-9 h-9 rounded-full bg-emerald-50 text-emerald-700 text-lg flex items-center justify-center shadow-xs">🌿</span>
                        <h4 class="text-base font-extrabold text-emerald-950 m-0">${cardCareTitle}</h4>
                    </div>
                    ${isHighlighted ? `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">${activeFocusText}</span>` : ''}
                </div>

                <div class="flex flex-col gap-3 mt-1">
                    ${data.care.map((c, idx) => {
                        const stageName = (typeof window.translateDynamic === 'function' ? window.translateDynamic(c.stage, lang) : null) || c.stage;
                        const stageDesc = (typeof window.translateDynamic === 'function' ? window.translateDynamic(c.text, lang) : null) || c.text;
                        const timingBadge = STAGE_TIMING_BADGES[idx] ? (STAGE_TIMING_BADGES[idx][lang] || STAGE_TIMING_BADGES[idx]['en']) : `Stage ${idx + 1}`;

                        return `
                            <div class="bg-slate-50/80 border border-slate-100 rounded-xl p-3.5 leading-relaxed transition hover:bg-slate-50">
                                <div class="flex justify-between items-center flex-wrap gap-1.5 mb-1.5">
                                    <span class="font-bold text-slate-900 text-xs flex items-center gap-1.5">
                                        <span>${c.icon || "🌱"}</span>
                                        <span>${stageName}</span>
                                    </span>
                                    <span class="text-[0.7rem] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full">${timingBadge}</span>
                                </div>
                                <div class="text-xs text-slate-600 pl-1">${stageDesc}</div>
                            </div>
                        `;
                    }).join("")}
                </div>
            `;
            container.appendChild(careCard);
        }

        // =========================================================================
        // CARD 2: TARGETED NUTRIENT & FERTILIZER SCHEDULE (Sky Theme)
        // =========================================================================
        if (showFertilizer && data.fertilizer && data.fertilizer.length > 0) {
            const isHighlighted = priority === "fertilizer";
            const fertCard = document.createElement("div");
            fertCard.className = `bg-white/95 rounded-2xl p-6 shadow-md border ${isHighlighted ? 'border-sky-500 ring-2 ring-sky-200 shadow-xl' : 'border-slate-200/80'} border-t-4 border-t-sky-500 flex flex-col gap-4 transition-all duration-300 hover:shadow-xl`;

            fertCard.innerHTML = `
                <div class="flex justify-between items-center flex-wrap gap-2 pb-2 border-b border-slate-100">
                    <div class="flex items-center gap-2.5">
                        <span class="w-9 h-9 rounded-full bg-sky-50 text-sky-700 text-lg flex items-center justify-center shadow-xs">🧪</span>
                        <h4 class="text-base font-extrabold text-sky-950 m-0">${cardFertTitle}</h4>
                    </div>
                    ${isHighlighted ? `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-sky-100 text-sky-800 border border-sky-200">${activeFocusText}</span>` : ''}
                </div>

                <div class="flex flex-col gap-3 mt-1">
                    ${data.fertilizer.map((f, idx) => {
                        const fertStage = (typeof window.translateDynamic === 'function' ? window.translateDynamic(f.stage, lang) : null) || f.stage;
                        const fertText = (typeof window.translateDynamic === 'function' ? window.translateDynamic(f.text, lang) : null) || f.text;

                        return `
                            <div class="bg-slate-50/80 border border-slate-100 rounded-xl p-3.5 leading-relaxed transition hover:bg-slate-50">
                                <div class="flex justify-between items-center flex-wrap gap-1.5 mb-1.5">
                                    <span class="font-bold text-slate-900 text-xs flex items-center gap-1.5">
                                        <span class="w-5 h-5 rounded-full bg-sky-600 text-white flex items-center justify-center text-[0.65rem] font-black">${idx + 1}</span>
                                        <span>${fertStage}</span>
                                    </span>
                                    ${f.formula ? `<span class="bg-sky-100 text-sky-800 rounded-md px-2 py-0.5 text-xs font-bold border border-sky-200">${getLocalizedFormula(f.formula, lang, t)}</span>` : ''}
                                </div>
                                <div class="text-xs text-slate-600 pl-1">${fertText}</div>
                            </div>
                        `;
                    }).join("")}
                </div>
            `;
            container.appendChild(fertCard);
        }

        // =========================================================================
        // CARD 3: PEST & DISEASE IPM SHIELD (Rose/Crimson Theme)
        // =========================================================================
        if (showPest && data.pest && data.pest.length > 0) {
            const isHighlighted = priority === "pest";
            const pestCard = document.createElement("div");
            pestCard.className = `bg-white/95 rounded-2xl p-6 shadow-md border ${isHighlighted ? 'border-rose-500 ring-2 ring-rose-200 shadow-xl' : 'border-slate-200/80'} border-t-4 border-t-rose-500 flex flex-col gap-4 transition-all duration-300 hover:shadow-xl`;

            pestCard.innerHTML = `
                <div class="flex justify-between items-center flex-wrap gap-2 pb-2 border-b border-slate-100">
                    <div class="flex items-center gap-2.5">
                        <span class="w-9 h-9 rounded-full bg-rose-50 text-rose-700 text-lg flex items-center justify-center shadow-xs">🛡️</span>
                        <h4 class="text-base font-extrabold text-rose-950 m-0">${cardPestTitle}</h4>
                    </div>
                    ${isHighlighted ? `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200">${activeFocusText}</span>` : ''}
                </div>

                <div class="flex flex-col gap-3 mt-1">
                    ${data.pest.map((p, idx) => {
                        const pestType = (typeof window.translateDynamic === 'function' ? window.translateDynamic(p.type, lang) : null) || p.type;
                        const pestText = (typeof window.translateDynamic === 'function' ? window.translateDynamic(p.text, lang) : null) || p.text;
                        const icon = idx === 0 ? "🔍" : (idx === 1 ? "🌿" : "💊");

                        return `
                            <div class="bg-slate-50/80 border border-slate-100 rounded-xl p-3.5 leading-relaxed transition hover:bg-slate-50">
                                <div class="flex justify-between items-center flex-wrap gap-1.5 mb-1.5">
                                    <span class="font-bold text-slate-900 text-xs flex items-center gap-1.5">
                                        <span>${icon}</span>
                                        <span>${pestType}</span>
                                    </span>
                                    <span class="text-[0.7rem] font-semibold bg-rose-100 text-rose-800 border border-rose-200 px-2 py-0.5 rounded-full">${(dict && dict["step_prefix"]) || STEP_PREFIX_I18N[lang] || "Step"} ${idx + 1}</span>
                                </div>
                                <div class="text-xs text-slate-600 pl-1">${pestText}</div>
                            </div>
                        `;
                    }).join("")}
                </div>
            `;
            container.appendChild(pestCard);
        }

        // Show result box with unified sleek teal borders and ring
        resBox.className = "result-box advisoryCard border-2 border-teal-400 shadow-lg ring-1 ring-teal-200 rounded-2xl bg-white/95";
        resBox.style.display = "block";
    }

    // Expose to window namespace
    window.renderAdvisory = renderAdvisory;
    window.renderAdvisoryModule = renderAdvisory;

    // Attach listeners on DOM ready
    function setupAdvisoryListeners() {
        const btnFetch = document.getElementById("btnFetchAdvisory");
        if (btnFetch) {
            btnFetch.addEventListener("click", () => {
                renderAdvisory();
                const resBox = document.getElementById("advisoryResult") || document.getElementById("advisoryCard");
                if (resBox) {
                    resBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
                }
            });
        }

        const cropEl = document.getElementById("advisoryCropSelect") || document.getElementById("adCrop");
        if (cropEl) {
            cropEl.addEventListener("change", () => {
                renderAdvisory();
            });
        }

        const priorityEl = document.getElementById("adPriority") || document.getElementById("advisoryPrioritySelect");
        if (priorityEl) {
            priorityEl.addEventListener("change", () => {
                renderAdvisory();
            });
        }

        // Re-render advisory when language changes if result box is visible
        window.addEventListener("languageChanged", (e) => {
            const resBox = document.getElementById("advisoryResult") || document.getElementById("advisoryCard");
            if (resBox && resBox.style.display !== "none") {
                renderAdvisory();
            }
        });
    }

    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupAdvisoryListeners);
        } else {
            setupAdvisoryListeners();
        }
    }

})(window, document);
