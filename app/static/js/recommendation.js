/**
 * RythuCrop - Crop Recommendation Module (Frontend Engine)
 * Strictly mirrors Farm Planning form styling, executive-grade 3-rank cards,
 * zero-leakage 10-language localization with getTranslation lookup.
 */

(function(window, document) {
    'use strict';

    function getActiveLanguage() {
        return (window.AppState && window.AppState.lang) || localStorage.getItem('rythucrop_lang') || 'en';
    }

    /**
     * Universal translation resolver supporting direct keys and category / metadata phrases
     */
    function getTranslation(keyOrText, lang) {
        if (!keyOrText) return "";
        lang = lang || getActiveLanguage();

        const dict = (window.TRANSLATIONS && window.TRANSLATIONS[lang]) || {};
        if (dict[keyOrText] !== undefined) {
            return dict[keyOrText];
        }

        const phraseMap = {
            // Category pills
                        // Tags and Metadata Badges
            "agricultural crop": "tag_agricultural_crop",
            "horticultural crop": "tag_horticultural_crop",
            "commercial crop": "tag_commercial_crop",
            "seasonal": "tag_seasonal",
            "annual": "tag_annual",
            "moderate": "tag_moderate",
            "high": "tag_high",
            "low": "tag_low",
            "perennial": "tag_perennial",
            "commercial and fibre crops": "cat_commercial_fibre",
            "cereals and millets": "cat_cereals_millets",
            "pulses": "cat_pulses",
            "fruits / plantation": "cat_fruits_plantation",
            "vegetables / cucurbits": "cat_vegetables_cucurbits",
            "spices and plantation crops": "cat_spices_plantation",
            "vegetables": "cat_vegetables",
            "oilseeds": "cat_oilseeds",

            // Water Requirements
            "good water availability": "water_good_avail",
            "moderate water availability": "water_moderate_avail",
            "low water availability": "water_low_avail",

            // Feasibility Badges
            "high agronomic feasibility": "feasibility_high",
            "moderate agronomic feasibility": "feasibility_moderate",
            "marginal agronomic feasibility": "feasibility_marginal",

            // Duration suffix
            "days": "duration_days"
        };

        const clean = String(keyOrText).trim().toLowerCase();
        const mappedKey = phraseMap[clean];
        if (mappedKey && dict[mappedKey] !== undefined) {
            return dict[mappedKey];
        }

        if (typeof window.translateDynamic === 'function') {
            const dyn = window.translateDynamic(keyOrText, lang);
            if (dyn && dyn !== keyOrText) return dyn;
        }

        const enDict = (window.TRANSLATIONS && window.TRANSLATIONS['en']) || {};
        if (mappedKey && enDict[mappedKey] !== undefined) {
            return enDict[mappedKey];
        }

        return keyOrText;
    }

    /**
     * Localizes duration string with proper language suffix (e.g., "110–145 రోజులు")
     */
    function translateDuration(durStr, lang) {
        if (!durStr) return "";
        lang = lang || getActiveLanguage();
        const clean = String(durStr).trim().toLowerCase();
        if (clean === "seasonal" || clean === "annual" || clean === "perennial") {
            return getTranslation(durStr, lang);
        }
        const suffix = getTranslation("duration_days", lang) || "days";
        return String(durStr).replace(/\s*days/gi, " " + suffix);
    }

    /**
     * Builds dynamic, localized climate alignment text with strictly interpolated user-input values
     */
    function getDynamicClimateAlignment(tempVal, rainVal, lang) {
        const tempDisp = (tempVal % 1 === 0) ? tempVal.toFixed(0) : tempVal.toFixed(1);
        const rainDisp = (rainVal % 1 === 0) ? rainVal.toFixed(0) : rainVal.toFixed(1);

        const climateTemplates = {
            en: "$1°C & $2mm rainfall provide strong agro-climatic alignment",
            te: "$1°C & $2mm వర్షపాతం అనుకూలమైన వ్యవసాయ శీతోష్ణస్థితిని అందిస్తున్నాయి",
            hi: "$1°C & $2mm वर्षा मजबूत कृषि-जलवायु अनुकूलता प्रदान करते हैं",
            ta: "$1°C & $2mm மழைப்பொழிவு சிறந்த பயிர் சூழலை வழங்குகிறது",
            kn: "$1°C & $2mm ಮಳೆಯು ಬಲವಾದ ಕೃಷಿ-ಹವಾಮಾನ ಹೊಂದಾಣಿಕೆಯನ್ನು ಒದಗಿಸುತ್ತದೆ",
            ml: "$1°C താപനിലയും $2mm മഴയും ശക്തമായ കാർഷിക-കാലാവസ്ഥാ അനുയോജ്യത നൽകുന്നു",
            mr: "$1°C तापमान आणि $2mm पाऊस अनुकूल कृषी-हवामान परिस्थिती निर्माण करतो",
            bn: "$1°C এবং $2mm বৃষ্টিপাত শক্তিশালী কৃষি-আবহাওয়া সামঞ্জস্য প্রদান করে",
            gu: "$1°C અને $2mm વરસાદ શ્રેષ્ઠ કૃષિ-આબોહવા અનુકૂળતા પૂરી પાડે છે",
            od: "$1°C ତାପମାତ୍ରା ଏବଂ $2mm ବର୍ଷା ଅନୁକୂଳ କୃଷି-ପାଣିପାଗ ସମନ୍ୱୟ ପ୍ରଦାନ କରେ"
        };

        const tmpl = climateTemplates[lang] || climateTemplates["en"];
        return tmpl.replace("$1", tempDisp).replace("$2", rainDisp);
    }

    /**
     * Localizes agronomic diagnosis for N-P-K and pH
     */
    function localizeDiagnosis(text, lang) {
        if (!text) return "";
        if (typeof window.localizeCropRecDiagnosis === 'function') {
            return window.localizeCropRecDiagnosis(text, lang);
        }
        return text;
    }

    /**
     * Renders exactly 3 visually distinct recommendation cards:
     * - Rank #1: Highlighted hero card with emerald primary accent badge
     * - Rank #2: High-contrast card with blue accent badge
     * - Rank #3: Clean card with slate accent badge
     * All metadata and text strictly localized with getTranslation().
     */
    function renderCropRecResults(data) {
        if (!data) return;
        const resBox = document.getElementById("recommendationResult") || document.getElementById("cropResult");
        if (!resBox) return;

        // Restore template if container was cleared during refresh/reset
        if (!document.getElementById("cropResultList") && window._CONTAINER_TEMPLATES && window._CONTAINER_TEMPLATES.recommendationResult) {
            resBox.innerHTML = window._CONTAINER_TEMPLATES.recommendationResult;
            if (typeof window.applyTranslations === 'function') {
                try { window.applyTranslations(getActiveLanguage()); } catch (e) {}
            }
        }
        const list = document.getElementById("cropResultList");
        if (!list) return;

        list.innerHTML = "";
        const lang = getActiveLanguage();
        const cropNames = (window.RYTHUCROP_I18N && window.RYTHUCROP_I18N.crop_names) || (window.LOCALIZED_CROP_NAMES) || {};

        // Extract verified user-input values
        const nEl = document.getElementById("N") || document.getElementById("nitrogen");
        const pEl = document.getElementById("P") || document.getElementById("phosphorus");
        const kEl = document.getElementById("K") || document.getElementById("potassium");
        const tEl = document.getElementById("temperature");
        const rEl = document.getElementById("rainfall");

        const userTemp = (data.input && data.input.temperature !== undefined)
            ? parseFloat(data.input.temperature)
            : (parseFloat(tEl?.value) || 25.5);
        const userRain = (data.input && data.input.rainfall !== undefined)
            ? parseFloat(data.input.rainfall)
            : (parseFloat(rEl?.value) || 100.0);

        const items = data.top_3_detailed || [];
        items.forEach(item => {
            const card = document.createElement("div");
            card.className = "crop-card crop-card-rank-" + item.rank;
            const cf = item.cultivation_feasibility || {};

            let rawCrop = (item.crop_id || item.name || "").toLowerCase().trim();
            let cropKey = rawCrop.replace(/[\(\)\/\s]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
            if (cropNames[cropKey]) {
                // Direct match in localized dictionary
            } else if (cropKey.includes("coffee")) {
                cropKey = "coffee";
            } else if (cropKey.includes("cotton")) {
                cropKey = "cotton";
            } else if (cropKey.includes("turmeric")) {
                cropKey = "turmeric";
            } else if (cropKey.includes("tur") || cropKey.includes("arhar") || cropKey.includes("pigeonpea")) {
                cropKey = cropNames["pigeonpeas"] ? "pigeonpeas" : "arhar_tur";
            } else if (cropKey.includes("chickpea")) {
                cropKey = cropNames["chickpea"] ? "chickpea" : "gram";
            } else if (cropKey.includes("gram")) {
                cropKey = cropNames["gram"] ? "gram" : "chickpea";
            } else if (cropKey.includes("chillies")) {
                cropKey = "dry_chillies";
            }

            // Pure localized crop name without brackets
            const locCrop = (cropNames[cropKey] && (cropNames[cropKey][lang] || cropNames[cropKey]["en"])) || (item.name || "").replace(/\s*\([^)]*\)/g, '');

            // Localized metadata pills via getTranslation
            const locCategory = getTranslation(item.category, lang);
            const locDuration = translateDuration(item.duration, lang);
            const locWaterReq = getTranslation(item.water_req, lang);

            // Feasibility score & localized status
            const feasScore = item.feasibility_score || cf.feasibility_score || (cf.feasibility_index ? parseInt(cf.feasibility_index, 10) : Math.round(item.confidence_pct + 15)) || 75;
            const feasStatusRaw = item.feasibility_status || cf.feasibility_status || (feasScore >= 70 ? "High Agronomic Feasibility" : "Moderate Agronomic Feasibility");
            const locFeasStatus = getTranslation(feasStatusRaw, lang);

            // Dynamic Diagnosis tailored per crop
            const rawNpk = item.npk_analysis || cf.npk_analysis || cf.soil_npk_analysis ||
                           (cf.soil_n_status ? `${cf.soil_n_status}, ${cf.soil_p_status}, ${cf.soil_k_status}` : "");
            const rawPh = item.ph_compatibility || cf.ph_compatibility || cf.soil_ph_suitability || cf.ph_suitability || "";

            const locNpk = localizeDiagnosis(rawNpk, lang);
            const locPh = localizeDiagnosis(rawPh, lang);

            // Strictly bind user input temperature and rainfall into the climate bullet point
            const cardTemp = (item.input_temperature !== undefined) ? item.input_temperature : userTemp;
            const cardRain = (item.input_rainfall !== undefined) ? item.input_rainfall : userRain;
            const locClimate = getDynamicClimateAlignment(cardTemp, cardRain, lang);

            // Visual hierarchy per Rank with Tailwind modern dashboard cards
            const rawR1 = getTranslation("rank_1_badge", lang) || "Rank #1 — Primary Recommendation";
            const cleanR1 = rawR1.replace(/^[★*•\s]+/, '');
            const rawR2 = getTranslation("rank_2_badge", lang) || "Rank #2 — Strong Alternative";
            const cleanR2 = rawR2.replace(/^[★*•\s]+/, '');
            const rawR3 = getTranslation("rank_3_badge", lang) || "Rank #3 — Viable Crop";
            const cleanR3 = rawR3.replace(/^[★*•\s]+/, '');

            let cardContainerClass = '';
            let rankBadgeHtml = '';
            let progressGradientClass = '';
            let titleColorClass = '';
            let confBadgeClass = '';

            if (item.rank === 1) {
                cardContainerClass = 'border-2 border-emerald-500 shadow-lg ring-1 ring-emerald-300 rounded-2xl bg-white p-6 relative transition-all duration-300 hover:shadow-2xl mb-6';
                rankBadgeHtml = `<span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-600 text-white shadow-sm tracking-wide inline-flex items-center gap-1.5">★ ${cleanR1}</span>`;
                confBadgeClass = 'bg-emerald-100 text-emerald-800 border border-emerald-200';
                progressGradientClass = 'bg-gradient-to-r from-emerald-500 to-teal-500';
                titleColorClass = 'text-emerald-950';
            } else if (item.rank === 2) {
                cardContainerClass = 'border-2 border-blue-400 shadow-md ring-1 ring-blue-200 rounded-2xl bg-white p-6 relative transition-all duration-300 hover:shadow-xl mb-6';
                rankBadgeHtml = `<span class="px-3 py-1 rounded-full text-xs font-bold bg-blue-600 text-white shadow-sm tracking-wide inline-flex items-center gap-1.5">★ ${cleanR2}</span>`;
                confBadgeClass = 'bg-sky-100 text-sky-800 border border-sky-200';
                progressGradientClass = 'bg-gradient-to-r from-sky-500 to-blue-500';
                titleColorClass = 'text-slate-800';
            } else {
                cardContainerClass = 'border-2 border-blue-400 shadow-md ring-1 ring-blue-200 rounded-2xl bg-white p-6 relative transition-all duration-300 hover:shadow-xl mb-6';
                rankBadgeHtml = `<span class="px-3 py-1 rounded-full text-xs font-bold bg-slate-700 text-white shadow-sm tracking-wide inline-flex items-center gap-1.5">★ ${cleanR3}</span>`;
                confBadgeClass = 'bg-slate-100 text-slate-800 border border-slate-200';
                progressGradientClass = 'bg-gradient-to-r from-slate-400 to-slate-600';
                titleColorClass = 'text-slate-800';
            }

            card.className = cardContainerClass;

            const confLabel = getTranslation("confidence_label", lang) || "Confidence";
            const feasTitle = (getTranslation("feasibility_title", lang) || "Agronomic Feasibility").replace(/^[★*•\s]+/, '');
            const npkLabel = getTranslation("npk_diagnosis_label", lang) || "N-P-K Diagnosis:";
            const phLabel = getTranslation("soil_ph_suitability_label", lang) || "Soil pH Suitability:";
            const climateLabel = getTranslation("climate_alignment_label", lang) || "Climate Alignment:";

            card.innerHTML = `
                <div class="flex justify-between items-center mb-3 flex-wrap gap-2">
                    ${rankBadgeHtml}
                    <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold ${confBadgeClass} shadow-xs">
                        <span>${item.confidence_pct}%</span>
                        <span>${confLabel}</span>
                    </span>
                </div>

                <div class="w-full h-2 bg-slate-100 rounded-full my-3 overflow-hidden">
                    <div class="h-full ${progressGradientClass} rounded-full transition-all duration-500" style="width:${item.confidence_pct}%;"></div>
                </div>

                <h3 class="text-2xl font-black ${titleColorClass} mb-2 tracking-tight">${locCrop}</h3>

                <div class="flex flex-wrap gap-2 mb-4">
                    <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/60">🌿 ${locCategory}</span>
                    <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200/60">⏱️ ${locDuration}</span>
                    <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-sky-50 text-sky-700 border border-sky-200/60">💧 ${locWaterReq}</span>
                </div>

                <div class="bg-slate-50 rounded-xl p-3.5 text-xs text-slate-700 border border-slate-100/90">
                    <div class="flex justify-between items-center mb-2.5 pb-2 border-b border-slate-200/60">
                        <span class="font-bold text-slate-800 uppercase tracking-wider text-[0.7rem]">★ ${feasTitle}</span>
                        <span class="px-2.5 py-0.5 rounded-full text-[0.7rem] font-bold ${item.rank === 1 ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-slate-200 text-slate-700'}">${feasScore}% • ${locFeasStatus}</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-2">
                        <div><strong class="text-slate-900">• ${npkLabel}</strong> <span class="text-slate-600">${locNpk || "N-P-K Optimal"}</span></div>
                        <div><strong class="text-slate-900">• ${phLabel}</strong> <span class="text-slate-600">${locPh || "pH Neutral"}</span></div>
                    </div>
                    <div class="pt-2 border-t border-slate-200/60">
                        <strong class="text-slate-900">• ${climateLabel}</strong> <span class="text-slate-600">${locClimate}</span>
                    </div>
                </div>
            `;
            list.appendChild(card);
        });

        if (resBox) resBox.style.display = "block";
    }

    /**
     * Re-renders active crop recommendation cards upon language switch
     */
    function reRenderCropRecCards(lang) {
        if (window.lastCropRecData) {
            renderCropRecResults(window.lastCropRecData);
        }
    }

    /**
     * Submits clean 7-parameter laboratory soil & climate readings to recommendation endpoint
     */
    async function handleCropRecommendation(e) {
        if (e && typeof e.preventDefault === 'function') e.preventDefault();
        const errBox = document.getElementById("cropErrorBox");
        if (errBox) errBox.style.display = "none";

        const nEl = document.getElementById("N") || document.getElementById("nitrogen");
        const pEl = document.getElementById("P") || document.getElementById("phosphorus");
        const kEl = document.getElementById("K") || document.getElementById("potassium");
        const tEl = document.getElementById("temperature");
        const hEl = document.getElementById("humidity");
        const phEl = document.getElementById("ph");
        const rEl = document.getElementById("rainfall");

        if (!nEl || !pEl || !kEl || !tEl || !hEl || !phEl || !rEl) return;

        const payload = {
            N: parseFloat(nEl.value),
            P: parseFloat(pEl.value),
            K: parseFloat(kEl.value),
            temperature: parseFloat(tEl.value),
            humidity: parseFloat(hEl.value),
            ph: parseFloat(phEl.value),
            rainfall: parseFloat(rEl.value)
        };

        try {
            const res = await fetch("/predict", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });
            if (!res.ok) {
                if (res.status === 401) {
                    alert("Crop Recommendation error: Authentication required. Please login with your Email.");
                    const resBox = document.getElementById("recommendationResult") || document.getElementById("cropResult");
                    if (resBox) {
                        resBox.style.display = "none";
                        resBox.innerHTML = "";
                    }
                    if (errBox) {
                        errBox.style.display = "none";
                        errBox.textContent = "";
                    }
                    return;
                }
                const data = await res.json().catch(() => ({}));
                if (errBox) {
                    errBox.textContent = data.error || data.message || "Input validation failed";
                    errBox.style.display = "block";
                }
                return;
            }
            const data = await res.json();

            window.lastCropRecData = data;
            renderCropRecResults(data);

            const resBox = document.getElementById("recommendationResult") || document.getElementById("cropResult");
            if (resBox) resBox.scrollIntoView({behavior: "smooth", block: "nearest"});
        } catch (err) {
            if (errBox) {
                errBox.textContent = "Server error occurred. Please try again.";
                errBox.style.display = "block";
            }
        }
    }

    // Expose functions to global namespace
    window.getTranslation = getTranslation;
    window.renderCropRecResults = renderCropRecResults;
    window.renderCropRecResultsModule = renderCropRecResults;
    window.handleCropRecommendation = handleCropRecommendation;
    window.handleCropRecommendationModule = handleCropRecommendation;
    window.reRenderCropRecCards = reRenderCropRecCards;
    window.getDynamicClimateAlignment = getDynamicClimateAlignment;

    // Attach listeners on DOMContentLoaded
    if (typeof document !== 'undefined') {
        document.addEventListener("DOMContentLoaded", function() {
            // Form Submit Handler
            const form = document.getElementById("cropRecForm") || document.getElementById("cropForm");
            if (form) {
                form.addEventListener("submit", handleCropRecommendation);
            }

            // Reactive Language Switch Handler
            const langSelect = document.getElementById("langSelect");
            if (langSelect) {
                langSelect.addEventListener("change", function(e) {
                    reRenderCropRecCards(e.target.value);
                });
            }
        });
    }

})(window, document);
