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

            let cropKey = (item.crop_id || item.name || "").toLowerCase().replace(/[\(\)\/\s]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
            if (cropKey.includes("cotton")) cropKey = "cotton";
            else if (cropKey.includes("turmeric")) cropKey = "turmeric";
            else if (cropKey.includes("tur") || cropKey.includes("arhar") || cropKey.includes("pigeonpea")) cropKey = "arhar_tur";
            else if (cropKey.includes("gram") || cropKey.includes("chickpea")) cropKey = "gram";
            else if (cropKey.includes("chillies")) cropKey = "dry_chillies";

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

            // Visual hierarchy per Rank
            let badgeHtml = '';
            let cardInlineStyle = '';
            let progressGradient = '';
            let titleColor = '';

            const rawR1 = getTranslation("rank_1_badge", lang) || "Rank #1 — Primary Recommendation";
            const cleanR1 = rawR1.replace(/^[★*•\s]+/, '');
            const rawR2 = getTranslation("rank_2_badge", lang) || "Rank #2 — Strong Alternative";
            const cleanR2 = rawR2.replace(/^[★*•\s]+/, '');
            const rawR3 = getTranslation("rank_3_badge", lang) || "Rank #3 — Viable Crop";
            const cleanR3 = rawR3.replace(/^[★*•\s]+/, '');

            if (item.rank === 1) {
                badgeHtml = `<span style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: #ffffff; padding: 5px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 3px 10px rgba(16, 185, 129, 0.35);">★ ${cleanR1}</span>`;
                cardInlineStyle = 'border: 2px solid #10b981; background: linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%); border-radius: 18px; padding: 24px; position: relative; box-shadow: 0 12px 28px -6px rgba(16, 185, 129, 0.18), 0 6px 12px -4px rgba(16, 185, 129, 0.08); transition: transform 0.25s ease, box-shadow 0.25s ease;';
                progressGradient = 'linear-gradient(90deg, #10b981, #059669)';
                titleColor = '#064e3b';
            } else if (item.rank === 2) {
                badgeHtml = `<span style="background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); color: #ffffff; padding: 5px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 750; letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.25);">★ ${cleanR2}</span>`;
                cardInlineStyle = 'border: 1.5px solid #cbd5e1; background: #ffffff; border-radius: 18px; padding: 22px; position: relative; box-shadow: 0 4px 18px rgba(15, 23, 42, 0.06); transition: transform 0.25s ease, box-shadow 0.25s ease;';
                progressGradient = 'linear-gradient(90deg, #0284c7, #38bdf8)';
                titleColor = '#1e293b';
            } else {
                badgeHtml = `<span style="background: linear-gradient(135deg, #475569 0%, #64748b 100%); color: #ffffff; padding: 5px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 750; letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 3px 10px rgba(71, 85, 105, 0.25);">★ ${cleanR3}</span>`;
                cardInlineStyle = 'border: 1.5px solid #cbd5e1; background: #ffffff; border-radius: 18px; padding: 22px; position: relative; box-shadow: 0 4px 18px rgba(15, 23, 42, 0.06); transition: transform 0.25s ease, box-shadow 0.25s ease;';
                progressGradient = 'linear-gradient(90deg, #475569, #64748b)';
                titleColor = '#1e293b';
            }

            card.style.cssText = cardInlineStyle;

            const confLabel = getTranslation("confidence_label", lang) || "Confidence";
            const feasTitle = (getTranslation("feasibility_title", lang) || "Agronomic Feasibility").replace(/^[★*•\s]+/, '');
            const npkLabel = getTranslation("npk_diagnosis_label", lang) || "N-P-K Diagnosis:";
            const phLabel = getTranslation("soil_ph_suitability_label", lang) || "Soil pH Suitability:";
            const climateLabel = getTranslation("climate_alignment_label", lang) || "Climate Alignment:";

            card.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    ${badgeHtml}
                    <span style="font-weight:800; font-size:1rem; color:${item.rank === 1 ? '#059669' : (item.rank === 2 ? '#0284c7' : '#475569')};">${item.confidence_pct}% ${confLabel}</span>
                </div>
                <div style="width:100%; height:6px; background:#e2e8f0; border-radius:10px; margin-bottom:14px; overflow:hidden;">
                    <div style="width:${item.confidence_pct}%; height:100%; background:${progressGradient}; border-radius:10px;"></div>
                </div>
                <h3 style="font-size:1.55rem; font-weight:850; color:${titleColor}; margin:0 0 10px; letter-spacing:-0.02em;">${locCrop}</h3>
                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
                    <span class="badge" style="background:#dbeafe; color:#1e40af; font-weight:600; font-size:0.78rem; padding:4px 10px; border-radius:6px;">🌿 ${locCategory}</span>
                    <span class="badge" style="background:#f1f5f9; color:#475569; font-weight:600; font-size:0.78rem; padding:4px 10px; border-radius:6px;">⏱️ ${locDuration}</span>
                    <span class="badge" style="background:#e0f2fe; color:#0369a1; font-weight:600; font-size:0.78rem; padding:4px 10px; border-radius:6px;">💧 ${locWaterReq}</span>
                </div>
                <div class="feasibility-card" style="margin-top:12px; padding:14px 16px; background:${item.rank === 1 ? '#ffffff' : '#f8fafc'}; border-radius:12px; border:1px solid ${item.rank === 1 ? '#bbf7d0' : '#e2e8f0'}; font-size:0.84rem; line-height:1.55;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; padding-bottom:8px; border-bottom:1px solid ${item.rank === 1 ? '#f0fdf4' : '#e2e8f0'};">
                        <span style="font-weight:750; color:${item.rank === 1 ? '#166534' : '#334155'}; font-size:0.88rem;">★ ${feasTitle}</span>
                        <span style="background:${item.rank === 1 ? '#dcfce7' : '#f1f5f9'}; color:${item.rank === 1 ? '#15803d' : '#475569'}; font-weight:750; font-size:0.78rem; padding:2px 10px; border-radius:12px; border:1px solid ${item.rank === 1 ? '#86efac' : '#cbd5e1'};">${feasScore}% • ${locFeasStatus}</span>
                    </div>
                    <div style="color:#334155; margin-bottom:5px;"><strong style="color:#0f172a;">• ${npkLabel}</strong> ${locNpk || "N-P-K Optimal"}</div>
                    <div style="color:#334155; margin-bottom:5px;"><strong style="color:#0f172a;">• ${phLabel}</strong> ${locPh || "pH Neutral"}</div>
                    <div style="color:#334155;"><strong style="color:#0f172a;">• ${climateLabel}</strong> ${locClimate}</div>
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
            const data = await res.json();

            if (!res.ok) {
                if (errBox) {
                    errBox.textContent = data.error || "Input validation failed";
                    errBox.style.display = "block";
                }
                return;
            }

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
    window.handleCropRecommendation = handleCropRecommendation;
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
